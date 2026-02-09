from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
from matplotlib.ticker import FuncFormatter, MultipleLocator

years = [2030, 2035, 2040, 2045, 2050]
scenarios = ["REF", "DYN", "SIM", "SWE"]
scenario_labels = [
    "Reference (without SRE)",
    "Low-dynamic",
    "Low-simultaneous",
    "Low-sweeping",
]
technologies = [
    "Residential (rooftop) PV",
    "Utility-scale PV",
    "Onshore wind power",
    "Offshore wind power",
    "Biomass",
    "Battery storage",
    "Hydrogen",
    "Electrolyzer",
    "Pumped hydro storage",
    "Hydropower",
    "Conventional",
    "Other",
]
colors = [
    "#C6B866",
    "#FEE484",
    "#4FCFAD",
    "#77BACC",
    "#F3B1BC",
    "#57C35E",
    "#D5ACFE",
    "#CA41B1",
    "#5555ffff",
    "#C1EAFE",
    "#E47B38",
    "#C7C7C7",
]

absolute_data = {
    "REF": [
        [389, 628, 387, 169, 13, 23, 140, 89, 73, 176, 322, 24],
        [515, 805, 498, 293, 13, 44, 185, 195, 73, 176, 306, 22],
        [602, 920, 584, 417, 12, 96, 240, 273, 73, 176, 271, 7],
        [684, 1036, 736, 476, 9, 165, 282, 355, 73, 176, 227, 4],
        [747, 1100, 794, 533, 7, 240, 311, 405, 73, 176, 169, 2],
    ],
    "DYN": [
        [397, 644, 388, 169, 13, 23, 141, 91, 73, 176, 322, 24],
        [528, 830, 500, 294, 13, 46, 188, 197, 73, 176, 306, 22],
        [614, 945, 591, 417, 12, 102, 243, 274, 73, 176, 271, 7],
        [703, 1062, 732, 475, 9, 174, 288, 350, 73, 176, 227, 4],
        [774, 1134, 796, 533, 7, 256, 318, 403, 73, 176, 169, 2],
    ],
    "SIM": [
        [397, 644, 387, 169, 13, 22, 141, 92, 73, 176, 322, 24],
        [527, 829, 498, 293, 13, 44, 187, 197, 73, 176, 306, 22],
        [613, 943, 583, 417, 12, 101, 241, 272, 73, 176, 271, 7],
        [701, 1063, 729, 475, 9, 172, 286, 352, 73, 176, 227, 4],
        [771, 1129, 792, 533, 7, 250, 317, 404, 73, 176, 169, 2],
    ],
    "SWE": [
        [391, 632, 389, 169, 13, 24, 141, 89, 73, 176, 322, 24],
        [522, 815, 506, 294, 13, 48, 186, 198, 73, 176, 306, 22],
        [609, 932, 597, 417, 12, 103, 241, 275, 73, 176, 271, 7],
        [690, 1047, 745, 478, 9, 173, 285, 357, 73, 176, 227, 4],
        [760, 1116, 803, 537, 7, 254, 311, 406, 73, 176, 169, 2],
    ],
}

difference_data = {
    "DYN": [
        [8, 15, 1, 0, 0, 0, 2, 2, 0, 0, 0, 0],
        [12, 24, 2, 1, 0, 2, 2, 2, 0, 0, 0, 0],
        [12, 25, 7, 0, 0, 6, 3, 1, 0, 0, 0, 0],
        [19, 26, -5, -1, 0, 9, 6, -5, 0, 0, 0, 0],
        [27, 34, 2, 0, 0, 16, 7, -2, 0, 0, 0, 0],
    ],
    "SIM": [
        [8, 16, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0],
        [12, 24, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0],
        [11, 23, -1, 0, 0, 5, 0, 0, 0, 0, 0, 0],
        [18, 27, -7, -1, 0, 7, 4, -3, 0, 0, 0, 0],
        [23, 29, -2, -1, 0, 10, 6, -1, 0, 0, 0, 0],
    ],
    "SWE": [
        [2, 3, 2, 0, 0, 1, 1, -1, 0, 0, 0, 0],
        [6, 10, 8, 1, 0, 4, 1, 3, 0, 0, 0, 0],
        [7, 12, 13, 0, 0, 7, 1, 3, 0, 0, 0, 0],
        [7, 11, 9, 3, 0, 7, 3, 2, 0, 0, 0, 0],
        [13, 17, 10, 3, 0, 14, -1, 1, 0, 0, 0, 0],
    ],
}

plt.rcParams.update(
    {
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
    }
)


def yfmt(x, _pos):
    return f"{x:,.0f}"


fig = plt.figure(figsize=(10.8, 7.2))
gs = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.06)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

width = 0.70
x_positions: list[float] = []
current = 0.0

ax1.axhline(0, color="black", linewidth=0.8, linestyle="-")

