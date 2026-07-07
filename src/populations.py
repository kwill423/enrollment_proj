import pandas as pd
import requests as rq
from datetime import datetime as dt

state_map = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
    "DC": "District of Columbia",
    "PR": "Puerto Rico"
}
def get_state_populations(self, year= None):
    if year is None:
        year = dt.now().year

    url = f"https://api.census.gov/data/{year}/pep/charv"
    parameters = {"get": "NAME,POP",
                "for": "state:*",
                "YEAR": str(year)
    }
    response = rq.get(url, params= parameters)

    
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}")

    data = response.json()

    if len(data) <= 1:
        raise ValueError("Population API returned no data.")
    
    df_pop = pd.DataFrame(data[1:], columns= data[0])
    df_pop["POP"] = df_pop["POP"].astype(int)

    self.df_pop = df_pop

    return self.df_pop

def merge_population(self):
    df = self.df

    df = df.merge(
    self.df_pop[["NAME", "POP"]],
    left_on="state_name",
    right_on="NAME",
    how="left"
    )

    df = df.rename(columns={"POP": "population"})
    self.df = df

    return self.df