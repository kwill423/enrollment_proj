import pandas as pd
import pgeocode as pg

def clean_zip(self):
    '''
    Purpose
    -------
    Cleans zip codes that have a '-' and 4 additional numbers after the initial 5 digit zip code
    '''

    df = self.df
    
    df = df.dropna(subset=["State", "Zip"])
    
    
    df["Zip"] = (
        pd.to_numeric(df["Zip"], errors="coerce")
        .astype("Int64")
        .astype(str)
        .str.zfill(5)
    )

    print(df.head())
    self.df = df

    return self.df


def zip_conversion(self):

    df = self.df

    nomi = pg.Nominatim("us")
    coords = nomi.query_postal_code(df["Zip"].tolist())

    df["Latitude"] = coords["latitude"].values
    df["Longitude"] = coords["longitude"].values

    self.df = df

    return self.df