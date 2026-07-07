import pandas as pd

def load_enroll_data(self, file_path):
    df = pd.read_excel(file_path)
    df = df.rename(columns={
        "Study": "study_id",
        "Study Site": "site_id",
        "Pts per Site": "enrollments",
        "SER": "prior_rate",
        "Duration (months)": "time",
        "State": "state"
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
            "State (cleaned)": "state",
            "Incidence Rate": "incidence_rate"
        })
    df_prev["incidence_rate"] = pd.to_numeric(
            df_prev["incidence_rate"], errors="coerce"
        )
    
    self.df_prev = df_prev
    
    return self.df_prev
