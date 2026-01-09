import os
import openslide
import numpy as np
from PIL import Image

INPUT_DIR = "data/wsi_raw"
OUTPUT_DIR = "data/tiles"
TILE_SIZE = 224
WHITE_THRESHOLD = 0.8  # background filter

os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_background(tile):
    gray = np.array(tile.convert("L")) / 255.0
    return gray.mean() > WHITE_THRESHOLD

for root, _, files in os.walk(INPUT_DIR):
    for f in files:
        if not f.endswith(".svs"):
            continue

        slide_path = os.path.join(root, f)
        slide_id = f.replace(".svs", "")
        slide_out = os.path.join(OUTPUT_DIR, slide_id)
        os.makedirs(slide_out, exist_ok=True)

        slide = openslide.OpenSlide(slide_path)
        width, height = slide.level_dimensions[0]

        for x in range(0, width, TILE_SIZE):
            for y in range(0, height, TILE_SIZE):
                tile = slide.read_region((x, y), 0, (TILE_SIZE, TILE_SIZE)).convert("RGB")

                if is_background(tile):
                    continue

                tile.save(os.path.join(slide_out, f"{x}_{y}.png"))

        slide.close()
        print(f"Finished tiling {slide_id}")

