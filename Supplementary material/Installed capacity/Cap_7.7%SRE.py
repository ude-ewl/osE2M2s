import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

years = [2030, 2035, 2040, 2045, 2050]
scenarios = ['REF', 'DYN', 'SIM', 'SWE']
scenario_labels = [
    "Reference (without SRE)",
    "Low-dyn",
    "Low-sim",
    "Low-swe"
]

technologies = [
    'Residential (rooftop) PV', 'Utility-scale PV',
    'Onshore wind power', 'Offshore wind power',
    'Biomass', 'Battery storage',
    'Hydrogen', 'Electrolyzer',
    'Pumped hydro storage', 'Hydropower',
    'Conventional', 'Other'
]

colors = [
    'gold', 'yellow',
    'mediumturquoise', 'cadetblue',
    'salmon', 'forestgreen',
    'violet', 'mediumvioletred',
    'blueviolet', 'cyan',
    'red', 'gray'
]

absolute_data = {
    'REF': [
        [389, 628, 387, 169, 13, 23, 140, 89, 73, 176, 322, 24],
        [515, 805, 498, 293, 13, 44, 185, 195, 73, 176, 306, 22],
        [602, 920, 584, 417, 12, 96, 240, 273, 73, 176, 271, 7],
        [684, 1036, 736, 476, 9, 165, 282, 355, 73, 176, 227, 4],
        [747, 1100, 794, 533, 7, 240, 311, 405, 73, 176, 169, 2]
    ],
    'DYN': [
        [397, 644, 388, 169, 13, 23, 141, 91, 73, 176, 322, 24],
        [528, 830, 500, 294, 13, 46, 188, 197, 73, 176, 306, 22],
        [614, 945, 591, 417, 12, 102, 243, 274, 73, 176, 271, 7],
        [703, 1062, 732, 475, 9, 174, 288, 350, 73, 176, 227, 4],
        [774, 1134, 796, 533, 7, 256, 318, 403, 73, 176, 169, 2]
    ],
    'SIM': [
        [397, 644, 387, 169, 13, 22, 141, 92, 73, 176, 322, 24],
        [527, 829, 498, 293, 13, 44, 187, 197, 73, 176, 306, 22],
        [613, 943, 583, 417, 12, 101, 241, 272, 73, 176, 271, 7],
        [701, 1063, 729, 475, 9, 172, 286, 352, 73, 176, 227, 4],
        [771, 1129, 792, 533, 7, 250, 317, 404, 73, 176, 169, 2]
    ],
    'SWE': [
        [391, 632, 389, 169, 13, 24, 141, 89, 73, 176, 322, 24],
        [522, 815, 506, 294, 13, 48, 186, 198, 73, 176, 306, 22],
        [609, 932, 597, 417, 12, 103, 241, 275, 73, 176, 271, 7],
        [690, 1047, 745, 478, 9, 173, 285, 357, 73, 176, 227, 4],
        [760, 1116, 803, 537, 7, 254, 311, 406, 73, 176, 169, 2]
    ]
}

difference_data = {
    'DYN': [
        [8, 15, 1, 0, 0, 0, 2, 2, 0, 0, 0, 0],
        [12, 24, 2, 1, 0, 2, 2, 2, 0, 0, 0, 0],
        [12, 25, 7, 0, 0, 6, 3, 1, 0, 0, 0, 0],
        [19, 26, -5, -1, 0, 9, 6, -5, 0, 0, 0, 0],
        [27, 34, 2, 0, 0, 16, 7, -2, 0, 0, 0, 0]
    ],
    'SIM': [
        [8, 16, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0],
        [12, 24, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0],
        [11, 23, -1, 0, 0, 5, 0, 0, 0, 0, 0, 0],
        [18, 27, -7, -1, 0, 7, 4, -3, 0, 0, 0, 0],
        [23, 29, -2, -1, 0, 10, 6, -1, 0, 0, 0, 0]
    ],
    'SWE': [
        [2, 3, 2, 0, 0, 1, 1, -1, 0, 0, 0, 0],
        [6, 10, 8, 1, 0, 4, 1, 3, 0, 0, 0, 0],
        [7, 12, 13, 0, 0, 7, 1, 3, 0, 0, 0, 0],
        [7, 11, 9, 3, 0, 7, 3, 2, 0, 0, 0, 0],
        [13, 17, 10, 3, 0, 14, -1, 1, 0, 0, 0, 0]
    ]
}

fig = plt.figure(figsize=(18, 14))
gs = fig.add_gridspec(2, 1, height_ratios=[3, 1], hspace=0.05)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

width = 0.7
x_positions = []
current = 0

