import matplotlib.pyplot as plt
import numpy as np

ref = [
    66.74, 62.77, 67.71, 69.33, 66.84, 65.32, 68.61, 67.94, 61.80, 61.65, 55.62, 64.74, 56.08, 55.93, 61.41, 67.16, 66.88, 69.58, 66.67, 55.06, 68.66, 55.74, 67.11, 66.91, 68.34, 57.57, 67.28, 53.98, 66.87, 67.51, 55.48, 66.79, 70.43, 66.10
]

low_dyn = [
    67.26, 63.37, 68.19, 69.79, 67.30, 65.71, 69.13, 68.60, 62.19, 62.07, 55.79, 65.06, 56.06, 56.12, 61.50, 67.68, 67.23, 69.92, 67.11, 55.16, 69.29, 55.85, 67.63, 67.40, 68.84, 57.69, 67.71, 54.09, 67.16, 67.95, 55.67, 67.36, 70.99, 66.51
]

low_sim = [
    67.14, 63.11, 68.13, 69.57, 67.21, 65.66, 68.78, 68.22, 61.92, 61.78, 55.79, 65.03, 55.97, 56.13, 61.36, 67.61, 67.20, 69.64, 66.89, 55.14, 68.91, 55.85, 67.52, 67.26, 68.45, 57.67, 67.43, 54.00, 67.11, 67.91, 55.67, 67.27, 70.59, 66.21
]

low_swe = [
    67.23, 63.17, 68.15, 69.81, 67.27, 65.81, 69.04, 68.50, 62.13, 61.97, 55.62, 65.10, 56.29, 55.89, 61.66, 67.59, 67.29, 69.98, 67.23, 55.08, 69.21, 55.75, 67.60, 67.39, 68.90, 57.52, 67.64, 54.11, 67.22, 67.92, 55.46, 67.25, 71.05, 66.47
]

avg_dyn = [
    67.27, 63.46, 68.21, 70.09, 67.31, 65.65, 69.26, 68.67, 62.12, 61.98, 55.86, 65.03, 56.30, 56.18, 61.47, 67.71, 67.29, 69.86, 66.98, 55.18, 69.33, 55.91, 67.64, 67.33, 68.86, 57.76, 67.73, 54.39, 67.17, 68.00, 55.73, 67.41, 71.01, 66.53
]

avg_sim = [
    67.09, 63.24, 68.13, 69.86, 67.22, 65.52, 68.96, 68.34, 61.90, 61.74, 55.79, 64.91, 56.10, 56.13, 61.39, 67.61, 67.22, 69.61, 66.80, 55.11, 69.00, 55.83, 67.51, 67.16, 68.57, 57.71, 67.47, 54.24, 67.12, 67.91, 55.67, 67.27, 70.68, 66.26
]

avg_swe = [
    67.82, 63.73, 68.72, 70.63, 67.78, 66.54, 69.80, 69.49, 62.76, 62.58, 55.84, 65.53, 56.77, 56.13, 62.24, 68.12, 67.73, 70.99, 67.99, 55.21, 70.17, 55.94, 68.21, 67.93, 69.82, 57.44, 68.18, 54.85, 67.54, 68.43, 55.76, 67.82, 72.07, 67.57
]

high_dyn = [
    65.70, 63.30, 66.61, 70.23, 65.86, 64.86, 69.05, 68.09, 62.06, 61.92, 56.23, 63.67, 56.11, 56.61, 60.60, 66.19, 65.86, 69.25, 64.81, 55.50, 68.70, 56.23, 65.97, 65.87, 68.45, 58.08, 67.43, 54.40, 65.76, 66.49, 56.10, 65.61, 70.60, 66.66
]

high_sim = [
    65.47, 63.16, 66.39, 70.08, 65.64, 64.66, 68.96, 67.94, 61.86, 61.71, 56.12, 63.54, 56.03, 56.50, 60.50, 65.97, 65.73, 69.33, 64.70, 55.39, 68.55, 56.13, 65.74, 65.63, 68.44, 57.96, 67.33, 54.39, 65.64, 66.26, 55.99, 65.47, 70.54, 66.54
]

high_swe = [
    69.92, 65.51, 70.87, 73.04, 69.95, 68.53, 72.44, 72.38, 64.20, 64.02, 56.36, 67.32, 58.32, 56.78, 63.96, 69.94, 69.47, 72.87, 70.18, 55.51, 73.01, 56.57, 70.32, 69.94, 72.59, 57.42, 69.43, 56.33, 69.24, 70.61, 56.13, 69.68, 74.29, 69.59
]

pos_ref  = [1]
pos_660  = [3, 4, 5]
pos_1683 = [7, 8, 9]
pos_33   = [11,12,13]

clusters = [
    (pos_660,  [low_dyn,  low_sim,  low_swe],
     "Low scenario (7.7% SRE)"),
    (pos_1683, [avg_dyn, avg_sim, avg_swe],
     "Average scenario (17.2% SRE)"),
    (pos_33,   [high_dyn, high_sim, high_swe],
     "High scenario (33% SRE)")
]

colours = {
    "Reference": "#FFFFFF",
    "Dyn":       "#E18B6B",
    "Sim":       "#78B43D",
    "Sweep":     "#5B84B1"
}

fig, ax = plt.subplots(figsize=(15, 6))

