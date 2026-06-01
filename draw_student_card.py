import pygame
import os

pygame.init()
pygame.display.set_mode((1, 1), pygame.HIDDEN)

# Pixel art size
W = 130
H = 75

# Add extra space for drop shadow
W_FULL = W + 5
H_FULL = H + 5
surface = pygame.Surface((W_FULL, H_FULL), pygame.SRCALPHA)

# True pixel art palette, now more muted and desaturated to fit the table/buttons
OUTLINE = (15, 15, 20)
BASE_COLOR = (42, 50, 68) # Muted grayish blue
HIGHLIGHT = (65, 75, 95)
SHADOW = (25, 32, 48)
TEXT_COLOR = (210, 215, 220)
TEXT_SHADOW = (20, 25, 35)
LOGO_COLOR = (180, 160, 90) # Muted gold
LOGO_SHADOW = (110, 90, 45)

# Draw Drop Shadow
pygame.draw.rect(surface, (0, 0, 0, 110), (3, 4, W, H))

# Draw base
pygame.draw.rect(surface, OUTLINE, (0, 0, W, H))
pygame.draw.rect(surface, BASE_COLOR, (1, 1, W-2, H-2))

# Draw bevel (light top/left, dark bottom/right)
pygame.draw.line(surface, HIGHLIGHT, (1, 1), (W-2, 1))
pygame.draw.line(surface, HIGHLIGHT, (1, 1), (1, H-2))
pygame.draw.line(surface, SHADOW, (1, H-2), (W-2, H-2))
pygame.draw.line(surface, SHADOW, (W-2, 1), (W-2, H-2))

# Draw spine
pygame.draw.line(surface, SHADOW, (8, 1), (8, H-2))
pygame.draw.line(surface, OUTLINE, (9, 0), (9, H-1))
pygame.draw.line(surface, HIGHLIGHT, (10, 1), (10, H-2))

# Dithered texture for leather
for y in range(2, H-2):
    for x in range(11, W-2):
        if (x + y) % 2 == 0:
            surface.set_at((x, y), (36, 45, 62))

# Custom 5x5 font
font5x5 = {
    'У': ["X   X", "X   X", " XXXX", "    X", "XXXX "],
    'Р': ["XXXX ", "X   X", "XXXX ", "X    ", "X    "],
    'А': ["  X  ", " X X ", "XXXXX", "X   X", "X   X"],
    'Л': ["   XX", "  X X", " X  X", "X   X", "X   X"],
    'Ь': ["X    ", "X    ", "XXXX ", "X   X", "XXXX "],
    'С': [" XXXX", "X    ", "X    ", "X    ", " XXXX"],
    'К': ["X   X", "X  X ", "XXX  ", "X  X ", "X   X"],
    'И': ["X   X", "X  XX", "X X X", "XX  X", "X   X"],
    'Й': ["X   X", "X  XX", "X X X", "XX  X", "X   X"], 
    'Ф': ["  X  ", " XXX ", "X X X", " XXX ", "  X  "],
    'Е': ["XXXXX", "X    ", "XXXX ", "X    ", "XXXXX"],
    'Д': ["  XX ", " X  X", " X  X", "XXXXX", "X   X"],
    'Н': ["X   X", "X   X", "XXXXX", "X   X", "X   X"],
    'В': ["XXXX ", "X   X", "XXXX ", "X   X", "XXXX "],
    'Т': ["XXXXX", "  X  ", "  X  ", "  X  ", "  X  "],
    'Ч': ["X   X", "X   X", " XXXX", "    X", "    X"],
    'Б': ["XXXXX", "X    ", "XXXX ", "X   X", "XXXX "],
    ' ': ["     ", "     ", "     ", "     ", "     "],
    '.': ["     ", "     ", "     ", "     ", "  X  "],
}

def draw_text(text, x, y, color, shadow_color):
    curr_x = x
    for char in text:
        if char == 'Й':
            surface.set_at((curr_x + 1, y - 2), shadow_color)
            surface.set_at((curr_x + 2, y - 2), shadow_color)
            surface.set_at((curr_x + 3, y - 2), shadow_color)
            surface.set_at((curr_x + 1, y - 3), color)
            surface.set_at((curr_x + 2, y - 3), color)
            surface.set_at((curr_x + 3, y - 3), color)
            
        if char in font5x5:
            matrix = font5x5[char]
            for row_i, row_str in enumerate(matrix):
                for col_i, px in enumerate(row_str):
                    if px == 'X':
                        surface.set_at((curr_x + col_i, y + row_i + 1), shadow_color)
                        surface.set_at((curr_x + col_i, y + row_i), color)
        curr_x += 6 

draw_text("УРАЛЬСКИЙ", 45, 12, TEXT_COLOR, TEXT_SHADOW)
draw_text("ФЕДЕРАЛЬНЫЙ", 45, 20, TEXT_COLOR, TEXT_SHADOW)
draw_text("УНИВЕРСИТЕТ", 45, 28, TEXT_COLOR, TEXT_SHADOW)

draw_text("СТУДЕНЧЕСКИЙ", 28, 48, LOGO_COLOR, LOGO_SHADOW)
draw_text("БИЛЕТ", 52, 56, LOGO_COLOR, LOGO_SHADOW)

# Draw Logo (UrFU stylized 'У' or 'J')
logo_matrix = [
    "  XXXXX",
    "      X",
    "      X",
    "    XXX",
    "  XX   ",
    " XX    ",
    "XX     "
]
logo_x = 22
logo_y = 15
for row_i, row_str in enumerate(logo_matrix):
    for col_i, px in enumerate(row_str):
        if px == 'X':
            surface.set_at((logo_x + col_i, logo_y + row_i + 1), LOGO_SHADOW)
            surface.set_at((logo_x + col_i, logo_y + row_i), LOGO_COLOR)

# Scale 2x with NEAREST to preserve chunky pixels
scaled = pygame.transform.scale(surface, (W_FULL * 2, H_FULL * 2))

os.makedirs("assets/images", exist_ok=True)
pygame.image.save(scaled, "assets/images/student_card.png")
print("Authentic Papers, Please style card with shadow generated!")
