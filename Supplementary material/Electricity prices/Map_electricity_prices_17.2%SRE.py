import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm, TwoSlopeNorm
import os
from matplotlib.colors import to_hex

# Adjust this path to point to your world-administrative-boundaries.shp file
shapefile_path = r"C:\...\world-administrative-boundaries.shp"
world = gpd.read_file(shapefile_path)

ref_00 = {
    "Albania": 66.74,
    "Austria": 62.77,
    "Bosnia & Herzegovina": 67.71,
    "Belgium": 69.33,
    "Bulgaria": 66.84,
    "Switzerland": 65.32,
    "Czech Republic": 68.61,
    "Germany": 67.94,
    "Denmark": 61.73,
    "Estonia": 55.62,
    "Spain": 56.08,
    "Finland": 55.93,
    "France": 61.41,
    "Greece": 64.74,
    "Croatia": 67.16,
    "Hungary": 66.88,
    "Ireland": 69.58,
    "Italy": 66.67,
    "Lithuania": 55.06,
    "Luxembourg": 68.66,
    "Latvia": 55.74,
    "Montenegro": 67.11,
    "The former Yugoslav Republic of Macedonia": 66.91,
    "Netherlands": 68.34,
    "Norway": 57.57,
    "Poland": 67.28,
    "Portugal": 53.98,
    "Romania": 66.87,
    "Serbia": 67.51,
    "Sweden": 55.48,
    "Slovenia": 66.79,
    "Slovakia": 70.43,
    "U.K. of Great Britain and Northern Ireland": 66.10
}

diff_dyn = {
    "Albania": 0.52,
    "Austria": 0.69,
    "Bosnia & Herzegovina": 0.49,
    "Belgium": 0.76,
    "Bulgaria": 0.47,
    "Switzerland": 0.33,
    "Czech Republic": 0.64,
    "Germany": 0.73,
    "Denmark": 0.32,
    "Estonia": 0.24,
    "Spain": 0.22,
    "Finland": 0.25,
    "France": 0.06,
    "Greece": 0.29,
    "Croatia": 0.55,
    "Hungary": 0.40,
    "Ireland": 0.28,
    "Italy": 0.31,
    "Lithuania": 0.12,
    "Luxembourg": 0.67,
    "Latvia": 0.17,
    "Montenegro": 0.52,
    "The former Yugoslav Republic of Macedonia": 0.43,
    "Netherlands": 0.52,
    "Norway": 0.19,
    "Poland": 0.46,
    "Portugal": 0.40,
    "Romania": 0.30,
    "Serbia": 0.49,
    "Sweden": 0.25,
    "Slovenia": 0.62,
    "Slovakia": 0.58,
    "U.K. of Great Britain and Northern Ireland": 0.44
}

diff_sim = {
    "Albania": 0.34,
    "Austria": 0.47,
    "Bosnia & Herzegovina": 0.42,
    "Belgium": 0.53,
    "Bulgaria": 0.38,
    "Switzerland": 0.20,
    "Czech Republic": 0.35,
    "Germany": 0.40,
    "Denmark": 0.09,
    "Estonia": 0.17,
    "Spain": 0.02,
    "Finland": 0.20,
    "France": -0.02,
    "Greece": 0.17,
    "Croatia": 0.45,
    "Hungary": 0.33,
    "Ireland": 0.02,
    "Italy": 0.13,
    "Lithuania": 0.05,
    "Luxembourg": 0.34,
    "Latvia": 0.09,
    "Montenegro": 0.39,
    "The former Yugoslav Republic of Macedonia": 0.26,
    "Netherlands": 0.23,
    "Norway": 0.14,
    "Poland": 0.20,
    "Portugal": 0.25,
    "Romania": 0.25,
    "Serbia": 0.40,
    "Sweden": 0.19,
    "Slovenia": 0.48,
    "Slovakia": 0.25,
    "U.K. of Great Britain and Northern Ireland": 0.16
}

diff_swe = {
    "Albania": 1.08,
    "Austria": 0.96,
    "Bosnia & Herzegovina": 1.00,
    "Belgium": 1.30,
    "Bulgaria": 0.94,
    "Switzerland": 1.22,
    "Czech Republic": 1.19,
    "Germany": 1.55,
    "Denmark": 0.94,
    "Estonia": 0.22,
    "Spain": 0.69,
    "Finland": 0.20,
    "France": 0.83,
    "Greece": 0.79,
    "Croatia": 0.96,
    "Hungary": 0.85,
    "Ireland": 1.41,
    "Italy": 1.32,
    "Lithuania": 0.15,
    "Luxembourg": 1.50,
    "Latvia": 0.21,
    "Montenegro": 1.10,
    "The former Yugoslav Republic of Macedonia": 1.02,
    "Netherlands": 1.48,
    "Norway": -0.13,
    "Poland": 0.90,
    "Portugal": 0.86,
    "Romania": 0.67,
    "Serbia": 0.92,
    "Sweden": 0.28,
    "Slovenia": 1.03,
    "Slovakia": 1.64,
    "U.K. of Great Britain and Northern Ireland": 1.48
}

scenarios = [
    ("Avg-dyn — difference to the reference", diff_dyn),
    ("Avg-sim — difference to the reference", diff_sim),
    ("Avg-swe — difference to the reference", diff_swe)
]

