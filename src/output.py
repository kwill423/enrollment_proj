import pandas as pd
import numpy as np
import kaleido
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.formatting.rule import ColorScaleRule
import os
import plotly.express as px

def compute_performance(self, csv_path1= "results/site_performance.csv", csv_path2= "results/study_performance.csv" ):
    
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
            ["Study_idx", "Study_id"]
        ]
        .drop_duplicates("Study_idx")
        .sort_values("Study_idx")
        .reset_index(drop=True)
    )

    study_performance = study_lookup.copy()

    study_performance["U_study"] = u_study_mean
    study_performance["Performance_multiplier"] = np.exp(u_study_mean)

    os.makedirs("results", exist_ok=True)
    site_performance.to_csv(csv_path1, index=False)
    study_performance.to_csv(csv_path2, index=False)
    
    print(f"Saved site CSV to: {csv_path1}")
    print(f"Saved study CSV to: {csv_path2}")

    self.site_performance = site_performance
    self.study_performance = study_performance

    return self.site_performance, self.study_performance

def excel_output(self, excel_path= "results/performance.xlsx"):

    site_performance = self.site_performance
    study_performance = self.study_performance

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
    site_ws.conditional_formatting.add(f"H2:H{site_row_count}", color_rule)
    study_ws.conditional_formatting.add(f"D2:D{study_row_count}", color_rule)

    workbook.save(excel_path)
    print(f"Saved workbook to: {excel_path}")

    self.workbook = workbook

    return self.workbook

def png_output(self, html_path= "results/interactive_heatmap.html"):
    
    site_performance = self.site_performance

    os.makedirs("results", exist_ok=True)

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
    
    fig.update_layout(
        title={
            "text": "Site Enrollment Performance Across the US",
            "x": 0.5,
            "xanchor": "center"
        }
    )

    fig.update_layout(
        coloraxis_colorbar= dict(
            title= "Performance",
            tickvals= [0.75, 1.0, 1.25],
            ticktext= [
                "Underperforming (< 0.75)",
                "As Expected (1.0)",
                "Overperforming (> 1.25)"
            ]
        )
    )

    missing_cords = site_performance[
        site_performance["Latitude"].isna() |
        site_performance["Longitude"].isna()
    ]

    if len(missing_cords) > 0:
        omitted_sites = ",".join(
            missing_cords["Site_id"].astype(str).tolist()
        )
        caption = (f"Sites not shown on  map due to missing zip codes:({omitted_sites})")
    else:
        caption = "All sites contained zip codes and are included in the map."

    fig.add_annotation(
        text = caption,
        xref= "paper",
        yref= "paper",
        x= 0,
        y= -0.12,
        showarrow= False,
        align= "left",
        font= dict(size= 12)
    )    

    fig.write_html(html_path)
    print(f"Saved interactive heatmap to: {html_path}")

    self.site_performance = site_performance
    self.fig = fig

    return self.site_performance, self.fig