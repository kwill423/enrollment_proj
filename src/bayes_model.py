import pymc as pm
import numpy as np
import pandas as pd
import arviz as az


def run_model(self):
    df = self.df.copy()

    # --------------------------------------------------
    # 1. Make sure required numeric columns are numeric
    # --------------------------------------------------
    numeric_cols = [
        "Enrollments",
        "Time",
        "Prior_rate",
        "Population",
        "Incidence_rate",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # --------------------------------------------------
    # 2. Remove rows that can break the Bayesian model
    # --------------------------------------------------
    required_cols = [
        "Site_id",
        "Study_id",
        "Enrollments",
        "Time",
        "Population",
        "Incidence_rate",
    ]

    df_model = df.dropna(subset=required_cols).copy()

    # Time must be > 0 because we use log(Time)
    df_model = df_model[df_model["Time"] > 0].copy()

    # Enrollments for Poisson must not be negative
    df_model = df_model[df_model["Enrollments"] >= 0].copy()

    # Population and incidence must not be negative
    df_model = df_model[df_model["Population"] >= 0].copy()
    df_model = df_model[df_model["Incidence_rate"] >= 0].copy()

    print(f"Training model on {len(df_model)} rows out of {len(df)} total rows...")

    if len(df_model) == 0:
        raise ValueError(
            "No valid rows left after filtering. "
            "Check Time, Enrollments, Population, and Incidence_rate."
        )

    # --------------------------------------------------
    # 3. Recreate site/study indexes AFTER filtering
    # --------------------------------------------------
    df_model["Site_idx"] = pd.Categorical(df_model["Site_id"]).codes
    df_model["Study_idx"] = pd.Categorical(df_model["Study_id"]).codes

    self.df_model = df_model

    # --------------------------------------------------
    # 4. Prepare arrays
    # --------------------------------------------------
    y = df_model["Enrollments"].astype(int).values
    t = df_model["Time"].astype(float).values
    pop = df_model["Population"].astype(float).values
    incidence = df_model["Incidence_rate"].astype(float).values
    site_idx = df_model["Site_idx"].astype(int).values
    study_idx = df_model["Study_idx"].astype(int).values

    n_sites = int(df_model["Site_idx"].nunique())
    n_studies = int(df_model["Study_idx"].nunique())

    # --------------------------------------------------
    # 5. Debug prints
    # --------------------------------------------------
    print("Data checks before sampling:")
    print("Rows used:", len(df_model))
    print("Enrollments min/max:", y.min(), y.max())
    print("Time min/max:", t.min(), t.max())
    print("Population min/max:", pop.min(), pop.max())
    print("Incidence min/max:", incidence.min(), incidence.max())
    print("n_sites:", n_sites, "| max site_idx:", site_idx.max())
    print("n_studies:", n_studies, "| max study_idx:", study_idx.max())

    print("Missing values after filtering:")
    print(
        df_model[
            [
                "Enrollments",
                "Time",
                "Population",
                "Incidence_rate",
                "Site_idx",
                "Study_idx",
            ]
        ].isna().sum()
    )

    # --------------------------------------------------
    # 6. Safety checks
    # --------------------------------------------------
    if np.any(~np.isfinite(y)):
        raise ValueError("Enrollments contains NaN or infinite values.")

    if np.any(~np.isfinite(t)):
        raise ValueError("Time contains NaN or infinite values.")

    if np.any(~np.isfinite(pop)):
        raise ValueError("Population contains NaN or infinite values.")

    if np.any(~np.isfinite(incidence)):
        raise ValueError("Incidence_rate contains NaN or infinite values.")

    if np.any(t <= 0):
        raise ValueError("Time contains zero or negative values. Cannot use log(Time).")

    if site_idx.max() >= n_sites:
        raise ValueError("site_idx is out of bounds.")

    if study_idx.max() >= n_studies:
        raise ValueError("study_idx is out of bounds.")

    # --------------------------------------------------
    # 7. Log-transform and scale predictors
    #    This helps avoid bad initial energy in PyMC
    # --------------------------------------------------
    log_pop = np.log1p(pop)
    log_incidence = np.log1p(incidence)
    log_time = np.log(t)

    log_pop_scaled = (log_pop - log_pop.mean()) / log_pop.std()
    log_incidence_scaled = (log_incidence - log_incidence.mean()) / log_incidence.std()

    # In case std is zero
    log_pop_scaled = np.nan_to_num(log_pop_scaled, nan=0.0, posinf=0.0, neginf=0.0)
    log_incidence_scaled = np.nan_to_num(
        log_incidence_scaled,
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )

    # --------------------------------------------------
    # 8. Build Bayesian model
    # --------------------------------------------------
    with pm.Model() as model:
        beta_0 = pm.Normal("beta_0", mu=0, sigma=2, initval=0)
        beta_pop = pm.Normal("beta_pop", mu=0, sigma=1, initval=0)
        beta_inc = pm.Normal("beta_inc", mu=0, sigma=1, initval=0)

        sigma_site = pm.HalfNormal("sigma_site", sigma=1, initval=0.5)
        sigma_study = pm.HalfNormal("sigma_study", sigma=1, initval=0.5)

        u_site_raw =pm.Normal(
            "u_site_raw",
            mu=0,
            sigma=1,
            shape=n_sites,
            initval=np.zeros(n_sites),
        )

        u_site =pm.Deterministic(
            "u_site",
            sigma_site * u_site_raw,
        )

        u_study_raw = pm.Normal(
            "u_study_raw",
            mu=0,
            sigma=1,
            shape=n_studies,
            initval=np.zeros(n_studies),
        )

        u_study = pm.Deterministic(
            "u_study",
            sigma_study * u_study_raw,
        )

        log_lambda = (
            beta_0
            + beta_pop * log_pop_scaled
            + beta_inc * log_incidence_scaled
            + u_site[site_idx]
            + u_study[study_idx]
            + log_time
        )

        # Prevent extreme values from crashing sampling
        log_lambda = pm.math.clip(log_lambda, -20, 20)

        mu = pm.math.exp(log_lambda)

        pm.Poisson("y_obs", mu=mu, observed=y)

        print("Starting PyMC sampling...")

        try:
            self.trace = pm.sample(
                draws=4000,
                tune=4000,
                chains=4,
                cores=1,
                init="adapt_diag",
                target_accept=0.99,
                progressbar=True,
                random_seed=42,
            )

        except Exception as e:
            print("Model failed during sampling.")
            print("Error was:")
            print(e)
            print("Running PyMC model debug...")
            model.debug()
            raise
        
        print("Model complete")

    return self.df_model, self.trace