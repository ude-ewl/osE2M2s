from __future__ import annotations

from itertools import chain

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

years = [2030, 2035, 2040, 2045, 2050]
sre_costs = {
    "Low scenario (7.7% SRE)": {
        "DYN": [1.48, 4.41, 8.43, 13.24, 18.65],
        "SIM": [1.10, 3.22, 6.01, 9.10, 12.69],
        "SWE": [1.55, 4.51, 8.38, 13.15, 18.29],
    },
    "Average scenario (17.2% SRE)": {
        "DYN": [3.13, 9.30, 17.41, 26.58, 37.26],
        "SIM": [2.81, 8.25, 15.21, 22.89, 31.90],
        "SWE": [3.48, 10.24, 19.17, 30.08, 42.06],
    },
    "High scenario (33% SRE)": {
        "DYN": [6.40, 19.17, 36.11, 54.98, 77.18],
        "SIM": [6.10, 18.22, 34.08, 51.55, 72.31],
        "SWE": [6.70, 20.02, 37.77, 59.36, 82.87],
    },
}

ref_cost = [411.138, 465.042, 487.826, 526.795, 554.718]
high_swe_total = [417.839, 478.364, 505.574, 548.385, 578.225]

abs_totals = {
    "LOW_DYN": [412.613, 467.974, 491.849, 531.607, 560.125],
    "LOW_SIM": [412.241, 467.157, 490.614, 529.892, 558.307],
    "LOW_SWE": [412.687, 468.000, 491.699, 531.560, 559.864],
    "AVG_DYN": [414.269, 471.210, 495.933, 535.968, 565.394],
    "AVG_SIM": [413.948, 470.485, 494.787, 534.467, 563.731],
    "AVG_SWE": [414.613, 471.803, 496.758, 537.711, 566.695],
    "HIGH_DYN": [417.542, 477.805, 504.764, 545.667, 576.917],
    "HIGH_SIM": [417.239, 477.163, 503.680, 544.272, 575.473],
    "HIGH_SWE": [417.839, 478.364, 505.574, 548.385, 578.225],
}

colors = {"DYN": "#E18B6B", "SIM": "#78B43D", "SWE": "#5B84B1"}
linestyles = {"DYN": "-", "SIM": ":", "SWE": "--"}
markers = {"DYN": "o", "SIM": "o", "SWE": "o"}
scenario_labels = {"DYN": "Dynamic", "SIM": "Simultaneous", "SWE": "Sweeping"}

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
    years,
    ref_cost,
    label="Reference",
    color="0.45",
    linestyle="-",
    marker="o",
    linewidth=LW_REF,
    markersize=MS_MAIN,
)
ax0.plot(
    years,
    high_swe_total,
    label="Maximum SRE",
    color=colors["SWE"],
    linestyle="--",
    marker="o",
    linewidth=LW_MAIN,
    markersize=MS_MAIN,
)

for key, values in abs_totals.items():
    if key == "HIGH_SWE":
        continue
    if "DYN" in key:
        c = colors["DYN"]
    elif "SIM" in key:
        c = colors["SIM"]
    else:
        c = colors["SWE"]
    ax0.plot(
        years,
        values,
        linestyle="None",
        marker="o",
        color=c,
        markersize=MS_PTS,
        alpha=0.9,
    )

fig.canvas.draw()
ymin, ymax = ax0.get_ylim()
y_offset = 0.015 * (ymax - ymin)
pct_inc = [(h - r) / r * 100 for r, h in zip(ref_cost, high_swe_total)]
for x, y, p in zip(years, high_swe_total, pct_inc):
    ax0.text(
        x,
        y + y_offset,
        f"+{p:.1f}%",
        ha="center",
        va="bottom",
        fontsize=8,
        color=colors["SWE"],
        clip_on=False,
    )

ax0.set_title("Overall view")
ax0.set_xlabel("Year", labelpad=XLABEL_PAD)
ax0.set_ylabel("Total system costs (bn€/yr)", labelpad=YLABEL_PAD)
ax0.set_xticks(years)
ax0.legend(frameon=False, loc="upper left", fontsize=8)

titles = list(sre_costs.keys())
for ax, title in zip(axes[1:], titles):
    data = sre_costs[title]
    for scen in ["DYN", "SIM", "SWE"]:
        ax.plot(
            years,
            data[scen],
            color=colors[scen],
            linestyle=linestyles[scen],
            marker=markers[scen],
            markersize=MS_MAIN,
            linewidth=LW_MAIN,
        )
    ax.set_title(title)
    ax.set_xlabel("Year", labelpad=XLABEL_PAD)
    ax.set_ylabel("Additional system costs (bn€/yr)", labelpad=YLABEL_PAD)
    ax.set_xticks(years)

max_y = max(
    max(chain.from_iterable(sre_costs[scenario][scen] for scen in ["DYN", "SIM", "SWE"]))
    for scenario in sre_costs
)
ymax_add = (int(max_y / 10) + 1) * 10
for ax in axes[1:]:
    ax.set_ylim(0, ymax_add)

handles = [
    Line2D(
        [],
        [],
        color=colors[k],
        linestyle=linestyles[k],
        marker=markers[k],
        linewidth=LW_MAIN,
        markersize=MS_MAIN,
        label=scenario_labels[k],
    )
    for k in ["DYN", "SIM", "SWE"]
]
labels = [scenario_labels[k] for k in ["DYN", "SIM", "SWE"]]

fig.legend(
    handles,
    labels,
    loc="center left",
    bbox_to_anchor=(0.875, 0.50),
    frameon=False,
    fontsize=8,
)

plt.show()