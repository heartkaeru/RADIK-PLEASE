import math
import random
import pygame


class ValueNoise2D:
    """
    Простой генератор двумерного шума значений (Value Noise).
    Создает псевдослучайную непрерывную текстуру шума на основе заданного зерна (seed).
    Используется для придания процедурным текстурам "естественности".
    """
    def __init__(self, seed: int):
        self.seed = seed
        self.rng = random.Random(seed)
        # Генерация таблицы перестановок
        self.p = list(range(256))
        self.rng.shuffle(self.p)
        self.p += self.p

    def _fade(self, t: float) -> float:
        """Сглаживающая функция для интерполяции (6t^5 - 15t^4 + 10t^3)."""
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, t: float, a: float, b: float) -> float:
        """Линейная интерполяция между a и b."""
        return a + t * (b - a)

    def get(self, x: float, y: float) -> float:
        """
        Возвращает значение шума в координатах (x, y).
        Результат находится в диапазоне от 0.0 до 1.0.
        """
        xi = int(math.floor(x)) & 255
        yi = int(math.floor(y)) & 255
        xf = x - math.floor(x)
        yf = y - math.floor(y)

        u = self._fade(xf)
        v = self._fade(yf)

        def val(ix, iy):
            # Детерминированное псевдослучайное значение для точки сетки [0, 1)
            idx = self.p[self.p[ix] + iy]
            # Используем индекс для создания числа с плавающей точкой от 0 до 1
            return (idx * 2654435761 % 4294967296) / 4294967296.0

        x00 = val(xi, yi)
        x10 = val((xi + 1) & 255, yi)
        x01 = val(xi, (yi + 1) & 255)
        x11 = val((xi + 1) & 255, (yi + 1) & 255)

        return self._lerp(v, self._lerp(u, x00, x10), self._lerp(u, x01, x11))

    def fbm(self, x: float, y: float, octaves: int = 4) -> float:
        """
        Фрактальное броуновское движение (FBM).
        Складывает несколько слоев шума с разной частотой для большей детализации.
        """
        val = 0.0
        amp = 0.5
        freq = 1.0
        for _ in range(octaves):
            val += self.get(x * freq, y * freq) * amp
            amp *= 0.5
            freq *= 2.0
        return val


def generate_document_photo(original_sprite: pygame.Surface, width: int, height: int, seed: int) -> pygame.Surface:
    """
    Генерирует фотографию для документа на основе оригинального спрайта персонажа.
    Вырезает верхнюю часть (портрет), масштабирует и накладывает процедурные
    эффекты "печати" (шум, черно-белый фильтр или сепия).
    """
    rng = random.Random(seed)
    surface = pygame.Surface((width, height))
    
    # Цвет фона фотокарточки
    bg_color = (235, 235, 240)
    surface.fill(bg_color)
    
    orig_w, orig_h = original_sprite.get_size()
    
    # 1. Вырезаем портретно-плечевую зону из оригинального спрайта
    # Предполагаем, что лицо находится в верхней трети спрайта.
    crop_width = int(orig_w * 0.8)
    crop_height = int(crop_width * (height / width))
    
    # Смещение, чтобы голова была по центру
    crop_x = orig_w // 2 - crop_width // 2
    crop_y = int(orig_h * 0.05) # чуть отступаем сверху
    
    crop_rect = pygame.Rect(crop_x, crop_y, crop_width, crop_height)
    
    # Создаем вырезанную часть
    portrait = pygame.Surface((crop_width, crop_height), pygame.SRCALPHA)
    portrait.blit(original_sprite, (0, 0), crop_rect)
    
    # 2. Масштабируем до размеров фото в документе
    portrait_scaled = pygame.transform.scale(portrait, (width, height))
    
    # 3. Применяем эффект "напечатанной фотографии"
    noise_gen = ValueNoise2D(seed)
    
    for y in range(height):
        for x in range(width):
            color = portrait_scaled.get_at((x, y))
            
            # Если пиксель прозрачный, берем цвет фона
            if color.a == 0:
                final_r, final_g, final_b = bg_color
            else:
                final_r, final_g, final_b = color.r, color.g, color.b
                
            # Перевод в ЧБ (градации серого)
            gray = int(final_r * 0.299 + final_g * 0.587 + final_b * 0.114)
            
            # Добавляем шум принтера
            noise_val = noise_gen.get(x * 0.5, y * 0.5)
            noise_modifier = (noise_val - 0.5) * 40 # случайное отклонение яркости
            
            gray = max(0, min(255, int(gray + noise_modifier)))
            
            # Немного синеватый/винтажный оттенок (опционально)
            # Для строгого документа сделаем просто серым
            surface.set_at((x, y), (gray, gray, gray, 255))
            
    # Добавляем строгую черную рамку
    pygame.draw.rect(surface, (20, 20, 20), surface.get_rect(), 2)

    return surface


