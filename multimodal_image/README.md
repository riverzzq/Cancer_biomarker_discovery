# Multimodal Image Pipeline (TCGA-BRCA)

This directory contains the image-side pipeline for multimodal cancer biomarker discovery using TCGA-BRCA whole-slide images (WSIs).

The pipeline covers:
- Downloading WSI data from GDC
- Tiling WSIs into image patches
- Generating slide-level and tile-level labels
- Sanity checks for downstream multimodal fusion

---

## Directory Structure

multimodal_image/
├── scripts/
│ ├── tile_wsi.py # Tile WSIs into image patches
│ └── make_tile_labels.py # Generate tile-level labels
├── tools/
├── sanity_check.py # Sanity checks for generated image data
├── data/
│ ├── wsi_raw/ # Raw WSI files (NOT tracked in GitHub)
│ ├── tiles/ # Tiled image patches (NOT tracked)
│ ├── metadata/ # Metadata files
│ ├── slide_labels.csv # Slide-level labels
│ └── tile_labels.csv # Tile-level labels
└── README.md


---

## Data Availability

Due to size constraints, large data files are **not stored in this GitHub repository**, including:
- Raw whole-slide images (`wsi_raw/`)
- Tiled image patches (`tiles/`)
- Large expression matrices

These data are stored separately on shared storage and can be regenerated using the provided scripts.

---

## Usage

### 1. Tile WSIs
```bash
python scripts/tile_wsi.py


### 2. Generate tile-level labels
```bash
python scripts/make_tile_labels.py

### 3. Run sanity checks
```bash
python sanity_check.py
