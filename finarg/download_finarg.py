# C:\Users\hp\Desktop\FinArg\finarg\download_finarg.py

from datasets import load_dataset
import pandas as pd
import os
from pathlib import Path

print(" Loading dataset: TheFinAI/finarg-ecc-auc_train")

try:
    # Load the dataset
    dataset = load_dataset("TheFinAI/finarg-ecc-auc_train")
    
    # Check structure
    print(f" Dataset structure: {dataset}")
    
    # Access data
    if "train" in dataset:
        df = dataset["train"].to_pandas()
    else:
        df = dataset.to_pandas()
    
    print(f" Loaded {len(df)} records")
    print("\n Sample:")
    print(df.head())
    
   
    script_dir = Path(__file__).parent  
    
    
    output_dir = script_dir / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n Saving dataset to: {output_dir}")
    
    
    df.to_csv(output_dir / "finarg_ecc_train.csv", index=False)
    df.to_parquet(output_dir / "finarg_ecc_train.parquet", index=False)
    df.to_json(output_dir / "finarg_ecc_train.jsonl", orient="records", lines=True)
    
    print(f" Saved files:")
    print(f"   - {output_dir / 'finarg_ecc_train.csv'}")
    print(f"   - {output_dir / 'finarg_ecc_train.parquet'}")
    print(f"   - {output_dir / 'finarg_ecc_train.jsonl'}")
    
except Exception as e:
    print(f" Error: {e}")
    print("\n Make sure you:")
    print("1. Are logged in: hf auth login")
    print("2. Accepted terms at: https://huggingface.co/datasets/TheFinAI/finarg-ecc-auc_train")