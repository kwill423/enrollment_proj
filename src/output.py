import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from openpyxl import load_workbook
from openpyxl.formatting.rule import ColorScaleRule

def compute_performance(self):
    
    print("Entering compute performance...")
    trace = self.trace
    df_model = self.df_model

    u_site_mean = trace.posterior["u_site"].mean(
        dim=("chain", "draw")
    ).values

    site_performance = pd.DataFrame({
        "Site_id": df_model.drop_duplicates("Site_idx")["Site_id"],
        "State": df_model.drop_duplicates("Site_idx")["State"],
        "U_site": u_site_mean,
        "Performance_multiplier": np.exp(u_site_mean)
    })
    site_performance = site_performance.sort_values("Performance_multiplier", ascending=False).reset_index(drop=True)
    
    
    u_study_mean = trace.posterior["u_study"].mean(dim=("chain", "draw")).values

    study_performance = pd.DataFrame({
        "Study_id": df_model.drop_duplicates("Study_idx")["Study_id"],
        "State": df_model.drop_duplicates("Study_idx")["State"],
        "U_study": u_study_mean,
        "Performance_multiplier": np.exp(u_study_mean)

    })

    os.makedirs("results", exist_ok=True)
    csv_path1 = "results/site_performance.csv"
    csv_path2 = "results/study_performance.csv"
    site_performance.to_csv(csv_path1, index=False)
    study_performance.to_csv(csv_path2, index=False)

    self.site_performance = site_performance
    self.study_performance = study_performance

    return self.site_performance, self.study_performance

def excel_output(self):
    site_performance = self.site_performance
    study_performance = self.study_performance
    excel_path = "results/performance.xlsx"

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
    study_performance = self.study_performance

    os.makedirs("results", exist_ok=True)
    png_path1 = "results/site_performance_heatmap.png"
    '''
    -------------------------
    PNG for Site Performance
    -------------------------
    '''
    fig_height_site = max(
        6,
        len(site_performance) * 0.3
    )

    fig_site, ax = plt.subplots(
        figsize=(6, fig_height_site)
    )

    heatmap_values = site_performance[
        ["Performance_multiplier"]
    ].values

    im = ax.imshow(
        heatmap_values,
        cmap="RdYlGn",
        aspect="auto"
    )

    ax.set_yticks(range(len(site_performance)))

    ax.set_yticklabels(
        site_performance["Site_id"],
        fontsize=8
    )

    ax.set_xticks([0])

    ax.set_xticklabels(
        ["Performance Multiplier"]
    )

    ax.set_title(
        "Site Performance Heatmap",
        fontsize=14
    )

    cbar = plt.colorbar(im)
    cbar.set_label(
        "Performance Multiplier"
    )

    plt.tight_layout()

    plt.savefig(
        png_path1,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved Site PNG heatmap to: {png_path1}")
    '''
    -------------------------
    PNG for Site Performance
    -------------------------
    '''
    png_path2 = "results/study_performance_heatmap.png"

    fig_height_study = max(
        6,
        len(study_performance) * 0.3
    )

    fig_study, ax = plt.subplots(
        figsize=(6, fig_height_study)
    )

    heatmap_values = study_performance[
        ["Performance_multiplier"]
    ].values

    im = ax.imshow(
        heatmap_values,
        cmap="RdYlGn",
        aspect="auto"
    )

    ax.set_yticks(range(len(study_performance)))

    ax.set_yticklabels(
        study_performance["Study_id"],
        fontsize=8
    )

    ax.set_xticks([0])

    ax.set_xticklabels(
        ["Performance Multiplier"]
    )

    ax.set_title(
        "Study Performance Heatmap",
        fontsize=14
    )

    cbar = plt.colorbar(im)
    cbar.set_label(
        "Performance Multiplier"
    )

    plt.tight_layout()

    plt.savefig(
        png_path2,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved Study PNG heatmap to: {png_path2}")


    self.fig_site = fig_site
    self.fig_study = fig_study

    return self.fig_site, self.fig_study
