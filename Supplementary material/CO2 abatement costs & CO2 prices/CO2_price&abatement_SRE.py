from __future__ import annotations

from typing import cast
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Patch
import matplotlib.patches as mpatches

scenarios = ["REF", "DYN", "SIM", "SWE"]
years = [2030, 2035, 2040]
fuel_types = ["Coal", "Lignite", "Gas", "Other"]
fuel_colors = ["#A15015", "#F29E4C", "#DEB887", "#778899"]

cost_data_low: dict[tuple[str, int], list[float]] = {
    ("REF", 2030): [0.465, 0.106, 20.675, 2.431],
    ("REF", 2035): [0.234, 0.026, 12.862, 2.386],
    ("REF", 2040): [0.176, 0.000, 8.348, 0.017],
    ("DYN", 2030): [0.470, 0.107, 20.860, 2.452],
    ("DYN", 2035): [0.239, 0.000, 13.064, 2.412],
    ("DYN", 2040): [0.201, 0.000, 8.498, 0.017],
    ("SIM", 2030): [0.474, 0.106, 20.762, 2.443],
    ("SIM", 2035): [0.223, 0.026, 12.954, 2.397],
    ("SIM", 2040): [0.183, 0.000, 8.416, 0.017],
    ("SWE", 2030): [0.454, 0.108, 21.033, 2.470],
    ("SWE", 2035): [0.242, 0.000, 13.306, 2.456],
    ("SWE", 2040): [0.217, 0.000, 8.509, 0.016],
}
co2_low = pd.DataFrame(
    {"REF": [89.14, 87.57, 96.47],
     "DYN": [89.94, 88.74, 98.44],
     "SIM": [89.55, 88.09, 97.31],
     "SWE": [90.60, 90.38, 98.74]},
    index=years,
)
scenario_labels_low = [
    "Reference (without SRE)",
    "Low dynamic",
    "Low simultaneous",
    "Low sweeping",
]

cost_data_avg: dict[tuple[str, int], list[float]] = {
    ("REF", 2030): [0.465, 0.106, 20.675, 2.431],
    ("REF", 2035): [0.234, 0.026, 12.862, 2.386],
    ("REF", 2040): [0.176, 0.000, 8.348, 0.017],
    ("DYN", 2030): [0.480, 0.107, 20.873, 2.457],
    ("DYN", 2035): [0.236, 0.000, 13.135, 2.420],
    ("DYN", 2040): [0.198, 0.000, 8.470, 0.017],
    ("SIM", 2030): [0.484, 0.107, 20.818, 2.451],
    ("SIM", 2035): [0.223, 0.026, 13.023, 2.403],
    ("SIM", 2040): [0.172, 0.000, 8.388, 0.017],
    ("SWE", 2030): [0.458, 0.108, 21.182, 2.489],
    ("SWE", 2035): [0.283, 0.000, 13.967, 2.570],
    ("SWE", 2040): [0.225, 0.000, 8.782, 0.016],
}
co2_avg = pd.DataFrame(
    {"REF": [89.14, 87.57, 96.47],
     "DYN": [90.0393, 89.1681, 98.0869],
     "SIM": [89.82, 88.52, 96.87],
     "SWE": [91.25, 94.99, 101.91]},
    index=years,
)
scenario_labels_avg = [
    "Reference (without SRE)",
    "Average dynamic",
    "Average simultaneous",
    "Average sweeping",
]

cost_data_high: dict[tuple[str, int], list[float]] = {
    ("REF", 2030): [0.465, 0.106, 20.675, 2.431],
    ("REF", 2035): [0.234, 0.026, 12.862, 2.386],
    ("REF", 2040): [0.176, 0.000, 8.348, 0.017],
    ("DYN", 2030): [0.494, 0.107, 20.827, 2.455],
    ("DYN", 2035): [0.247, 0.000, 13.276, 2.455],
    ("DYN", 2040): [0.202, 0.000, 8.025, 0.020],
    ("SIM", 2030): [0.490, 0.107, 20.808, 2.451],
    ("SIM", 2035): [0.230, 0.000, 13.180, 2.435],
    ("SIM", 2040): [0.184, 0.000, 7.989, 0.020],
    ("SWE", 2030): [0.476, 0.074, 21.524, 2.530],
    ("SWE", 2035): [0.301, 0.000, 15.263, 2.779],
    ("SWE", 2040): [0.254, 0.000, 9.771, 0.017],
}
co2_high = pd.DataFrame(
    {"REF": [89.14, 87.57, 96.47],
     "DYN": [89.91, 90.23, 93.14],
     "SIM": [89.81, 89.48, 92.53],
     "SWE": [92.63, 103.59, 113.42]},
    index=years,
)
scenario_labels_high = [
    "Reference (without SRE)",
    "High dynamic",
    "High simultaneous",
    "High sweeping",
]

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 8,
    "axes.titlesize": 10,
    "axes.labelsize": 10,
    "axes.titleweight": "normal",
    "axes.labelweight": "normal",
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

def fmt_bar_label(v: float) -> str | None:
    r1 = round(float(v), 1)
    if abs(r1) < 1e-9:
        return None
    if abs(r1 - round(r1)) < 1e-9:
        return f"{int(round(r1))}"
    return f"{r1:.1f}"

def max_stack(cost_dict: dict[tuple[str, int], list[float]]) -> float:
    return max(sum(cost_dict[(s, y)]) for s in scenarios for y in years)