for scenario in scenarios:
    for idx, year in enumerate(years):
        x_positions.append(current)
        bottom = 0.0
        label_toggle_abs = False

        for tech_idx, tech in enumerate(technologies):
            value = float(absolute_data[scenario][idx][tech_idx])
            c = colors[tech_idx]
            ax1.bar(current, value, width=width, bottom=bottom, color=c, edgecolor="none", linewidth=0)

            if value > 0:
                center_y = bottom + value / 2.0
                if tech in {"Hydrogen", "Battery storage", "Electrolyzer"}:
                    ax1.text(current, center_y, f"{int(value)}", ha="center", va="center", fontsize=5, fontweight="bold")
                elif tech == "Biomass":
                    if year in {2030, 2035}:
                        offset = 0.35 if label_toggle_abs else -0.35
                        ha = "left" if label_toggle_abs else "right"
                        ax1.text(current + offset, center_y, f"{int(value)}", ha=ha, va="center", fontsize=5, fontweight="bold")
                        ax1.plot(
                            [current + (width / 2 if label_toggle_abs else -width / 2), current + (0.3 if label_toggle_abs else -0.3)],
                            [center_y, center_y],
                            color="black",
                            linewidth=0.5,
                        )
                        label_toggle_abs = not label_toggle_abs
                    else:
                        ax1.text(current, center_y, f"{int(value)}", ha="center", va="center", fontsize=5, fontweight="bold")
                else:
                    if (tech == "Other" and value >= 7) or (tech in {"Pumped hydro storage"}) or (tech != "Other" and value > 150):
                        ax1.text(current, center_y, f"{int(value)}", ha="center", va="center", fontsize=5, fontweight="bold")
                    elif tech != "Other":
                        offset = 0.35 if label_toggle_abs else -0.35
                        ha = "left" if label_toggle_abs else "right"
                        ax1.text(current + offset, center_y, f"{int(value)}", ha=ha, va="center", fontsize=5, fontweight="bold")
                        ax1.plot(
                            [current + (width / 2 if label_toggle_abs else -width / 2), current + (0.3 if label_toggle_abs else -0.3)],
                            [center_y, center_y],
                            color="black",
                            linewidth=0.5,
                        )
                        label_toggle_abs = not label_toggle_abs
            bottom += value
        current += 1.0
    current += 1.5

scenario_texts = []
nY = len(years)
scenario_midpoints = [(x_positions[i * nY] + x_positions[i * nY + (nY - 1)]) / 2.0 for i in range(len(scenarios))]
for i, mid in enumerate(scenario_midpoints):
    t = ax1.text(
        mid,
        1.02,
        scenario_labels[i],
        transform=ax1.get_xaxis_transform(),
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="normal",
        clip_on=False,
    )
    scenario_texts.append(t)

ax1.set_ylabel("Installed capacity (GW)")
ax1.set_ylim(0, 5000)
ax1.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)
ax1.set_xticks([])
ticks = ax1.get_yticks()
ax1.set_yticks([t for t in ticks if t != 0])
ax1.spines["bottom"].set_visible(False)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.grid(axis="y", linestyle="--", alpha=0.5)
ax1.axhline(color="black", alpha=0.8, linestyle="-", linewidth=0.8)
ax1.ticklabel_format(axis="y", style="plain", useOffset=False)
ax1.yaxis.set_major_formatter(FuncFormatter(yfmt))
ax1.yaxis.set_major_locator(MultipleLocator(1000))

current = 0.0
for scenario in scenarios:
    if scenario == "REF":
        for _ in range(len(years)):
            ax2.hlines(y=0, xmin=current - width / 2, xmax=current + width / 2, color="white", linewidth=1)
            current += 1.0
        current += 1.5
        continue

    for idx, _year in enumerate(years):
        pos_bottom = 0.0
        neg_bottom = 0.0
        for tech_idx, _tech in enumerate(technologies):
            diff_value = float(difference_data[scenario][idx][tech_idx])
            c = colors[tech_idx]
            if diff_value > 2:
                ax2.bar(current, diff_value, width=width, bottom=pos_bottom, color=c, edgecolor="none", linewidth=0)
                center_y = pos_bottom + diff_value / 2.0
                ax2.text(current, center_y, f"+{int(diff_value)}", ha="center", va="center", fontsize=5, fontweight="bold", color="black")
                pos_bottom += diff_value
            elif diff_value < -1:
                ax2.bar(current, diff_value, width=width, bottom=neg_bottom, color=c, edgecolor="none", linewidth=0)
                center_y = neg_bottom + diff_value / 2.0
                ax2.text(current, center_y, f"{int(diff_value)}", ha="center", va="center", fontsize=5, fontweight="bold", color="black")
                neg_bottom += diff_value
        current += 1.0
    current += 1.5

ax2.set_xticks(x_positions)
ax2.set_xticklabels([str(year) for year in years] * len(scenarios))
ax2.set_xlabel("Year")
ax2.set_ylabel("Difference to\nthe reference —\ncapacity [GW]")
ax2.axhline(color="black", linewidth=0.6, linestyle="-")
ax2.set_ylim(-15, 85)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(axis="y", linestyle="--", alpha=0.5)
ax2.ticklabel_format(axis="y", style="plain", useOffset=False)
ax2.yaxis.set_major_formatter(FuncFormatter(yfmt))
ax2.yaxis.set_major_locator(MultipleLocator(20))

handles = [mpatches.Patch(color=colors[i], label=technologies[i]) for i in range(len(technologies))][::-1]
fig.subplots_adjust(left=0.08, right=0.83, top=0.93, bottom=0.10)
leg = ax1.legend(handles=handles, loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False, fontsize=8)

try:
    out_dir = Path(__file__).resolve().parent
    base = Path(__file__).stem
except NameError:
    out_dir = Path.cwd()
    base = "extended_data_figure"

pdf_path = out_dir / f"{base}.pdf"
tmp_svg_path = out_dir / f"_tmp_{base}.svg"
emf_path = out_dir / f"{base}.emf"
tif_path = out_dir / f"{base}.tif"

fig.canvas.draw()
extra_artists: list[Artist] = [cast(Artist, leg)]
for ax in fig.axes:
    extra_artists.extend(cast(list[Artist], list(ax.texts)))
extra_artists.extend(cast(list[Artist], list(fig.texts)))

SAVE_KW: dict[str, Any] = {
    "bbox_inches": "tight",
    "bbox_extra_artists": tuple(extra_artists),
    "pad_inches": 0.05,
    "transparent": False,
}

plt.show()