ax1.axhline(0, color='black', linewidth=0.8, linestyle='-')
for scenario in scenarios:
    for idx, year in enumerate(years):
        x_positions.append(current)
        bottom = 0
        label_toggle_abs = False
        for tech_idx, tech in enumerate(technologies):
            value = absolute_data[scenario][idx][tech_idx]
            color = colors[tech_idx]
            ax1.bar(current, value, width=width, bottom=bottom, color=color)

            if value > 0:
                center_y = bottom + value / 2

                if tech in {'Hydrogen', 'Battery storage', 'Electrolyzer'}:
                    ax1.text(current, center_y, f"{int(value)}", ha='center', va='center', fontsize=8, fontweight='bold')

                elif tech == 'Biomass':
                    if year in {2030, 2035}:
                        offset = 0.35 if label_toggle_abs else -0.35
                        ha = 'left' if label_toggle_abs else 'right'
                        ax1.text(current + offset, center_y, f"{int(value)}", ha=ha, va='center', fontsize=8, fontweight='bold')
                        ax1.plot([current + (width/2 if label_toggle_abs else -width/2),
                                  current + (0.3 if label_toggle_abs else -0.3)],
                                 [center_y, center_y], color='black', linewidth=0.5)
                        label_toggle_abs = not label_toggle_abs
                    else:
                        ax1.text(current, center_y, f"{int(value)}", ha='center', va='center', fontsize=8, fontweight='bold')

                else:
                    if ((tech == 'Other' and value >= 7) or tech == 'Pumped hydro storage' or (tech != 'Other' and value > 150)):
                        ax1.text(current, center_y, f"{int(value)}", ha='center', va='center', fontsize=8, fontweight='bold')
                    elif tech != 'Other':
                        offset = 0.35 if label_toggle_abs else -0.35
                        ha = 'left' if label_toggle_abs else 'right'
                        ax1.text(current + offset, center_y, f"{int(value)}", ha=ha, va='center', fontsize=8, fontweight='bold')
                        ax1.plot([current + (width/2 if label_toggle_abs else -width/2),
                                  current + (0.3 if label_toggle_abs else -0.3)],
                                 [center_y, center_y], color='black', linewidth=0.5)
                        label_toggle_abs = not label_toggle_abs

            bottom += value
        current += 1
    current += 1.5

current = 0
len_years = len(years)
for scenario in scenarios:
    if scenario == 'REF':
        for _ in years:
            ax2.hlines(y=0, xmin=current - width/2, xmax=current + width/2, color='white', linewidth=1)
            current += 1
        current += 1.5
        continue

    for idx, _ in enumerate(years):
        pos_bottom = 0
        neg_bottom = 0
        for tech_idx, tech in enumerate(technologies):
            diff_value = difference_data[scenario][idx][tech_idx]
            color = colors[tech_idx]
            if diff_value > 2:
                ax2.bar(current, diff_value, width=width, bottom=pos_bottom, color=color)
                center_y = pos_bottom + diff_value / 2
                ax2.text(current, center_y, f"+{int(diff_value)}", ha='center', va='center', fontsize=8, fontweight='bold', color='black')
                pos_bottom += diff_value
            elif diff_value < -1:
                ax2.bar(current, diff_value, width=width, bottom=neg_bottom, color=color)
                center_y = neg_bottom + diff_value / 2
                ax2.text(current, center_y, f"{int(diff_value)}", ha='center', va='center', fontsize=8, fontweight='bold', color='black')
                neg_bottom += diff_value
        current += 1
    current += 1.5

ax1.set_ylabel('Installed capacity [GW]', fontweight='bold', fontsize=14)
ax1.set_ylim(0, 5000)
ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ticks = ax1.get_yticks()
ax1.set_yticks([t for t in ticks if t != 0])
ax1.spines['bottom'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

ax2.set_xticks(x_positions)
ax2.set_xticklabels(years * len(scenarios))
ax2.set_ylabel('Difference to\nthe reference —\ncapacity [GW]', fontweight='bold', fontsize=14)
ax2.axhline(color='black', linewidth=0.5, linestyle='-')
ax2.set_ylim(-15, 85)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

len_scenarios = len(scenarios)
midpoints = [(x_positions[i * len_years] + x_positions[i * len_years + len_years - 1]) / 2 for i in range(len_scenarios)]
for idx, midpoint in enumerate(midpoints):
    ax2.text(midpoint, ax2.get_ylim()[0] - 0.12 * (ax2.get_ylim()[1] - ax2.get_ylim()[0]),
             scenario_labels[idx], ha='center', va='top', fontsize=14, fontweight='bold')

handles = [mpatches.Patch(color=colors[i], label=technologies[i]) for i in range(len(technologies))]
handles = handles[::-1]
fig.subplots_adjust(right=0.83)
ax1.legend(handles=handles, loc='center left', bbox_to_anchor=(1.01, 0.5), frameon=False)

plt.show()