from PIL import Image, ImageFilter
import os

def process_image(input_path, output_path):
    print(f"Processing {input_path} -> {output_path}")
    try:
        source_img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        print(f"Error opening source image {input_path}: {e}")
        return

    TARGET_WIDTH = 1200
    TARGET_HEIGHT = 630

    # Resize logic: Fill width (1200), maintain aspect ratio, then crop height
    w_ratio = TARGET_WIDTH / source_img.width
    scale = w_ratio 
    
    # If scaling by width makes height too small (<630), scale by height instead
    if (source_img.height * scale) < TARGET_HEIGHT:
        scale = TARGET_HEIGHT / source_img.height

    scaled_w = int(source_img.width * scale)
    scaled_h = int(source_img.height * scale)
    
    img_scaled = source_img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
    
    # Center crop
    left = (scaled_w - TARGET_WIDTH) // 2
    top = (scaled_h - TARGET_HEIGHT) // 2
    right = left + TARGET_WIDTH
    bottom = top + TARGET_HEIGHT
    
    final_img = img_scaled.crop((left, top, right, bottom))
    
    # Save (force overwrite)
    final_img.save(output_path)
    print(f"Saved {output_path} ({TARGET_WIDTH}x{TARGET_HEIGHT})")

# We must load into memory first because input and output path might be same
# Actually PIL Image.open is lazy, so we should be careful. 
# Let's read to memory or use temp name then rename in python.

def safe_process(filename):
    temp_name = f"temp_{filename}"
    process_image(filename, temp_name)
    if os.path.exists(temp_name):
        try:
            # FORCE REPLACE
            if os.path.exists(filename):
                os.remove(filename)
            os.rename(temp_name, filename)
            print(f"Overwrote {filename}")
        except OSError as e:
            print(f"Error renaming: {e}")

safe_process("og-image.png")
safe_process("twitter-card.png")
