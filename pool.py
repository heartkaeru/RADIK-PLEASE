import pygame

class ObjectPool:
    """
    Пул объектов. Позволяет переиспользовать объекты, вместо того чтобы 
    постоянно их создавать и удалять.
    """
    def __init__(self, factory_func):
        self.factory_func = factory_func
        self.pool = []

    def get(self):
        if self.pool:
            return self.pool.pop()
        return self.factory_func()

    def release(self, obj):
        self.pool.append(obj)


class FloatingTextEffect:
    """
    Эффект всплывающего текста.
    Анимирует движение текста вверх и постепенное исчезновение.
    """
    def __init__(self):
        self.active = False
        self.x = 0.0
        self.y = 0.0
        self.surface = None
        self.alpha = 255
        self.speed = 0.0
        self.life_time = 0.0
        self.max_life_time = 0.0
        self.is_static = False

    def reset(self, text, color, font, x, y, speed=50.0, max_life_time=2.0, is_static=False):
        self.surface = font.render(text, True, color).convert_alpha()
        self.x = float(x)
        self.y = float(y)
        self.alpha = 255
        self.speed = float(speed)
        self.life_time = 0.0
        self.max_life_time = float(max_life_time)
        self.is_static = is_static
        self.active = True

    def update(self, dt):
        if not self.active or self.is_static:
            return
            
        self.life_time += dt
        self.y -= self.speed * dt
        
        fade_start = self.max_life_time * 0.5
        if self.life_time > fade_start:
            progress = (self.life_time - fade_start) / (self.max_life_time - fade_start)
            self.alpha = max(0, int(255 * (1.0 - progress)))
            if self.surface:
                self.surface.set_alpha(self.alpha)
                
        if self.life_time >= self.max_life_time:
            self.active = False

    def draw(self, screen):
        if self.active and self.surface:
            screen.blit(self.surface, (int(self.x), int(self.y)))
