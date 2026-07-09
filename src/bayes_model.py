import pymc as pm
import numpy as np
import pandas as pd

def run_model(self):

    df = self.df   
    df["Site_idx"] = pd.Categorical(df["Site_id"]).codes
    df["Study_idx"] = pd.Categorical(df["Study_id"]).codes

    df_model = self.df.dropna(subset=["Population", "Incidence_rate"])
    self.df_model = df_model
    print(f"Training model on {len(df_model)} rows out of {len(df)} total rows...")

    y = df_model["Enrollments"].values
    t = df_model["Time"].values
    prior_rate = df_model["Prior_rate"].values
    pop = df_model["Population"].values
    incidence = df_model["Incidence_rate"].values
    site_idx = df_model["Site_idx"].values
    study_idx = df_model["Study_idx"].values

    n_sites = df_model["Site_idx"].nunique()
    n_studies = df_model["Study_idx"].nunique()

    with pm.Model() as model:

        beta_0 = pm.Normal("beta_0", 0, 5)
        beta_pop = pm.Normal("beta_pop", 0, 1)
        beta_inc = pm.Normal("beta_inc", 0, 1)

        sigma_site = pm.HalfNormal("sigma_site", 1)
        sigma_study = pm.HalfNormal("sigma_study", 1)

        u_site = pm.Normal("u_site", 0, sigma_site, shape=n_sites)
        u_study = pm.Normal("u_study", 0, sigma_study, shape=n_studies)

        log_lambda = (
            beta_0
            + beta_pop * np.log(pop + 1)
            + beta_inc * np.log(incidence + 1)
            + u_site[site_idx]
            + u_study[study_idx]
            + np.log(t)
        )

        mu = pm.math.exp(log_lambda)

        pm.Poisson("y_obs", mu= mu, observed=y)

        self.trace = pm.sample(1000, tune=1000)

    return self.df_model, self.trace
