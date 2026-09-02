# C:\Users\hp\Desktop\FinArg\finarg\extract_sentences.py

import pandas as pd
from pathlib import Path

print("="*60)
print(" EXTRACTING SENTENCES FOR ANNOTATION")
print("="*60)

# Load original dataset
file_path = Path(__file__).parent / "data" / "raw" / "finarg_ecc_train.csv"

if not file_path.exists():
    print(f" File not found: {file_path}")
    print(" Run download_finarg.py first.")
    exit()

df = pd.read_csv(file_path)
print(f" Loaded {len(df)} sentences")

# Create annotation template with all sentences
annotation_df = df[['id', 'text']].copy()

# Add original label
annotation_df['sentence_label'] = df['gold'].apply(lambda x: 'claim' if x == 1 else 'premise')

# Add empty columns for YOUR annotations
annotation_df['target'] = ""              # YOU WILL FILL
annotation_df['target_category'] = ""     # YOU WILL FILL
annotation_df['premise_span'] = ""        # YOU WILL FILL
annotation_df['claim_span'] = ""          # YOU WILL FILL
annotation_df['annotator'] = "YourName"
annotation_df['timestamp'] = ""

# --- SAVE IN: finarg/annotated/ (NOT data/annotated/) ---
output_dir = Path(__file__).parent / "annotated"  # 👈 YAHAN CHANGE!
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "sentences_to_annotate.csv"

# Save as CSV
annotation_df.to_csv(output_path, index=False)

print(f"\n Created annotation file!")
print(f" Location: {output_path}")
print(f" Total sentences: {len(annotation_df)}")
print(f"\n Columns: {annotation_df.columns.tolist()}")

print("\n" + "="*60)
print(" NEXT STEPS:")
print("="*60)
print("1. Open this CSV in Excel / VS Code / Google Sheets")
print(f"   Path: {output_path}")
print("2. Fill in: target, target_category, premise_span, claim_span")
print("3. Save the file")
print("4. Run: python finarg/convert_csv_to_json.py")
print("="*60)