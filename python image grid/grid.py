from PIL import Image, ImageDraw, ImageFont
import os
import shutil

# Configurations
input_folder = "/Users/chhailengtim/Desktop/python/images"
output_folder = "/Users/chhailengtim/Desktop/python/output_images"
processed_folder = "/Users/chhailengtim/Desktop/python/processed_images"
WATERMARK_TEXT = "© Kape Watch"   # Change watermark text
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"  # Path to font
FONT_COLOR = (255, 255, 255, 100)  # White with ~40% opacity

# Create output & processed folders if not exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(processed_folder, exist_ok=True)

# Function to crop image to fit 540x540
def crop_center(img, target_size=(540, 540)):
    width, height = img.size
    target_w, target_h = target_size
    aspect_img = width / height
    aspect_target = target_w / target_h

    # Scale to fill
    if aspect_img > aspect_target:
        new_height = target_h
        new_width = int(width * (target_h / height))
    else:
        new_width = target_w
        new_height = int(height * (target_w / width))

    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Crop center
    left = (new_width - target_w) / 2
    top = (new_height - target_h) / 2
    right = left + target_w
    bottom = top + target_h
    return img.crop((left, top, right, bottom))

# Function to add watermark in center (smaller text)
def add_watermark_center(img, text=WATERMARK_TEXT):
    watermark_img = img.convert("RGBA")
    overlay = Image.new("RGBA", watermark_img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Smaller font size (width / 15 instead of / 8)
    font_size = int(watermark_img.width / 30)
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except:
        font = ImageFont.load_default()

    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Position in center
    x = (watermark_img.width - text_w) / 2
    y = (watermark_img.height - text_h) / 2

    # Draw text (semi-transparent)
    draw.text((x, y), text, font=font, fill=FONT_COLOR)

    # Combine layers
    return Image.alpha_composite(watermark_img, overlay).convert("RGB")


# Process images in batches of 4
batch_num = 1
while True:
    images = [f for f in os.listdir(input_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if len(images) < 4:
        print("Not enough images to make another grid. Done!")
        break

    # Take first 4 images
    selected_images = images[:4]
    imgs_cropped = []

    for img_name in selected_images:
        img_path = os.path.join(input_folder, img_name)
        img = Image.open(img_path).convert("RGB")
        img = crop_center(img)
        imgs_cropped.append(img)

    # Create new grid
    grid_img = Image.new("RGB", (1080, 1080), (255, 255, 255))
    grid_img.paste(imgs_cropped[0], (0, 0))
    grid_img.paste(imgs_cropped[1], (540, 0))
    grid_img.paste(imgs_cropped[2], (0, 540))
    grid_img.paste(imgs_cropped[3], (540, 540))

    # Add centered watermark
    grid_img = add_watermark_center(grid_img)

    # Save output grid
    output_path = os.path.join(output_folder, f"grid_{batch_num}.jpg")
    grid_img.save(output_path)
    print(f"✅ Grid {batch_num} saved at {output_path}")

    # Move processed images
    for img_name in selected_images:
        shutil.move(os.path.join(input_folder, img_name), os.path.join(processed_folder, img_name))

    batch_num += 1
