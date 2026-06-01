import os
import shutil
from PIL import Image, ImageEnhance

# Copy originals
shutil.copy(r"C:\Users\User\.gemini\antigravity-ide\brain\a3b30af5-f0e8-45fc-bfd4-958c822ac5ea\green_allow_button_1781268930548.png", "assets/images/btn_allow.png")
shutil.copy(r"C:\Users\User\.gemini\antigravity-ide\brain\a3b30af5-f0e8-45fc-bfd4-958c822ac5ea\red_deny_button_1781268938559.png", "assets/images/btn_deny.png")

def process_image(input_path, output_path, pressed_path):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()
    new_data = []
    
    for r, g, b, a in data:
        # Calculate how close the pixel is to white (255, 255, 255)
        dist = ((255 - r)**2 + (255 - g)**2 + (255 - b)**2)**0.5
        
        if dist < 80:
            new_data.append((255, 255, 255, 0))  # Completely transparent
        elif dist < 160:
            # Alpha gradient based on distance to soften the edge
            alpha = int(((dist - 80) / 80) * 255)
            # Dim the RGB to avoid bright white halo
            dim_factor = 0.8
            new_data.append((int(r * dim_factor), int(g * dim_factor), int(b * dim_factor), alpha))
        else:
            new_data.append((r, g, b, 255))
            
    img.putdata(new_data)
    img.save(output_path)

    width, height = img.size
    new_width, new_height = int(width * 0.95), int(height * 0.95)
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Brightness(resized_img)
    darkened_img = enhancer.enhance(0.7)

    pressed_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    paste_x = (width - new_width) // 2
    paste_y = (height - new_height) // 2 + int(height * 0.05)
    pressed_img.paste(darkened_img, (paste_x, paste_y), darkened_img)

    pressed_img.save(pressed_path)

process_image("assets/images/btn_allow.png", "assets/images/btn_allow.png", "assets/images/btn_allow_pressed.png")
process_image("assets/images/btn_deny.png", "assets/images/btn_deny.png", "assets/images/btn_deny_pressed.png")
