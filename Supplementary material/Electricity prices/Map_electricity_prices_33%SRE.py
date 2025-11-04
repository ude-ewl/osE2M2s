import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm, TwoSlopeNorm
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
    "Albania": -1.05,
    "Austria": 0.53,
    "Bosnia & Herzegovina": -1.10,
    "Belgium": 0.89,
    "Bulgaria": -0.98,
    "Switzerland": -0.46,
    "Czech Republic": 0.44,
    "Germany": 0.15,
    "Denmark": 0.26,
    "Estonia": 0.61,
    "Spain": 0.04,
    "Finland": 0.68,
    "France": -0.81,
    "Greece": -1.07,
    "Croatia": -0.97,
    "Hungary": -1.03,
    "Ireland": -0.34,
    "Italy": -1.85,
    "Lithuania": 0.44,
    "Luxembourg": 0.04,
    "Latvia": 0.49,
    "Montenegro": -1.14,
    "The former Yugoslav Republic of Macedonia": -1.03,
    "Netherlands": 0.11,
    "Norway": 0.51,
    "Poland": 0.15,
    "Portugal": 0.42,
    "Romania": -1.11,
    "Serbia": -1.02,
    "Sweden": 0.62,
    "Slovenia": -1.18,
    "Slovakia": 0.17,
    "U.K. of Great Britain and Northern Ireland": 0.56
}

diff_sim = {
    "Albania": -1.28,
    "Austria": 0.40,
    "Bosnia & Herzegovina": -1.33,
    "Belgium": 0.75,
    "Bulgaria": -1.20,
    "Switzerland": -0.67,
    "Czech Republic": 0.35,
    "Germany": 0.00,
    "Denmark": 0.06,
    "Estonia": 0.50,
    "Spain": -0.05,
    "Finland": 0.56,
    "France": -0.91,
    "Greece": -1.20,
    "Croatia": -1.19,
    "Hungary": -1.15,
    "Ireland": -0.26,
    "Italy": -1.97,
    "Lithuania": 0.33,
    "Luxembourg": -0.12,
    "Latvia": 0.40,
    "Montenegro": -1.37,
    "The former Yugoslav Republic of Macedonia": -1.27,
    "Netherlands": 0.10,
    "Norway": 0.39,
    "Poland": 0.06,
    "Portugal": 0.41,
    "Romania": -1.23,
    "Serbia": -1.25,
    "Sweden": 0.51,
    "Slovenia": -1.32,
    "Slovakia": 0.11,
    "U.K. of Great Britain and Northern Ireland": 0.44
}

diff_swe = {
    "Albania": 3.18,
    "Austria": 2.74,
    "Bosnia & Herzegovina": 3.15,
    "Belgium": 3.71,
    "Bulgaria": 3.11,
    "Switzerland": 3.20,
    "Czech Republic": 3.83,
    "Germany": 4.44,
    "Denmark": 2.38,
    "Estonia": 0.74,
    "Spain": 2.24,
    "Finland": 0.85,
    "France": 2.55,
    "Greece": 2.59,
    "Croatia": 2.78,
    "Hungary": 2.59,
    "Ireland": 3.28,
    "Italy": 3.51,
    "Lithuania": 0.45,
    "Luxembourg": 4.35,
    "Latvia": 0.83,
    "Montenegro": 3.21,
    "The former Yugoslav Republic of Macedonia": 3.04,
    "Netherlands": 4.25,
    "Norway": -0.15,
    "Poland": 2.16,
    "Portugal": 2.35,
    "Romania": 2.37,
    "Serbia": 3.10,
    "Sweden": 0.65,
    "Slovenia": 2.89,
    "Slovakia": 3.85,
    "U.K. of Great Britain and Northern Ireland": 3.50
}

scenarios = [
    ("High-dyn — difference to the reference", diff_dyn),
    ("High-sim — difference to the reference", diff_sim),
    ("High-swe — difference to the reference", diff_swe)
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
   "High-dyn — difference to the reference",
   "High-sim — difference to the reference",
   "High-swe — difference to the reference"
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