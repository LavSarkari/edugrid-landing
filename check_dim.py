from PIL import Image
import os

files = ["og-image.png", "twitter-card.png"]
for f in files:
    if os.path.exists(f):
        img = Image.open(f)
        print(f"{f}: {img.size}")
    else:
        print(f"{f} NOT FOUND")
