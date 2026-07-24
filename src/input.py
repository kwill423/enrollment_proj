import pandas as pd
from pathlib import Path

def load_enroll_data(self, file_path):
    df = pd.read_excel(file_path, sheet_name= "DiseaseTarget")
    df = df.rename(columns={
        "Study": "Study_id",
        "Study Site": "Site_id",
        "Fiscal Year": "FY",
        "Pts per Site": "Enrollments",
        "SER": "Prior_rate",
        "Duration (months)": "Time",
        "State": "State",
        "Postal / Zip Code": "Zip"
    })

    
    df.drop(
        columns=df.columns[df.columns.str.contains('Unnamed')],
        inplace=True
    )

    # Remove completely identical rows
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    print(f"Removed {before - after} exact duplicate rows")


    self.df = df

    return self.df

def load_prev_data(self, file_path2):

    file_ext = Path(file_path2).suffix.lower()

    if file_ext in [".xlsx", ".xls"]:
        df_prev = pd.read_excel(
        file_path2,
        skiprows=8,
        usecols="B,C"
        )
    elif file_ext == ".csv":
        df_prev = pd.read_csv(
            file_path2,
            skiprows=8,
            usecols=[1,2]
        )
    else:
        raise ValueError(f"Unsupported file type:{file_ext}")

    df_prev = df_prev.iloc[1:].reset_index(drop=True)
       
    df_prev = df_prev.rename(columns={
            "State (cleaned)": "State",
            "Age-Adjusted Incidence Rate([rate note]) - cases per 100,000": "Incidence_rate"
        })
    df_prev["Incidence_rate"] = pd.to_numeric(
            df_prev["Incidence_rate"], errors="coerce"
        )
    
    self.df_prev = df_prev
    
    return self.df_prev
