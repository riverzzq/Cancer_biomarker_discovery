from pathlib import Path
import pandas as pd

SLIDE_CSV = Path("data/slide_labels.csv")
TILES_ROOT = Path("data/tiles")
OUT_CSV = Path("data/tile_labels.csv")

# skip normal and keep 4 subtypes
DROP_NORMAL = True
KEEP = {"BRCA_LumA", "BRCA_LumB", "BRCA_Basal", "BRCA_Her2"}

def extract_patient_id(slide_id: str) -> str:
    parts = slide_id.split("-")
    return "-".join(parts[:3]) if len(parts) >= 3 else slide_id

def main():
    slides = pd.read_csv(SLIDE_CSV)
    slides = slides[slides["Subtype"].notna()].copy()

    if DROP_NORMAL:
        slides = slides[slides["Subtype"].isin(KEEP)].copy()

    # patient_id -> subtype
    p2y = dict(zip(slides["patient_id"], slides["Subtype"]))

    rows = []
    img_ext = {".png", ".jpg", ".jpeg"}

    for slide_dir in TILES_ROOT.iterdir():
        if not slide_dir.is_dir():
            continue

        slide_id = slide_dir.name
        patient_id = extract_patient_id(slide_id)
        subtype = p2y.get(patient_id)

        if subtype is None:
            continue  # 没有label的slide直接跳过

        for fp in slide_dir.rglob("*"):
            if fp.suffix.lower() in img_ext:
                rows.append({
                    "tile_path": str(fp),
                    "slide_id": slide_id,
                    "patient_id": patient_id,
                    "Subtype": subtype
                })

    df = pd.DataFrame(rows)

    print("Total tiles:", len(df))
    print("Slides with tiles:", df["slide_id"].nunique())
    print("Patients:", df["patient_id"].nunique())
    print("\nLabel distribution:")
    print(df["Subtype"].value_counts())

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)
    print(f"\nSaved -> {OUT_CSV}")

if __name__ == "__main__":
    main()
