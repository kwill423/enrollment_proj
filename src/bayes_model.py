
import pymc as pm
import numpy as np

def run_model(self):
    df = self.df

    y = df["enrollments"].values
    t = df["time"].values
    prior_rate = df["prior_rate"].values
    pop = df["population"].values
    incidence = df["incidence_rate"].values
    site_idx = df["site_idx"].values

    n_sites = df["site_idx"].nunique()

    with pm.Model() as model:
        beta_0 = pm.Normal("beta_0", 0, 5)
        beta_pop = pm.Normal("beta_pop", 0, 1)
        beta_inc = pm.Normal("beta_inc", 0, 1)

        sigma_site = pm.HalfNormal("sigma_site", 1)
        u_site = pm.Normal("u_site", 0, sigma_site, shape=n_sites)

        log_lambda = (
            beta_0
            + beta_pop * np.log(pop + 1)
            + beta_inc * np.log(incidence + 1)
            + u_site[site_idx]
            + np.log(t)
        )

        mu = pm.math.exp(log_lambda)

        pm.Poisson("y_obs", mu= mu, observed=y)

        self.trace = pm.sample(1000, tune=1000)

    return self.trace
