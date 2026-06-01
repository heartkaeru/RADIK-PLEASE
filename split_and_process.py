import os
from PIL import Image, ImageEnhance

def remove_bg_and_trim(img):
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    
    for r, g, b, a in data:
        dist = ((255 - r)**2 + (255 - g)**2 + (255 - b)**2)**0.5
        if dist < 80:
            new_data.append((255, 255, 255, 0))
        elif dist < 160:
            alpha = int(((dist - 80) / 80) * 255)
            dim_factor = 0.8
            new_data.append((int(r * dim_factor), int(g * dim_factor), int(b * dim_factor), alpha))
        else:
            new_data.append((r, g, b, 255))
            
    img.putdata(new_data)
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img

def create_pressed(img):
    width, height = img.size
    new_width, new_height = int(width * 0.95), int(height * 0.95)
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Brightness(resized_img)
    darkened_img = enhancer.enhance(0.7)

    pressed_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    paste_x = (width - new_width) // 2
    paste_y = (height - new_height) // 2 + int(height * 0.05)
    pressed_img.paste(darkened_img, (paste_x, paste_y), darkened_img)
    return pressed_img

spritesheet_path = r"C:\Users\User\.gemini\antigravity-ide\brain\b6c0afcd-b332-4326-93ad-7d149175c647\matching_buttons_1781271408452.png"
sheet = Image.open(spritesheet_path)
width, height = sheet.size
mid = width // 2

left_half = sheet.crop((0, 0, mid, height))
right_half = sheet.crop((mid, 0, width, height))

allow_btn = remove_bg_and_trim(left_half)
deny_btn = remove_bg_and_trim(right_half)

max_w = max(allow_btn.width, deny_btn.width)
max_h = max(allow_btn.height, deny_btn.height)
size = max(max_w, max_h)

def square_pad(img, size):
    new_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x = (size - img.width) // 2
    y = (size - img.height) // 2
    new_img.paste(img, (x, y), img)
    return new_img

allow_btn = square_pad(allow_btn, size)
deny_btn = square_pad(deny_btn, size)

allow_btn.save("assets/images/btn_allow.png")
deny_btn.save("assets/images/btn_deny.png")

create_pressed(allow_btn).save("assets/images/btn_allow_pressed.png")
create_pressed(deny_btn).save("assets/images/btn_deny_pressed.png")
print("Done splitting and processing.")
