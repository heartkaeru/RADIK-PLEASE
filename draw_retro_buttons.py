import os
from PIL import Image, ImageDraw

def draw_industrial_button(color_type, is_pressed=False):
    size = 120
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Base padding
    pad = 8
    
    # Draw metal base
    draw.rectangle([pad, pad, size-pad, size-pad], fill=(20, 20, 20)) # Outer dark border
    draw.rectangle([pad+2, pad+2, size-pad-2, size-pad-2], fill=(80, 80, 85)) # Base main
    draw.rectangle([pad+4, pad+4, size-pad-4, size-pad-4], fill=(45, 45, 50)) # Inner dark cavity
    
    if color_type == 'allow':
        main_c = (70, 110, 70)
        light_c = (90, 140, 90)
        dark_c = (40, 70, 40)
    else:
        main_c = (140, 50, 50)
        light_c = (180, 70, 70)
        dark_c = (80, 30, 30)
        
    # Button sizes
    bx0, by0 = pad + 8, pad + 8
    bx1, by1 = size - pad - 8, size - pad - 8
    
    press_offset = 6 if is_pressed else 0
    
    # Draw button side (shadow)
    if not is_pressed:
        draw.rectangle([bx0, by0 + 8, bx1, by1], fill=dark_c)
        
    # Draw button top face
    face_y0 = by0 + press_offset
    face_y1 = by1 - 8 + press_offset
    draw.rectangle([bx0, face_y0, bx1, face_y1], fill=main_c)
    
    # Bevels
    draw.rectangle([bx0, face_y0, bx1, face_y0+3], fill=light_c) # Top highlight
    draw.rectangle([bx0, face_y0, bx0+3, face_y1], fill=light_c) # Left highlight
    
    # Symbol
    cx = (bx0 + bx1) // 2
    cy = (face_y0 + face_y1) // 2
    
    sym_c = (20, 25, 20)
    if color_type == 'allow':
        # Checkmark
        draw.line([(cx - 15, cy), (cx - 5, cy + 12), (cx + 15, cy - 12)], fill=sym_c, width=8, joint="curve")
    else:
        # X
        w = 12
        draw.line([(cx - w, cy - w), (cx + w, cy + w)], fill=sym_c, width=8)
        draw.line([(cx - w, cy + w), (cx + w, cy - w)], fill=sym_c, width=8)
        
    return img

draw_industrial_button('allow', False).save("assets/images/btn_allow.png")
draw_industrial_button('allow', True).save("assets/images/btn_allow_pressed.png")
draw_industrial_button('deny', False).save("assets/images/btn_deny.png")
draw_industrial_button('deny', True).save("assets/images/btn_deny_pressed.png")
print("Retro buttons generated!")
