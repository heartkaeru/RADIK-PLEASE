import math
import random
import pygame


class PerlinNoise2D:
    def __init__(self, seed: int):
        self.seed = seed
        self.rng = random.Random(seed)

        self.p = list(range(256))
        self.rng.shuffle(self.p)
        self.p += self.p

    def _fade(self, t: float) -> float:
        # Fade curve: 6t^5 - 15t^4 + 10t^3
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, t: float, a: float, b: float) -> float:
        return a + t * (b - a)

    def _grad(self, hash_val: int, x: float, y: float) -> float:
        # Gradient dot product
        h = hash_val & 3
        u = x if (h & 1) == 0 else -x
        v = y if (h & 2) == 0 else -y
        return u + v

    def get(self, x: float, y: float) -> float:
        # 1. Find grid cell coordinates
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255

        # 2. Find relative x, y within the cell
        xf = x - math.floor(x)
        yf = y - math.floor(y)

        # 3. Compute fade curves for xf, yf
        u = self._fade(xf)
        v = self._fade(yf)

        # 4. Hash coordinates of the 4 cell corners
        aa = self.p[self.p[X] + Y]
        ba = self.p[self.p[X + 1] + Y]
        ab = self.p[self.p[X] + Y + 1]
        bb = self.p[self.p[X + 1] + Y + 1]

        # 5. Gradient dot products and interpolation
        x1 = self._lerp(u, self._grad(aa, xf, yf), self._grad(ba, xf - 1, yf))
        x2 = self._lerp(u, self._grad(ab, xf, yf - 1), self._grad(bb, xf - 1, yf - 1))
        
        res = self._lerp(v, x1, x2)
        
        # 6. Map to [0, 1] range (true Perlin returns ~[-1, 1])
        return (res + 1.0) / 2.0

    def fbm(self, x: float, y: float, octaves: int = 4) -> float:
        val = 0.0
        amp = 0.5
        freq = 1.0
        max_val = 0.0
        for _ in range(octaves):
            # Map get() from [0, 1] back to [-1, 1] for fbm addition, or just keep it [0, 1]
            # Keeping it simple: accumulate raw get() values
            val += self.get(x * freq, y * freq) * amp
            max_val += amp
            amp *= 0.5
            freq *= 2.0
        # Normalize back to [0, 1]
        return val / max_val



def generate_document_photo(
    original_sprite: pygame.Surface, width: int, height: int, seed: int
) -> pygame.Surface:
    surface = pygame.Surface((width, height))

    bg_color = (235, 235, 240)
    surface.fill(bg_color)

    orig_w, orig_h = original_sprite.get_size()

    crop_width = int(orig_w * 0.8)
    crop_height = int(crop_width * (height / width))

    crop_x = orig_w // 2 - crop_width // 2
    crop_y = int(orig_h * 0.05)

    crop_rect = pygame.Rect(crop_x, crop_y, crop_width, crop_height)

    portrait = pygame.Surface((crop_width, crop_height), pygame.SRCALPHA)
    portrait.blit(original_sprite, (0, 0), crop_rect)

    portrait_scaled = pygame.transform.scale(portrait, (width, height))

    noise_gen = PerlinNoise2D(seed)

    for y in range(height):
        for x in range(width):
            color = portrait_scaled.get_at((x, y))

            if color.a == 0:
                final_r, final_g, final_b = bg_color
            else:
                final_r, final_g, final_b = color.r, color.g, color.b

            gray = int(final_r * 0.299 + final_g * 0.587 + final_b * 0.114)

            noise_val = noise_gen.get(x * 0.5, y * 0.5)
            noise_modifier = (
                noise_val - 0.5
            ) * 40

            gray = max(0, min(255, int(gray + noise_modifier)))

            surface.set_at((x, y), (gray, gray, gray, 255))

    pygame.draw.rect(surface, (20, 20, 20), surface.get_rect(), 2)

    return surface


def generate_signature(seed: int, width: int, height: int) -> pygame.Surface:
    rng = random.Random(
        seed + 100
    )
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    noise = PerlinNoise2D(seed + 200)

    num_points = rng.randint(15, 30)
    points = []

    current_x = 10.0
    for i in range(num_points):
        step_x = (width - 20) / num_points * rng.uniform(0.5, 1.5)
        current_x += step_x
        if current_x > width - 10:
            current_x = width - 10

        n_val = noise.fbm(current_x * 0.05, 0.0)
        y = 10 + n_val * (height - 20)

        points.append((int(current_x), int(y)))

        if current_x >= width - 10:
            break

    if len(points) >= 2:
        pygame.draw.aalines(surface, (0, 0, 150, 255), False, points)
        offset_points = [(p[0], p[1] + 1) for p in points]
        pygame.draw.aalines(surface, (0, 0, 150, 200), False, offset_points)

    return surface


def generate_card_background(
    seed: int, width: int, height: int, is_vip: bool = False
) -> pygame.Surface:
    rng = random.Random(seed + 500)
    surface = pygame.Surface((width, height))

    if is_vip:
        base_color = (230, 210, 210)
    else:
        base_color = (235, 240, 245)

    surface.fill(base_color)

    noise = PerlinNoise2D(seed + 600)

    line_color = (
        base_color[0] - 20,
        base_color[1] - 20,
        base_color[2] - 20,
        100,
    )
    line_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y_start in range(0, height, 40):
        points = []
        for x in range(0, width + 20, 20):
            n = noise.get(x * 0.02, y_start * 0.05)
            y = y_start + (n - 0.5) * 30
            points.append((x, y))
        if len(points) > 1:
            pygame.draw.aalines(line_surface, line_color, False, points)

    for x_start in range(0, width, 40):
        points = []
        for y in range(0, height + 20, 20):
            n = noise.get(x_start * 0.05, y * 0.02)
            x = x_start + (n - 0.5) * 30
            points.append((x, y))
        if len(points) > 1:
            pygame.draw.aalines(line_surface, line_color, False, points)

    surface.blit(line_surface, (0, 0))

    seal_radius = rng.randint(30, 50)
    seal_x = width - seal_radius - rng.randint(20, 50)
    seal_y = height // 2 + rng.randint(-30, 30)

    seal_color = (200, 180, 180, 150) if is_vip else (180, 200, 220, 150)
    pygame.draw.circle(
        line_surface, seal_color, (seal_x, seal_y), seal_radius, 4
    )
    pygame.draw.circle(
        line_surface, seal_color, (seal_x, seal_y), seal_radius - 8, 2
    )

    surface.blit(line_surface, (0, 0))

    return surface
