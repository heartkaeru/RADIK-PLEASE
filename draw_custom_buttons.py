import pygame
import os

pygame.init()
pygame.display.set_mode((1, 1), pygame.HIDDEN)

# Colors matching the image
GREEN_BASE = (95, 142, 85)
GREEN_LIGHT = (117, 163, 107)
GREEN_DARK = (63, 105, 54)

RED_BASE = (176, 57, 50)
RED_LIGHT = (201, 80, 72)
RED_DARK = (135, 33, 27)

BASE_BG = (109, 87, 69)
BASE_BORDER = (53, 40, 31)

BASE_SCREWS = (130, 140, 140)

SIZE = 120

# Use Segoe UI to match game's font
try:
    font = pygame.font.SysFont("segoeui", 18, bold=True)
except:
    font = pygame.font.Font(None, 24)

def draw_button(color_type, is_pressed):
    surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    
    pad = 4
    
    # Metal base background
    pygame.draw.rect(surface, BASE_BG, (pad, pad, SIZE - 2*pad, SIZE - 2*pad), border_radius=8)
    pygame.draw.rect(surface, BASE_BORDER, (pad, pad, SIZE - 2*pad, SIZE - 2*pad), width=4, border_radius=8)
    
    # Screws in corners
    for sx, sy in [(pad+6, pad+6), (SIZE-pad-6, pad+6), (pad+6, SIZE-pad-6), (SIZE-pad-6, SIZE-pad-6)]:
        pygame.draw.circle(surface, BASE_SCREWS, (sx, sy), 3)
        pygame.draw.circle(surface, BASE_BORDER, (sx, sy), 3, width=1)
        pygame.draw.line(surface, BASE_BORDER, (sx-2, sy-2), (sx+2, sy+2), 1)

    # Inner cavity (shadow inside the base)
    cavity_pad = pad + 10
    pygame.draw.rect(surface, (50, 40, 35), (cavity_pad, cavity_pad, SIZE - 2*cavity_pad, SIZE - 2*cavity_pad), border_radius=6)
    
    if color_type == 'allow':
        main_c = GREEN_BASE
        light_c = GREEN_LIGHT
        dark_c = GREEN_DARK
        text = "ОДОБРЕНО"
    else:
        main_c = RED_BASE
        light_c = RED_LIGHT
        dark_c = RED_DARK
        text = "ОТКАЗАНО"
        
    press_offset = 6 if is_pressed else 0
    
    bx = cavity_pad + 2
    by = cavity_pad + 2
    bw = SIZE - 2*cavity_pad - 4
    bh = SIZE - 2*cavity_pad - 4
    
    # Shadow / Side (3D depth)
    if not is_pressed:
        pygame.draw.rect(surface, dark_c, (bx, by + 6, bw, bh), border_radius=4)
        pygame.draw.rect(surface, BASE_BORDER, (bx, by + 6, bw, bh), width=3, border_radius=4)

    # Face of the button
    face_rect = (bx, by + press_offset, bw, bh - 6)
    pygame.draw.rect(surface, main_c, face_rect, border_radius=4)
    pygame.draw.rect(surface, BASE_BORDER, face_rect, width=3, border_radius=4)
    
    # Inner light bevel to give plastic/metal highlight
    bevel_rect = (bx + 3, by + press_offset + 3, bw - 6, bh - 12)
    pygame.draw.rect(surface, light_c, bevel_rect, width=3, border_radius=2)
    
    # Text
    text_surf = font.render(text, True, (245, 240, 230))
    text_rect = text_surf.get_rect(center=(SIZE//2, SIZE//2 + 20 + press_offset))
    surface.blit(text_surf, text_rect)
    
    # Icon (Checkmark or X)
    icon_color = (245, 240, 230)
    if color_type == 'allow':
        # Checkmark
        points = [
            (SIZE//2 - 14, SIZE//2 - 5 + press_offset),
            (SIZE//2 - 4, SIZE//2 + 5 + press_offset),
            (SIZE//2 + 14, SIZE//2 - 15 + press_offset)
        ]
        pygame.draw.lines(surface, icon_color, False, points, 7)
    else:
        # X
        w = 12
        cx = SIZE//2
        cy = SIZE//2 - 5 + press_offset
        pygame.draw.line(surface, icon_color, (cx - w, cy - w), (cx + w, cy + w), 7)
        pygame.draw.line(surface, icon_color, (cx - w, cy + w), (cx + w, cy - w), 7)
        
    return surface

os.makedirs("assets/images", exist_ok=True)
pygame.image.save(draw_button('allow', False), "assets/images/btn_allow.png")
pygame.image.save(draw_button('allow', True), "assets/images/btn_allow_pressed.png")
pygame.image.save(draw_button('deny', False), "assets/images/btn_deny.png")
pygame.image.save(draw_button('deny', True), "assets/images/btn_deny_pressed.png")

print("Custom style buttons generated!")
