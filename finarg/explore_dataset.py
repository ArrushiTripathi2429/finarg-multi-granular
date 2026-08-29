# C:\Users\hp\Desktop\FinArg\finarg\explore_dataset.py

import pandas as pd
from pathlib import Path

print("="*60)
print(" FINARG DATASET EXPLORATION")
print("="*60)


file_path = Path(__file__).parent / "data" / "raw" / "finarg_ecc_train.csv"

if not file_path.exists():
    print(f" File not found: {file_path}")
    print(" Run download_finarg.py first to download the dataset.")
    exit()
    
df = pd.read_csv(file_path)

print(f"\n Dataset loaded successfully!")
print(f"   Total sentences: {len(df)}")
print(f"   Columns: {df.columns.tolist()}")

# --- Basic Info ---
print("\n" + "="*60)
print(" BASIC INFORMATION")
print("="*60)
print(f"\nData Types:")
print(df.dtypes)

print(f"\n🔍 Null Values:")
print(df.isnull().sum())

# --- Label Distribution ---
print("\n" + "="*60)
print(" LABEL DISTRIBUTION")
print("="*60)

label_counts = df['gold'].value_counts()
print(f"\n0 = Premise: {label_counts.get(0, 0)} sentences")
print(f"1 = Claim: {label_counts.get(1, 0)} sentences")
print(f"\n{label_counts}")

# --- Sample Sentences ---
print("\n" + "="*60)
print(" SAMPLE SENTENCES")
print("="*60)

for i in range(5):
    label = "CLAIM" if df.iloc[i]['gold'] == 1 else "PREMISE"
    text = df.iloc[i]['text']
    print(f"\n{i+1}. [{label}] {text}")
    print(f"   ID: {df.iloc[i]['id']}")

# --- Text Length Analysis ---
print("\n" + "="*60)
print(" TEXT LENGTH ANALYSIS")
print("="*60)

df['word_count'] = df['text'].str.split().str.len()
df['char_count'] = df['text'].str.len()

print(f"\nWord Count:")
print(f"   Min: {df['word_count'].min()}")
print(f"   Max: {df['word_count'].max()}")
print(f"   Mean: {df['word_count'].mean():.1f}")
print(f"   Median: {df['word_count'].median()}")

print(f"\nCharacter Count:")
print(f"   Min: {df['char_count'].min()}")
print(f"   Max: {df['char_count'].max()}")
print(f"   Mean: {df['char_count'].mean():.1f}")
print(f"   Median: {df['char_count'].median()}")

# --- Check if sentences contain financial keywords ---
print("\n" + "="*60)
print(" FINANCIAL KEYWORD CHECK")
print("="*60)

keywords = ['revenue', 'margin', 'growth', 'demand', 'pricing', 'guidance', 
            'cost', 'profit', 'earnings', 'cash', 'debt', 'investment',
            'supply', 'inventory', 'market', 'risk', 'strategy']

found = []
for kw in keywords:
    count = df['text'].str.lower().str.contains(kw).sum()
    if count > 0:
        found.append((kw, count))
        print(f"   '{kw}': {count} sentences")

if not found:
    print("   No financial keywords found (check dataset structure)")


summary = {
    "total_sentences": len(df),
    "columns": df.columns.tolist(),
    "premise_count": int(label_counts.get(0, 0)),
    "claim_count": int(label_counts.get(1, 0)),
    "avg_word_count": float(df['word_count'].mean()),
    "avg_char_count": float(df['char_count'].mean()),
    "samples": [
        {"id": df.iloc[i]['id'], "label": "claim" if df.iloc[i]['gold']==1 else "premise", "text": df.iloc[i]['text'][:100]}
        for i in range(min(3, len(df)))
    ]
}

import json
summary_path = Path(__file__).parent / "data" / "raw" / "dataset_summary.json"
with open(summary_path, "w") as f:
    json.dump(summary, f, indent=2)

print(f"\nSummary saved to: {summary_path}")
print("\n" + "="*60)
print(" EXPLORATION COMPLETE!")
print("="*60)