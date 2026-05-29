from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from pathlib import Path
from typing import cast
from matplotlib.collections import PolyCollection

CSV_FILE = Path(r"C:\Users\delic\E2M2s-discounting\Supplementary material\Electricity price\el_prices_disc.csv")

if not CSV_FILE.exists():
    CSV_FILE = Path("/mnt/user-data/uploads/el_prices_disc.csv")

SCENARIOS = [
    ("exp_baseline", "Exponential baseline", "#7B4A8F"),
    ("hyp_upfront", "Hyperbolic upfront", "#6B5B4A"),
    ("hyp_feedin", "Hyperbolic feed-in tariff", "#4A6B8F"),
]

YEARS = [2030, 2035, 2040, 2045, 2050]

def load_data(file: Path):
    df = pd.read_csv(file)
    df.columns = [c.strip().lstrip("\ufeff") for c in df.columns]
    data = {y: [[] for _ in SCENARIOS] for y in YEARS}
    for y in YEARS:
        for i, (key, _, _) in enumerate(SCENARIOS):
            mask = (df["scenario"] == key) & (df["simyear"] == y)
            vals = df.loc[mask, "value"].dropna().to_numpy()
            data[y][i] = vals.tolist()
    return data

DATA = load_data(CSV_FILE)

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 8,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 7,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8,
    "xtick.major.size": 3, "ytick.major.size": 3,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "pdf.fonttype": 42, "ps.fonttype": 42,
})

fig, ax = plt.subplots(figsize=(15, 6.5), facecolor="white")

group_gap = 3.0
box_gap = 0.8
centers = [1 + i * group_gap for i in range(len(YEARS))]

def fmt(v):
    return f"{v:.2f}"

def lighten_color(color, amount=0.70):
    rgb = np.array(mcolors.to_rgb(color))
    white = np.array([1.0, 1.0, 1.0])
    return tuple((1 - amount) * rgb + amount * white)

for ci, year in enumerate(YEARS):
    center = centers[ci]
    offsets = [-box_gap, 0.0, +box_gap]

    for (sidx, (key, label, color)), off in zip(enumerate(SCENARIOS), offsets):
        pos = center + off
        values = DATA.get(year, [[], [], []])[sidx]
        if not values:
            continue

        vp = ax.violinplot(
            [values],
            positions=[pos],
            widths=0.95,
            showmeans=False,
            showextrema=False,
            showmedians=False,
            points=1500,
            bw_method=0.25,
        )

        bodies = cast(list[PolyCollection], vp["bodies"])

        for body in bodies:
            body.set_facecolor(color)
            body.set_edgecolor("none")
            body.set_alpha(0.55)
            body.set_linewidth(0.0)
            body.set_antialiased(True)
            body.set_zorder(0.4)

        bp = ax.boxplot(
            [values],
            positions=[pos],
            widths=0.7,
            patch_artist=True,
            showmeans=True,
            showfliers=False,
            boxprops=dict(linewidth=0.9, color="black"),
            whiskerprops=dict(linewidth=0.9, color="black"),
            capprops=dict(linewidth=0.9, color="black"),
            medianprops=dict(linewidth=1.3, color="black"),
            meanprops=dict(marker="x", markersize=6, markeredgecolor="black", markerfacecolor="black"),
        )

        box_face = lighten_color(color, amount=0.65)
        for patch in bp["boxes"]:
            patch.set_facecolor(box_face)
            patch.set_edgecolor("black")
            patch.set_zorder(2)

        for i in range(0, len(bp["whiskers"]), 2):
            lw = bp["whiskers"][i]
            uw = bp["whiskers"][i + 1]
            x_lw, y_lw = lw.get_xdata()[1], lw.get_ydata()[1]
            x_uw, y_uw = uw.get_xdata()[1], uw.get_ydata()[1]
            ax.text(x_lw, y_lw - 1.2, fmt(y_lw), ha="center", va="top", fontsize=6.5, color="black", zorder=3)
            ax.text(x_uw, y_uw + 0.8, fmt(y_uw), ha="center", va="bottom", fontsize=6.5, color="black", zorder=3)

        for med in bp["medians"]:
            x_med = np.mean(med.get_xdata())
            y_med = med.get_ydata()[0]
            ax.text(x_med, y_med + 0.8, fmt(y_med), ha="center", va="bottom", fontsize=6.5, fontweight="bold", color="black", zorder=3)

        for mean in bp["means"]:
            x_m = mean.get_xdata()[0]
            y_m = mean.get_ydata()[0]
            ax.text(x_m, y_m - 1.5, fmt(y_m), ha="center", va="top", fontsize=6.5, fontstyle="italic", color="black", zorder=3)

ax.set_xticks([])
ax.set_xticklabels([])
ax.tick_params(axis="x", which="both", length=0)
ax.set_ylabel("Electricity price (€/MWh)", fontsize=9)

for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(0.8)
    spine.set_color("black")

box_width = 0.7
pad_x = 0.4
x_min = centers[0] - box_gap - box_width / 2 - pad_x
x_max = centers[-1] + box_gap + box_width / 2 + pad_x
ax.set_xlim(x_min, x_max)

for center, year in zip(centers, YEARS):
    ax.text(center, 1.02, f"{year}", transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=9, clip_on=False)

scen_handles = [
    Patch(facecolor=lighten_color(color, amount=0.55), edgecolor="black", linewidth=0.8, label=label)
    for _, label, color in SCENARIOS
]
glyph_handles = [
    Line2D([], [], linestyle="-", color="black", linewidth=1.3, label="Median"),
    Line2D([], [], marker="x", color="black", linestyle="", markersize=6, label="Mean"),
]

fig.subplots_adjust(right=0.81, top=0.93, bottom=0.10, left=0.07)
fig.legend(handles=scen_handles + glyph_handles, loc="center left", bbox_to_anchor=(0.82, 0.5), frameon=False, fontsize=8, handlelength=1.5, handletextpad=0.5)

plt.show()