import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from openpyxl import load_workbook
from openpyxl.formatting.rule import ColorScaleRule

def compute_performance(self):
    trace = self.trace
    df = self.df

    u_site_mean = trace.posterior["u_site"].mean(
        dim=("chain", "draw")
    ).values

    performance = pd.DataFrame({
        "site_id": df.drop_duplicates("site_idx")["site_id"],
        "state": df.drop_duplicates("site_idx")["state"],
        "u_site": u_site_mean,
        "performance_multiplier": np.exp(u_site_mean)
    })
    performance = performance.sort_values("performanc_multiplier", ascending=False).reset_index(drop=True)
    

    os.makedirs("results", exist_ok=True)
    csv_path = "results/site_performance.csv"
    performance.to_csv(csv_path, index=False)
    

    self.performance = performance

    return self.performance

def excel_output(self):
    performance = self.performance
    excel_path = "results/site_performance.xlsx"

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        performance.to_excel(writer, sheet_name="Performance", index=False)
    
    workbook = load_workbook(excel_path)
    worksheet = workbook["Performance"]

    row_count = len(performance) + 1

    color_rule = ColorScaleRule(
        start_type="min",
        start_color="F8696B",
        mid_type="percentile",
        mid_value=50,
        mid_color="FFEB84",
        end_type="max",
        end_color="663BE7B"
        )
    worksheet.conditional_formatting.add(f"D2:D{row_count}", color_rule)

    workbook.save(excel_path)
    print(f"Saved workbook to: {excel_path}")

    self.workbook = workbook

    return self.workbook

def png_output(self):
    
    performance = self.performance

    os.makedirs("results", exist_ok=True)
    png_path = "results/performance_heatmap.png"
    
    fig_height = max(
        6,
        len(performance) * 0.3
    )

    fig, ax = plt.subplots(
        figsize=(6, fig_height)
    )

    heatmap_values = performance[
        ["performance_multiplier"]
    ].values

    im = ax.imshow(
        heatmap_values,
        cmap="RdYlGn",
        aspect="auto"
    )

    ax.set_yticks(range(len(performance)))

    ax.set_yticklabels(
        performance["site_id"],
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
        png_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved PNG heatmap to: {png_path}")

    self.fig = fig

    return self.fig
