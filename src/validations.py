import pandas as pd
import os

def validate_excel(file_path, df, req_cols):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    missing_cols = [col for col in req_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"The following required columns are missing: {missing_cols}")
    
    empty_cols = [col for col in req_cols if df[col].isna().all()]
    if empty_cols:
        raise ValueError(f"The following columns contain no data: {empty_cols}")
    
    if df.empty:
        raise ValueError(f"Entire data frame is empty; please check file path and column headers.")
    
    print("Excel file validation passed for: {file_path}")

def validate_csv(csv_path):
    if csv_path:
        print("Saved results as CSV to: {csv_path}")