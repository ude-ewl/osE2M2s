import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import NullFormatter
from itertools import chain

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
        "DYN": [6.40, 19.17, 36.11, 54.98, 77.18 ],
        "SIM": [6.10, 18.22, 34.08, 51.55, 72.31],
        "SWE": [6.70, 20.02, 37.77, 59.36, 82.87],
    }
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
markers = {"DYN": 'o', "SIM": 'o', "SWE": 'o'}
scenario_labels = {"DYN": "Dynamic", "SIM": "Simultaneous", "SWE": "Sweeping"}

fig = plt.figure(figsize=(20, 5))
outer = fig.add_gridspec(1, 2, width_ratios=[1.05, 3.0], wspace=0.16)
ax0 = fig.add_subplot(outer[0])

right = outer[1].subgridspec(1, 3, wspace=0.14)
axes_right = [fig.add_subplot(right[0, i]) for i in range(3)]
axes = [ax0] + axes_right

ax0.plot(years, ref_cost, label="Reference", color="#666666",
         linestyle="-", marker='o', linewidth=2, markersize=5)
ax0.plot(years, high_swe_total, label="Maximum SRE", color=colors["SWE"],
         linestyle="--", marker='o', linewidth=2, markersize=5)

for key, values in abs_totals.items():
    if "DYN" in key:
        c = colors["DYN"]
    elif "SIM" in key:
        c = colors["SIM"]
    elif "SWE" in key:
        c = colors["SWE"]
    ax0.plot(years, values, linestyle="None", marker='o', color=c, markersize=4, alpha=0.9)

pct_inc = [(h - r) / r * 100 for r, h in zip(ref_cost, high_swe_total)]
ymin, ymax = ax0.get_ylim()
y_offset = 0.015 * (ymax - ymin)
for x, y, p in zip(years, high_swe_total, pct_inc):
    ax0.text(x, y + y_offset, f"+{p:.1f}%", ha="center", va="bottom",
             fontsize=10, fontweight='bold', color=colors["SWE"], clip_on=False)

ax0.set_title("Overall view", fontsize=14, fontweight='bold')
ax0.set_ylabel("Total system costs [bn€/yr]", fontweight='bold', fontsize=14)
ax0.set_xticks(years)
ax0.legend(frameon=False, loc="upper left")

for ax, (title, data) in zip(axes[1:], sre_costs.items()):
    for scen in ["SWE", "DYN", "SIM"]:
        ax.plot(years, data[scen],
                label=scenario_labels[scen],
                color=colors[scen],
                linestyle=linestyles[scen],
                marker=markers[scen],
                markersize=5, linewidth=2)

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(years)

axes[1].set_ylabel("Additional system costs [bn€]", fontweight='bold', fontsize=14)

max_y = max([
    max(chain.from_iterable(sre_costs[scenario][scen] for scen in ["DYN", "SIM", "SWE"]))
    for scenario in sre_costs
])
ymax = 90
for ax in axes[1:]:
    ax.set_ylim(0, ymax)

axes[1].set_ylabel("Additional system costs [bn€]", fontweight='bold', fontsize=14)

for ax in axes[2:]:
    ax.tick_params(axis='y', which='major', left=True, labelleft=False)
    ax.yaxis.set_major_formatter(NullFormatter())
    ax.spines['left'].set_visible(True)

handles, labels = [], []
for scen in ["DYN", "SIM", "SWE"]:
    handles.append(plt.Line2D([], [], color=colors[scen],
                              linestyle=linestyles[scen],
                              marker=markers[scen],
                              label=scenario_labels[scen]))
    labels.append(scenario_labels[scen])

plt.subplots_adjust(right=0.85)
plt.tight_layout(rect=[0, 0, 0.85, 1])

fig.legend(handles, labels,
           loc='center left', bbox_to_anchor=(0.85, 0.5),
           frameon=False)

plt.show()