def generate_signature(seed: int, width: int, height: int) -> pygame.Surface:
    """
    Генерирует процедурную подпись с использованием плавных 1D кривых шума.
    """
    rng = random.Random(seed + 100)
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    noise = ValueNoise2D(seed + 200)
    
    num_points = rng.randint(15, 30)
    points = []
    
    current_x = 10.0
    for i in range(num_points):
        # Движемся вперед по оси X с небольшим разбросом
        step_x = (width - 20) / num_points * rng.uniform(0.5, 1.5)
        current_x += step_x
        if current_x > width - 10:
            current_x = width - 10
            
        # Ось Y управляется шумом для создания петелек и росчерков
        n_val = noise.fbm(current_x * 0.05, 0.0)
        y = 10 + n_val * (height - 20)
        
        points.append((int(current_x), int(y)))
        
        if current_x >= width - 10:
            break
            
    if len(points) >= 2:
        # Отрисовка сглаженных линий ручки
        pygame.draw.aalines(surface, (0, 0, 150, 255), False, points)
        # Делаем подпись чуть толще, отрисовывая ее со смещением
        offset_points = [(p[0], p[1]+1) for p in points]
        pygame.draw.aalines(surface, (0, 0, 150, 200), False, offset_points)

    return surface


def generate_card_background(seed: int, width: int, height: int, is_vip: bool = False) -> pygame.Surface:
    """
    Генерирует процедурный фон для документа (гильоширная сетка и водяные знаки).
    """
    rng = random.Random(seed + 500)
    surface = pygame.Surface((width, height))
    
    if is_vip:
        base_color = (230, 210, 210)  # Слегка красновато-золотистый для удостоверений
    else:
        base_color = (235, 240, 245)  # Слегка синеватый для обычных студентов
        
    surface.fill(base_color)
    
    noise = ValueNoise2D(seed + 600)
    
    # Рисуем полупрозрачную гильоширную защитную сетку
    line_color = (base_color[0] - 20, base_color[1] - 20, base_color[2] - 20, 100)
    line_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Горизонтальные волнистые линии
    for y_start in range(0, height, 40):
        points = []
        for x in range(0, width + 20, 20):
            n = noise.get(x * 0.02, y_start * 0.05)
            y = y_start + (n - 0.5) * 30
            points.append((x, y))
        if len(points) > 1:
            pygame.draw.aalines(line_surface, line_color, False, points)

    # Вертикальные волнистые линии
    for x_start in range(0, width, 40):
        points = []
        for y in range(0, height + 20, 20):
            n = noise.get(x_start * 0.05, y * 0.02)
            x = x_start + (n - 0.5) * 30
            points.append((x, y))
        if len(points) > 1:
            pygame.draw.aalines(line_surface, line_color, False, points)
            
    surface.blit(line_surface, (0, 0))
    
    # Добавляем круглую печать/водяной знак в случайном месте
    seal_radius = rng.randint(30, 50)
    seal_x = width - seal_radius - rng.randint(20, 50)
    seal_y = height // 2 + rng.randint(-30, 30)
    
    seal_color = (200, 180, 180, 150) if is_vip else (180, 200, 220, 150)
    pygame.draw.circle(line_surface, seal_color, (seal_x, seal_y), seal_radius, 4)
    pygame.draw.circle(line_surface, seal_color, (seal_x, seal_y), seal_radius - 8, 2)
    
    surface.blit(line_surface, (0, 0))
    
    return surface
