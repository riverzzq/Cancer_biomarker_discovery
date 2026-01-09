import pandas as pd
from pathlib import Path

# 1) 读带Subtype的表
df = pd.read_csv("data/BRCA-data.tsv", sep="\t")

ID_COL = "Unnamed: 0"
LABEL_COL = "Subtype"

def to_patient_id(x: str) -> str:
    parts = str(x).split("-")
    return "-".join(parts[:3]) if len(parts) >= 3 else str(x)

# patient -> subtype 映射（如果同一 patient 多条，先保留第一条；后面可改成投票策略）
sub = df[[ID_COL, LABEL_COL]].dropna()
sub["patient_id"] = sub[ID_COL].map(to_patient_id)
sub = sub.drop_duplicates("patient_id")
patient_to_subtype = dict(zip(sub["patient_id"], sub[LABEL_COL].astype(str)))

print("Subtype categories in table:", sorted(set(patient_to_subtype.values())))

# 2) 扫描SVS并对齐
svs_paths = sorted(Path("data/wsi_raw").rglob("*.svs"))
rows = []
for p in svs_paths:
    patient_id = "-".join(p.name.split("-")[:3])  # TCGA-XX-XXXX
    rows.append({
        "svs_path": str(p),
        "svs_file": p.name,
        "patient_id": patient_id,
        "Subtype": patient_to_subtype.get(patient_id, None)
    })

out = pd.DataFrame(rows)

print("\nTotal svs:", len(out))
print("Matched subtype:", out["Subtype"].notna().sum())
print("\nUnmatched examples (first 10):")
print(out[out["Subtype"].isna()][["svs_file","patient_id"]].head(10).to_string(index=False))

out.to_csv("data/slide_labels.csv", index=False)
print("\nSaved -> data/slide_labels.csv")