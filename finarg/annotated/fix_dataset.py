import pandas as pd
import json
import re
import os
import sys
import numpy as np

# Ensure files are saved in the same folder as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

CSV_FILE = "my_annotations.csv"

def find_csv_file():
    if os.path.exists(CSV_FILE):
        return CSV_FILE
    files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if len(files) == 1:
        print(f"⚠️ '{CSV_FILE}' nahi mili. Automatically '{files[0]}' use kar rahe hain.")
        return files[0]
    print(f"❌ CSV nahi mili. Current folder: {os.getcwd()}")
    sys.exit(1)

def split_spans(val):
    if pd.isna(val): return []
    val = str(val).strip()
    if not val or val.lower() == 'nan': return []
    if '||' in val: parts = re.split(r'\s*\|\|\s*', val)
    elif '|' in val: parts = re.split(r'\s*\|\s*', val)
    elif ';' in val: parts = re.split(r'\s*;\s*', val)
    else: parts = [val]
    return [p.strip() for p in parts if p.strip()]

def make_record(row, warnings=None):
    text = str(row['text'])
    spans = []
    for col, label in [('premise_span', 'premise'), ('claim_span', 'claim')]:
        for s in split_spans(row[col]):
            start = text.find(s)
            if start == -1:
                start = text.lower().find(s.lower())
                if start == -1:
                    if warnings is not None: warnings.append(f"{row['id']} | {col} | NOT FOUND: {s[:70]}")
                    continue
                s = text[start:start+len(s)]
            spans.append({"start": start, "end": start + len(s), "text": s, "label": label})
    
    unique, seen = [], set()
    for sp in sorted(spans, key=lambda x: (x['start'], x['end'])):
        key = (sp['start'], sp['end'], sp['label'])
        if key not in seen:
            seen.add(key)
            unique.append(sp)
            
    return {
        "id": row['id'],
        "text": text,
        "sentence_label": str(row['sentence_label']).strip().lower(),
        "target": str(row['target']).strip().lower(),
        "target_category": str(row['target_category']).strip().lower(),
        "spans": unique
    }

def save_jsonl(records, path):
    with open(path, "w", encoding="utf-8") as f:
        for r in records: f.write(json.dumps(r, ensure_ascii=False) + "\n")

def main():
    print("=" * 60)
    print(f"RUNNING IN FOLDER: {os.getcwd()}")
    print("=" * 60)

    # --- FIXED CSV LOADING SECTION ---
    csv_path = find_csv_file()
    print(f"\n[1/7] Loading: {csv_path}")
    try: 
        # on_bad_lines='skip' will ignore the bad lines (like line 72)
        df = pd.read_csv(csv_path, on_bad_lines='skip')
    except UnicodeDecodeError: 
        df = pd.read_csv(csv_path, encoding='latin-1', on_bad_lines='skip')
    print(f"   ✅ {len(df)} rows loaded")
    # ---------------------------------

    required = ['id', 'text', 'sentence_label', 'target', 'target_category', 'premise_span', 'claim_span']
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"   ❌ Missing columns: {missing}")
        sys.exit(1)

    for col in ['sentence_label', 'target', 'target_category']:
        df[col] = df[col].astype(str).str.strip().str.lower()

    cat_counts = df['target_category'].value_counts()
    rare = cat_counts[cat_counts < 30].index.tolist()
    if rare: df['target_category'] = df['target_category'].replace(rare, 'other')

    print(f"\n[2/7] Extracting spans...")
    warnings = []
    records = [make_record(row, warnings) for _, row in df.iterrows()]
    print(f"   ✅ {len(records)} records built")
    if warnings:
        with open("warnings.txt", "w", encoding="utf-8") as f:
            for w in warnings: f.write(w + "\n")
        print(f"   ⚠️ {len(warnings)} warnings saved to warnings.txt")

    total_spans = sum(len(r['spans']) for r in records)
    multi_span = sum(1 for r in records if len(r['spans']) > 1)
    zero_span = sum(1 for r in records if len(r['spans']) == 0)

    stats_lines = [
        "=" * 60, "DATASET STATISTICS", "=" * 60,
        f"Total rows:                {len(records)}",
        f"Total spans extracted:     {total_spans}",
        f"Rows with MULTIPLE spans:  {multi_span} ({100*multi_span/len(records):.1f}%)",
        f"Rows with ZERO spans:      {zero_span} ({100*zero_span/len(records):.1f}%)",
        "\nSentence label distribution:", str(df['sentence_label'].value_counts().to_string()),
        "\nTarget category distribution:", str(df['target_category'].value_counts().to_string()),
        "\nTop 30 targets:", str(df['target'].value_counts().head(30).to_string())
    ]
    stats_text = "\n".join(stats_lines)
    with open("stats.txt", "w", encoding="utf-8") as f: f.write(stats_text)
    print("\n" + stats_text)

    print(f"\n[3/7] Splitting train/val/test...")
    df['call_id'] = df['id'].astype(str).str.extract(r'(finargeccauc\d+)')
    if df['call_id'].isna().all():
        from sklearn.model_selection import train_test_split
        train_df, temp = train_test_split(df, test_size=0.3, stratify=df['sentence_label'], random_state=42)
        val_df, test_df = train_test_split(temp, test_size=0.5, stratify=temp['sentence_label'], random_state=42)
    else:
        calls = df['call_id'].dropna().unique()
        np.random.seed(42)
        np.random.shuffle(calls)
        n = len(calls)
        train_df = df[df['call_id'].isin(calls[:int(0.7*n)])]
        val_df = df[df['call_id'].isin(calls[int(0.7*n):int(0.85*n)])]
        test_df = df[df['call_id'].isin(calls[int(0.85*n):])]

    print(f"\n[4/7] Saving files...")
    save_jsonl(records, "finarg_clean.jsonl")
    save_jsonl([make_record(row) for _, row in train_df.iterrows()], "train.jsonl")
    save_jsonl([make_record(row) for _, row in val_df.iterrows()], "val.jsonl")
    save_jsonl([make_record(row) for _, row in test_df.iterrows()], "test.jsonl")

    print("\n" + "=" * 60)
    print(" DONE! Files created in THIS folder.")
    print("=" * 60)

if __name__ == "__main__":
    main()