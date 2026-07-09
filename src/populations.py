import pandas as pd
import requests as rq
from datetime import datetime as dt
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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

    api_key = "d7fc54be9bea59f851eb1a3004204c60f758932e"

    if year is None:
        year = (dt.now().year) - 3
    print(f"Pulling US population data for {year}...")

    url = f"https://api.census.gov/data/{year}/pep/charv"
    parameters = {"get": "NAME,POP",
                "for": "State:*",
                "YEAR": str(year),
                "key": api_key
    }

    response = rq.get(url, params= parameters, verify= False)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}")
    try:
        data = response.json()
    except Exception:
        print("API did not return JSON. Response was:")
        print(response.text)
        raise

    if len(data) <= 1:
        raise ValueError("Population API returned no data.")
    
    df_pop = pd.DataFrame(data[1:], columns= data[0])
    df_pop["POP"] = df_pop["POP"].astype(int)

    self.df_pop = df_pop

    return self.df_pop

def state_mapping(self):

    df_pop = self.df_pop
    df_prev = self.df_prev

    reverse_state_map = {v: k for k, v in state_map.items()}

    df_pop["State"] = df_pop["NAME"].map(reverse_state_map)

    df_prev["State"] = df_prev["State"].map(reverse_state_map)
    df_prev = df_prev.dropna(how="all")

    self.df_pop = df_pop
    self.df_prev = df_prev

    return self.df_pop, self.df_prev



def merge_population(self):
    df = self.df
    df_pop = self.df_pop

    df = df.merge(
    df_pop[["State", "POP"]],
    on = "State",
    how="left"
    )

    df = df.rename(columns={"POP": "Population"})
    self.df = df

    return self.df

def merge_prevalence(self):
    df = self.df
    df_prev = self.df_prev

    df = df.merge(
        df_prev[["State", "Incidence_rate"]],
        on = "State",
        how = "left"
    )

    self.df = df

    return self.df