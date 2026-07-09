import pandas as pd

def load_enroll_data(self, file_path):
    df = pd.read_excel(file_path)
    df = df.rename(columns={
        "Study": "Study_id",
        "Study Site": "Site_id",
        "Pts per Site": "Enrollments",
        "SER": "Prior_rate",
        "Duration (months)": "Time",
        "State": "State"
    })

    self.df = df

    return self.df

def load_prev_data(self, file_path2):
    df_prev = pd.read_excel(
    file_path2,
    skiprows=8,
    usecols="B,C"
    )

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