all_diff_vals = np.concatenate([list(d.values()) for _, d in scenarios])
vmin, vmax = np.floor(all_diff_vals.min()), np.ceil(all_diff_vals.max())
step = 1.0
bounds = np.arange(vmin, vmax + step, step)

cmap = LinearSegmentedColormap.from_list(
    "green-yellow-red",
    ["#2ca25f", "#ffffbf", "#d73027"],
    N=256
)

norm_grad = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

def plot_diff_map(ax, data, title):
    xlim, ylim = (-11, 35), (34, 72)

    if title == "Reference (without SRE)":
        world["ref"] = world["name"].map(data)
        subset = world[world["ref"].notnull()].copy()
        
        world.plot(ax=ax, color="#dddddd", edgecolor="black", linewidth=0.5)

        for _, row in subset.iterrows():
            country_name = row['name']
            x_pos = row.geometry.centroid.x
            y_pos = row.geometry.centroid.y
            
            if country_name == "Norway":
                x_pos = 9.8
                y_pos = 61.5
            elif country_name == "Sweden":
                x_pos = 15.0
                y_pos = 61.0
                
            ax.text(x_pos, y_pos,
                    f"{row['ref']:.1f}",
                    fontsize=8, ha='center', va='center',
                    bbox=dict(facecolor='white', alpha=0.5,
                             edgecolor='none', boxstyle='round,pad=0.1'))

        legend_intervals = sorted(zip(bounds[:-1], bounds[1:]), key=lambda t: t[0])
        cols = 2
        rows = int(np.ceil(len(legend_intervals) / cols))

        start_x, start_y = 0.01, 0.98
        box_w, box_h = 0.06, 0.04
        dx, dy = 0.18, 0.06

        pad_x = pad_y = 0.006
        rect_x = 0.003
        rect_y = start_y - (rows - 1) * dy - box_h - pad_y
        
        rect_w = (cols - 1) * dx + box_w + 0.10 + 2 * pad_x
        rect_h = rows * dy - (dy - box_h) + 2 * pad_y
        ax.add_patch(mpatches.Rectangle(
            (rect_x, rect_y), rect_w, rect_h,
            transform=ax.transAxes,
            facecolor="none", edgecolor="#BFBFBF", linewidth=1.0))

        def format_bound(bound):
            return f"{int(bound)}" if bound == 0 else f"{bound:+.0f}"

        for i, (lo, hi) in enumerate(legend_intervals):
                r, c = i % rows, i // rows
                x_left = start_x + c * dx
                y_top  = start_y - r * dy
                y_low  = y_top - box_h

                ax.add_patch(mpatches.Rectangle(
                    (x_left, y_low), box_w, box_h,
                    transform=ax.transAxes,
                    facecolor=cmap(norm_grad((lo + hi) / 2)),
                    edgecolor="none", linewidth=0.0))

                ax.text(
                    x_left + box_w + 0.003,
                    y_low + box_h / 2,
                    f"{format_bound(lo)} to {format_bound(hi)}",
                    transform=ax.transAxes,
                    fontsize=10,
                    ha="left", va="center"
                )

    else:
        world["diff"] = world["name"].map(data)
        subset = (
            world[world["diff"].notnull()]  
            .copy()
            .reset_index(drop=True)         
        )

        def get_color(val):
            if val == 0:
                return "#dddddd"              
            return to_hex(cmap(norm_grad(val)))  

        colors = [get_color(v) for v in subset["diff"]]

        subset.plot(
            ax=ax, color=colors,
            edgecolor="black", linewidth=0.5
        )

        world[world["diff"].isnull()].plot(
            ax=ax, color="lightgrey", edgecolor="white", linewidth=0.3
        )

        for _, row in subset.iterrows():
            country_name = row["name"]
            x_pos = row.geometry.centroid.x
            y_pos = row.geometry.centroid.y

            if country_name == "Norway":
                x_pos, y_pos = 9.8, 61.5
            elif country_name == "Sweden":
                x_pos, y_pos = 15.0, 61.0

            ax.text(
                x_pos, y_pos,
                f"{row['diff']:+.2f}",
                fontsize=8, ha="center", va="center",
                bbox=dict(
                    facecolor="white", alpha=0.5,
                    edgecolor="none", boxstyle="round,pad=0.1"
                )
            )

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("auto")
    ax.axis("off")

fig, axes = plt.subplots(2, 2, figsize=(13.2, 10))
axes = axes.flatten()

fig.subplots_adjust(
    left=0.03, right=0.97,
    top=0.96, bottom=0.10, 
    wspace=0.02, hspace=0.05
)

plot_diff_map(axes[0], ref_00, "Reference (without SRE)")
for ax, (t, d) in zip(axes[1:], scenarios):
    plot_diff_map(ax, d, "")

titles = [
   "Reference (without SRE)",
   "Avg-dyn — difference to the reference",
   "Avg-sim — difference to the reference",
   "Avg-swe — difference to the reference"
]

fig.subplots_adjust(hspace=0.12)

for ax, title in zip(axes, titles):
    bbox = ax.get_position()
    x = (bbox.x0 + bbox.x1) / 2
    y = bbox.y1 - 0.0005
    fig.text(x, y, title,
             ha="center", va="bottom",
             fontsize=14, fontweight="bold")

plt.show()