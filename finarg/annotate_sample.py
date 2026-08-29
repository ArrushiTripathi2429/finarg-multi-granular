# C:\Users\hp\Desktop\FinArg\finarg\annotate_sample.py

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import os

print("="*60)
print(" FINARG ANNOTATION TOOL - SAMPLE SET")
print("="*60)

# Load sample
sample_path = Path(__file__).parent / "data" / "annotated" / "sample_50_sentences.csv"
df = pd.read_csv(sample_path)

# Check progress
anno_dir = Path(__file__).parent / "data" / "annotated"
progress_path = anno_dir / "progress_sample.json"

if progress_path.exists():
    with open(progress_path, "r") as f:
        progress = json.load(f)
    start_idx = progress["last_annotated"] + 1
else:
    progress = {"last_annotated": -1, "annotations": []}
    start_idx = 0

print(f"\n Annotating sentences {start_idx+1} to {len(df)}")
print("Type 'skip' to skip a sentence, 'quit' to stop.\n")

annotations = progress["annotations"]

for idx in range(start_idx, len(df)):
    row = df.iloc[idx]
    
    print("="*80)
    print(f"Sentence {idx+1}/{len(df)}")
    print(f"ID: {row['id']}")
    print(f"Original Label: {'CLAIM' if row['gold']==1 else 'PREMISE'}")
    print(f"\n Text: {row['text']}")
    print("="*80)
    
    # Target
    print("\n 1. Target (specific financial topic):")
    print("   Options: revenue, margins, guidance, demand, pricing, ")
    print("            cost, capex, liquidity, market_share, etc.")
    target = input("   Enter target (or 'skip'/'quit'): ").strip()
    
    if target.lower() == 'quit':
        break
    if target.lower() == 'skip':
        continue
    
    # Category
    print("\n 2. Target Category (broad group):")
    print("   Options: guidance, profitability, revenue, cost_structure,")
    print("            liquidity, investment, operations, market, risk, strategy")
    category = input("   Enter category: ").strip()
    
    # Spans
    print("\n 3. Spans (break into premise + claim):")
    print("   Example: 'Although costs increased' → premise_span")
    print("            'we maintained margins' → claim_span")
    
    print("\n   Enter span 1:")
    span1_text = input("   Text: ").strip()
    span1_label = input("   Label (premise_span/claim_span): ").strip()
    
    print("\n   Enter span 2:")
    span2_text = input("   Text: ").strip()
    span2_label = input("   Label (premise_span/claim_span): ").strip()
    
    # Save annotation
    annotation = {
        "id": row['id'],
        "text": row['text'],
        "sentence_label": "claim" if row['gold'] == 1 else "premise",
        "target": target,
        "target_category": category,
        "spans": [
            {"text": span1_text, "label": span1_label},
            {"text": span2_text, "label": span2_label}
        ],
        "metadata": {
            "annotator": "YourName",
            "timestamp": datetime.now().isoformat(),
            "original_gold": int(row['gold'])
        }
    }
    
    annotations.append(annotation)
    
    # Save progress
    progress = {
        "last_annotated": idx,
        "annotations": annotations,
        "last_updated": datetime.now().isoformat()
    }
    
    with open(progress_path, "w") as f:
        json.dump(progress, f, indent=2)
    
    print(f"\n Saved! {len(annotations)} annotations done.")
    print("-"*80)

print(f"\n Annotation complete! Total: {len(annotations)} sentences.")