# C:\Users\hp\Desktop\FinArg\finarg\setup_annotation.py

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

print("="*60)
print("📁 SETTING UP ANNOTATION FILES")
print("="*60)

# Load dataset
df = pd.read_csv("finarg/data/raw/finarg_ecc_train.csv")

# Create output directories
anno_dir = Path(__file__).parent / "data" / "annotated"
anno_dir.mkdir(parents=True, exist_ok=True)

# Create annotation template
print("\n📝 Creating annotation template...")

template = {
    "id": "",
    "text": "",
    "sentence_label": "",
    "target": "",
    "target_category": "",
    "spans": [],
    "metadata": {
        "annotator": "YourName",
        "timestamp": datetime.now().isoformat()
    }
}

# Save template
with open(anno_dir / "annotation_template.json", "w") as f:
    json.dump(template, f, indent=2)

# Create a small sample (first 50 sentences for practice)
sample_df = df.head(50)
sample_df.to_csv(anno_dir / "sample_50_sentences.csv", index=False)

print(f" Template saved: {anno_dir / 'annotation_template.json'}")
print(f" Sample 50 sentences: {anno_dir / 'sample_50_sentences.csv'}")

print("\n Dataset Summary:")
print(f"   Total sentences: {len(df)}")
print(f"   Premises: {len(df[df['gold']==0])}")
print(f"   Claims: {len(df[df['gold']==1])}")
print(f"   Sample size: 50 sentences")

# Create progress tracker
progress = {
    "total": len(df),
    "annotated": 0,
    "remaining": len(df),
    "last_updated": datetime.now().isoformat()
}

with open(anno_dir / "progress.json", "w") as f:
    json.dump(progress, f, indent=2)

print(f" Progress tracker created: {anno_dir / 'progress.json'}")
print("\n" + "="*60)
print(" SETUP COMPLETE! Ready to annotate.")
print("="*60)