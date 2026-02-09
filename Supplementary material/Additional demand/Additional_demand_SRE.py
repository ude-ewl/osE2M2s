from __future__ import annotations

from itertools import chain
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

years = [2030, 2035, 2040, 2045, 2050]

ref_demand = [4469.86, 5242.57, 6057.14, 6791.00, 7316.72]
high_swe_total = [4543.33, 5457.20, 6358.92, 7096.05, 7689.97]

sre_demand = {
    "Low scenario (7.7% SRE)": {
        "DYN": [23.21, 47.33, 61.74, 69.66, 80.78],
        "SIM": [19.47, 39.21, 49.51, 55.18, 63.09],
        "SWE": [19.47, 38.70, 49.07, 54.82, 62.12],
    },
    "Average scenario (17.2% SRE)": {
        "DYN": [46.55, 95.82, 123.45, 138.75, 160.66],
        "SIM": [43.50, 88.88, 112.93, 126.29, 145.52],
        "SWE": [43.50, 87.16, 111.27, 124.47, 140.84],
    },
    "High scenario (33% SRE)": {
        "DYN": [85.92, 182.38, 237.70, 272.04, 314.93],
        "SIM": [83.45, 176.70, 228.42, 260.37, 301.94],
        "SWE": [83.45, 169.36, 218.02, 247.17, 276.34],
    },
}

sre_total = {
    "LOW_DYN":  [4496.71, 5291.91, 6123.12, 6843.85, 7401.65],
    "LOW_SIM":  [4493.92, 5281.69, 6100.03, 6830.50, 7373.80],
    "LOW_SWE":  [4483.18, 5288.49, 6121.96, 6855.17, 7398.46],
    "AVG_DYN":  [4520.06, 5328.42, 6165.30, 6907.01, 7456.11],
    "AVG_SIM":  [4515.11, 5315.30, 6147.60, 6894.02, 7438.07],
    "AVG_SWE":  [4506.36, 5351.23, 6200.72, 6949.83, 7502.34],
    "HIGH_DYN": [4557.01, 5390.67, 6254.65, 7042.96, 7614.79],
    "HIGH_SIM": [4557.02, 5380.47, 6239.56, 7032.32, 7593.35],
}

colors = {"DYN": "#E18B6B", "SIM": "#78B43D", "SWE": "#5B84B1"}
linestyles = {"DYN": "-", "SIM": ":", "SWE": "--"}
markers = {"DYN": "o", "SIM": "o", "SWE": "o"}
scenario_labels = {"DYN": "Dynamic", "SIM": "Simultaneous", "SWE": "Sweeping"}

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

fig = plt.figure(figsize=(15.5, 5.2))
gs = fig.add_gridspec(1, 4, wspace=0.35)
axes = [fig.add_subplot(gs[0, i]) for i in range(4)]

for ax in axes:
    ax.patch.set_visible(False)
fig.patch.set_facecolor("white")
fig.patch.set_alpha(1.0)

for ax in axes:
    try:
        ax.set_box_aspect(1)
    except Exception:
        pass

fig.subplots_adjust(left=0.06, right=0.86, bottom=0.18, top=0.88)

LW_MAIN = 1.4
LW_REF = 1.2
MS_MAIN = 3.8
MS_PTS = 3.2
YLABEL_PAD = 2
XLABEL_PAD = 2

ax0 = axes[0]
ax0.plot(
    years, ref_demand,
    label="Reference",
    color="0.45", linestyle="-",
    marker="o", linewidth=LW_REF, markersize=MS_MAIN
)
ax0.plot(
    years, high_swe_total,
    label="Maximum SRE",
    color=colors["SWE"], linestyle="--",
    marker="o", linewidth=LW_MAIN, markersize=MS_MAIN
)

for key, values in sre_total.items():
    if "DYN" in key:
        c = colors["DYN"]
    elif "SIM" in key:
        c = colors["SIM"]
    else:
        c = colors["SWE"]
    ax0.plot(
        years, values,
        linestyle="None", marker="o",
        color=c, markersize=MS_PTS, alpha=0.9
    )

fig.canvas.draw()
ymin, ymax = ax0.get_ylim()
y_offset = 0.015 * (ymax - ymin)

pct_inc = [(h - r) / r * 100 for r, h in zip(ref_demand, high_swe_total)]
for x, y, p in zip(years, high_swe_total, pct_inc):
    ax0.text(
        x, y + y_offset, f"+{p:.1f}%",
        ha="center", va="bottom",
        fontsize=8, color=colors["SWE"], clip_on=False
    )

ax0.set_title("Overall view")
ax0.set_xlabel("Year", labelpad=XLABEL_PAD)
ax0.set_ylabel("Total electricity demand (TWh/yr)", labelpad=YLABEL_PAD)
ax0.set_xticks(years)
ax0.legend(frameon=False, loc="upper left", fontsize=8)

titles = list(sre_demand.keys())
for ax, title in zip(axes[1:], titles):
    data = sre_demand[title]
    for scen in ["DYN", "SIM", "SWE"]:
        ax.plot(
            years, data[scen],
            label=scenario_labels[scen],
            color=colors[scen],
            linestyle=linestyles[scen],
            marker=markers[scen],
            markersize=MS_MAIN,
            linewidth=LW_MAIN
        )
    ax.set_title(title)
    ax.set_xlabel("Year", labelpad=XLABEL_PAD)
    ax.set_ylabel("Additional electricity demand (TWh/yr)", labelpad=YLABEL_PAD)
    ax.set_xticks(years)

max_y = max(
    max(chain.from_iterable(sre_demand[scenario][scen] for scen in ["DYN", "SIM", "SWE"]))
    for scenario in sre_demand
)
ymax = (int(max_y / 50) + 1) * 50
for ax in axes[1:]:
    ax.set_ylim(0, ymax)

handles = [
    Line2D([], [], color=colors[k], linestyle=linestyles[k], marker=markers[k],
           linewidth=LW_MAIN, markersize=MS_MAIN, label=scenario_labels[k])
    for k in ["DYN", "SIM", "SWE"]
]
labels = [scenario_labels[k] for k in ["DYN", "SIM", "SWE"]]

fig.legend(
    handles, labels,
    loc="center left",
    bbox_to_anchor=(0.875, 0.50),
    frameon=False,
    fontsize=8
)

plt.show()