def set_closed_frame(ax: Axes) -> None:
    for side in ("left", "right", "top", "bottom"):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(0.8)

WIDTH = 0.42
GAP = 0.30
x_positions: list[float] = []
x_meta: list[tuple[int, str, int, float]] = []
for si, s in enumerate(scenarios):
    base = si * (len(years) + GAP)
    for yi, y in enumerate(years):
        x = base + yi
        x_positions.append(x)
        x_meta.append((si, s, y, x))
group_midpoints = [
    (x_positions[i * len(years)] + x_positions[i * len(years) + (len(years) - 1)]) / 2
    for i in range(len(scenarios))
]

def plot_row(
    ax: Axes,
    cost_dict: dict[tuple[str, int], list[float]],
    co2_df: pd.DataFrame,
    scenario_labels_row: list[str],
    ylim_top: float,
    show_years_label: bool,
) -> None:
    for _, s, y, x in x_meta:
        bottom = 0.0
        vals = cost_dict[(s, y)]
        for fi, v in enumerate(vals):
            ax.bar(
                x, v, width=WIDTH, bottom=bottom,
                color=fuel_colors[fi], edgecolor="none", linewidth=0
            )
            txt = fmt_bar_label(v)
            if txt is not None:
                center_y = bottom + v / 2
                center_y = max(center_y, 0.5)
                if fuel_types[fi] == "Lignite":
                    text_x = x + 0.28
                    tick_start = x + WIDTH / 2
                    tick_end = text_x - 0.02
                    ax.text(
                        text_x, center_y + 0.05, txt,
                        ha="left", va="center", fontsize=8, fontweight="bold"
                    )
                    ax.plot(
                        [tick_start, tick_end],
                        [center_y, center_y + 0.05],
                        color="black", linewidth=0.5
                    )
                else:
                    ax.text(
                        x, center_y, txt,
                        ha="center", va="center", fontsize=8, fontweight="bold"
                    )
            bottom += v

    y_scen = 1.06
    y_co2 = 1.01
    for si, scen_label in enumerate(scenario_labels_row):
        x_mid = group_midpoints[si]
        ax.text(
            x_mid, y_scen, scen_label,
            transform=ax.get_xaxis_transform(),
            ha="center", va="bottom",
            fontsize=8,
            fontweight="normal",
            clip_on=False
        )
        for yi, y in enumerate(years):
            x = (si * (len(years) + GAP)) + yi
            co2_val = co2_df.loc[y, scenarios[si]] if (y in co2_df.index and scenarios[si] in co2_df.columns) else None
            if pd.notna(co2_val):
                co2_price = float(cast(float, co2_val))
                ax.text(
                    x, y_co2, f"{co2_price:.2f} €/t",
                    transform=ax.get_xaxis_transform(),
                    ha="center", va="top",
                    fontsize=8,
                    fontweight="bold",
                    bbox=dict(
                        facecolor="white",
                        alpha=0.95,
                        edgecolor="green",
                        boxstyle="square",
                    ),
                    clip_on=False
                )

    YEAR_Y = -0.025
    for _, _, y, x in x_meta:
        ax.text(
            x, YEAR_Y, f"{y}",
            transform=ax.get_xaxis_transform(),
            ha="center", va="top",
            fontsize=8,
            clip_on=False
        )

    if show_years_label:
        ax.text(
            0.5, -0.10, "Year",
            transform=ax.transAxes,
            ha="center", va="top",
            fontsize=9,
            fontweight="normal",
            clip_on=False
        )

    ax.set_ylabel("Costs (bn€)")
    ax.set_xticks(x_positions)
    ax.set_xticklabels([])
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    set_closed_frame(ax)
    ax.set_ylim(0, ylim_top)

max_all = max(
    max_stack(cost_data_low),
    max_stack(cost_data_avg),
    max_stack(cost_data_high)
)
ylim_top = max_all * 1.12

fig = plt.figure(figsize=(18.0, 10.8))
gs = fig.add_gridspec(3, 1, hspace=0.34)
ax_low = fig.add_subplot(gs[0, 0])
ax_avg = fig.add_subplot(gs[1, 0], sharex=ax_low)
ax_high = fig.add_subplot(gs[2, 0], sharex=ax_low)

for ax in (ax_low, ax_avg, ax_high):
    ax.patch.set_visible(False)

fig.patch.set_facecolor("white")
fig.patch.set_alpha(1.0)
fig.subplots_adjust(left=0.06, right=0.84, bottom=0.12, top=0.94)

plot_row(ax_low, cost_data_low, co2_low, scenario_labels_low, ylim_top, show_years_label=True)
plot_row(ax_avg, cost_data_avg, co2_avg, scenario_labels_avg, ylim_top, show_years_label=True)
plot_row(ax_high, cost_data_high, co2_high, scenario_labels_high, ylim_top, show_years_label=True)

fuel_handles = [
    Patch(facecolor=fuel_colors[i], edgecolor="none", label=fuel_types[i])
    for i in range(len(fuel_types))
][::-1]
co2_handle = mpatches.Patch(
    facecolor="white",
    edgecolor="green",
    label="CO$_2$ price (in each\nscenario year)",
)

fig.legend(
    handles=fuel_handles + [co2_handle],
    loc="center left",
    bbox_to_anchor=(0.845, 0.50),
    frameon=False,
    fontsize=8
)

plt.show()