bp_ref = ax.boxplot([ref], positions=pos_ref, widths=0.8,
                    patch_artist=True, showmeans=True,
                    boxprops=dict(linewidth=1, color='black'),
                    whiskerprops=dict(linewidth=1, color='black'),
                    capprops=dict(linewidth=1, color='black'),
                    medianprops=dict(linewidth=1.5, color='black'),
                    meanprops=dict(marker="x", markersize=6, markeredgecolor="black"),
                    flierprops=dict(marker='o', markersize=3, linestyle='none', markerfacecolor='gray', alpha=0.3))

for i, line in enumerate(bp_ref["whiskers"]):
    x = line.get_xdata()[1]
    y = line.get_ydata()[1]
    if i % 2 == 0:
        ax.text(x, y - 0.3, f"{y:.2f}", ha="center", va="top", fontsize=8) 
    else:
        ax.text(x, y + 0.1, f"{y:.2f}", ha="center", va="bottom", fontsize=8) 

for mean in bp_ref["means"]:
    x = mean.get_xdata()[0]
    y = mean.get_ydata()[0]
    ax.text(x, y - 0.4, f"{y:.2f}", ha="center", va="top", fontsize=8)

for med in bp_ref["medians"]:
    x = np.mean(med.get_xdata())
    y = med.get_ydata()[0]
    ax.text(x, y + 0.1, f"{y:.2f}", ha="center", va="bottom", fontsize=8)

ref_path = bp_ref["boxes"][0].get_path().vertices
x = np.mean(ref_path[:, 0])
q1 = ref_path[1, 1]
q3 = ref_path[2, 1]
ax.text(x - 0.06, q1 - 0.25, f"{q1:.2f}", ha="center", va="top", fontsize=8)
ax.text(x - 0.06, q3 + 0.1, f"{q3:.2f}", ha="center", va="bottom", fontsize=8)

bp_ref["boxes"][0].set_facecolor("white")
bp_ref["boxes"][0].set_edgecolor("black")

for positions, data_lists, caption in clusters:
    bp = ax.boxplot(data_lists, positions=positions, widths=0.8,
                    patch_artist=True, showmeans=True,
                    boxprops=dict(linewidth=1, color='black'),
                    whiskerprops=dict(linewidth=1, color='black'),
                    capprops=dict(linewidth=1, color='black'),
                    medianprops=dict(linewidth=1.5, color='black'),
                    meanprops=dict(marker="x", markersize=6, markeredgecolor="black"),
                    flierprops=dict(marker='o', markersize=3, linestyle='none', markerfacecolor='gray', alpha=0.3))

    box_colors = [colours["Dyn"], colours["Sim"], colours["Sweep"]]
    for patch, color in zip(bp['boxes'], box_colors):
        patch.set_facecolor(color)
        patch.set_edgecolor("black")

    for i in range(0, len(bp['whiskers']), 2):
        lw = bp['whiskers'][i]
        uw = bp['whiskers'][i+1]

        x_lw, y_lw = lw.get_xdata()[1], lw.get_ydata()[1]
        x_uw, y_uw = uw.get_xdata()[1], uw.get_ydata()[1]

        ax.text(x_lw, y_lw - 0.3, f"{y_lw:.2f}", ha="center", va="top", fontsize=8)
        ax.text(x_uw, y_uw + 0.1, f"{y_uw:.2f}", ha="center", va="bottom", fontsize=8)

    for med in bp["medians"]:
        x = np.mean(med.get_xdata())
        y = med.get_ydata()[0]
        ax.text(x, y + 0.1, f"{y:.2f}", ha="center", va="bottom", fontsize=8)

    for mean in bp["means"]:
        x = mean.get_xdata()[0]
        y = mean.get_ydata()[0]
        ax.text(x, y - 0.4, f"{y:.2f}", ha="center", va="top", fontsize=8)

    for patch in bp["boxes"]:
        path = patch.get_path().vertices
        x = np.mean(path[:, 0])
        q1 = path[1, 1]
        q3 = path[2, 1]
        ax.text(x - 0.05, q1 - 0.3, f"{q1:.2f}", ha="center", va="top", fontsize=8)
        ax.text(x - 0.05, q3 + 0.1, f"{q3:.2f}", ha="center", va="bottom", fontsize=8)

    ax.text(np.mean(positions), 75.3, caption,
            ha="center", va="bottom", fontweight='bold', fontsize=14)

ax.set_ylabel("Electricity prices [€/MWh]", fontweight="bold", fontsize=14)
ax.set_ylim(53, 75)
ax.set_xticks([])

handles = [
    plt.Line2D([], [], marker='s', linestyle='', markersize=10,
               markerfacecolor=colours["Reference"], markeredgecolor='black', label="Reference"),
    plt.Line2D([], [], marker='s', linestyle='', markersize=10,
               markerfacecolor=colours["Dyn"], markeredgecolor='black', label="Dynamic"),           
    plt.Line2D([], [], marker='s', linestyle='', markersize=10,
               markerfacecolor=colours["Sim"], markeredgecolor='black', label="Simultaneous"),
    plt.Line2D([], [], marker='s', linestyle='', markersize=10,
               markerfacecolor=colours["Sweep"], markeredgecolor='black', label="Sweeping")
]

plt.subplots_adjust(right=0.85)
plt.tight_layout(rect=[0, 0, 0.87, 1])
fig.legend(handles, [h.get_label() for h in handles],
           loc='center left', bbox_to_anchor=(0.86, 0.5), frameon=False)

plt.show()