import pandas as pd
import numpy as np
import kaleido
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.formatting.rule import ColorScaleRule
import os
import plotly.express as px

def compute_performance(self):
    
    print("Entering compute performance...")
    trace = self.trace
    df = self.df
    df_model = self.df_model

    u_site_mean = trace.posterior["u_site"].mean(
        dim=("chain", "draw")
    ).values


    # One row per site
    site_lookup = (
        df_model[
            ["Site_idx", "Site_id", "State", "Latitude", "Longitude"]
        ]
        .drop_duplicates("Site_idx")
        .sort_values("Site_idx")
        .reset_index(drop=True)
    )

    # Total enrollments per site
    site_enrollments = (
        df_model
        .groupby("Site_idx", as_index=False)["Enrollments"]
        .sum()
    )

    
    # Total enrollments per site
    site_enrollments = (
        df_model
        .groupby("Site_idx", as_index=False)["Enrollments"]
        .sum()
    )

    # Merge enrollments onto the site-level table
    site_performance = site_lookup.merge(
        site_enrollments,
        on="Site_idx",
        how="left"
    )

    # Add model results
    site_performance["U_site"] = u_site_mean
    site_performance["Performance_multiplier"] = np.exp(u_site_mean)

    site_performance = (
        site_performance
        .sort_values("Performance_multiplier", ascending=False)
        .reset_index(drop=True)
    )
    
    u_study_mean = trace.posterior["u_study"].mean(dim=("chain", "draw")).values

    
    study_lookup = (
        df_model[
            ["Study_idx", "Study_id", "State"]
        ]
        .drop_duplicates("Study_idx")
        .sort_values("Study_idx")
        .reset_index(drop=True)
    )

    study_performance = study_lookup.copy()

    study_performance["U_study"] = u_study_mean
    study_performance["Performance_multiplier"] = np.exp(u_study_mean)

    os.makedirs("results", exist_ok=True)
    csv_path1 = "results/site_performance2.csv"
    csv_path2 = "results/study_performance2.csv"
    site_performance.to_csv(csv_path1, index=False)
    study_performance.to_csv(csv_path2, index=False)
    
    print(f"Saved site CSV to: {csv_path1}")
    print(f"Saved study CSV to: {csv_path2}")

    self.site_performance = site_performance
    self.study_performance = study_performance

    return self.site_performance, self.study_performance

def excel_output(self):
    site_performance = self.site_performance
    study_performance = self.study_performance
    excel_path = "results/performance2.xlsx"

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        site_performance.to_excel(writer, sheet_name="Site_Performance", index=False)
        study_performance.to_excel(writer, sheet_name="Study_Performance", index=False)
    
    workbook = load_workbook(excel_path)
    site_ws = workbook["Site_Performance"]
    study_ws = workbook["Study_Performance"]


    site_row_count = len(site_performance) + 1
    study_row_count = len(study_performance) + 1

    color_rule = ColorScaleRule(
        start_type="min",
        start_color="F8696B",
        mid_type="percentile",
        mid_value=50,
        mid_color="FFEB84",
        end_type="max",
        end_color="63BE7B"
        )
    site_ws.conditional_formatting.add(f"D2:D{site_row_count}", color_rule)
    study_ws.conditional_formatting.add(f"D2:D{study_row_count}", color_rule)

    workbook.save(excel_path)
    print(f"Saved workbook to: {excel_path}")

    self.workbook = workbook

    return self.workbook

def png_output(self):
    
    site_performance = self.site_performance

    os.makedirs("results", exist_ok=True)
    png_path = "results/site_performance_heatmap.png"

    fig = px.scatter_geo(
        site_performance,
        lat= "Latitude",
        lon= "Longitude",
        color= "Performance_multiplier",
        size = "Enrollments",
        hover_data= {
            "Site_id": True,
            "Performance_multiplier": ":.2f",
            "Enrollments": True,
            "Latitude": False,
            "Longitude": False
        },
        scope= "usa",
        color_continuous_scale= "RdYlGn"
    )

    fig.write_image(
        png_path,
        width= 1600,
        height= 900
    )
    print(f"Saved PNG to: {png_path}")
    
    html_path = "results/interactive_heatmap.html"
    fig.write_html(html_path)

    self.site_performance = site_performance
    self.fig = fig

    return self.site_performance, self.fig