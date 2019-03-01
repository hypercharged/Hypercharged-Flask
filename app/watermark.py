from PIL import Image
import os
images_path = "raw_assets/"
logo = Image.open("static/assets/hctransparentdark.png")
logo = logo.resize((1000, 1000), Image.ANTIALIAS)
for image in os.listdir(images_path):
    if "hctransparent" not in image and "favicon" not in image:
        raw = Image.open(images_path + image)
        w, h = raw.size
        w1, h1 = logo.size
        w2 = int((w - w1)/2)
        h2 = int((h - h1)/2)
        wmark = Image.new('RGB', (w, h), (0, 0, 0, 0))
        wmark.paste(raw, (0, 0))
        wmark.paste(logo, (w2, h2), mask=logo)
        wmark.save("static/assets/" + image)
