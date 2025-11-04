import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

years = [2030, 2035, 2040, 2045, 2050]
scenarios = ['REF', 'DYN', 'SIM', 'SWE']
scenario_labels = [
    "Reference (without SRE)",
    "Avg-dyn",
    "Avg-sim",
    "Avg-swe"
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
        [405, 659, 388, 169, 13, 23, 148, 91, 73, 176, 322, 24],
        [541, 853, 501, 294, 13, 46, 199, 194, 73, 176, 306, 22],
        [631, 977, 588, 417, 12, 105, 257, 268, 73, 176, 271, 7],
        [725, 1096, 732, 475, 9, 182, 303, 348, 73, 176, 227, 4],
        [798, 1170, 791, 533, 7, 261, 342, 396, 73, 176, 169, 2]
    ],
    'SIM': [
        [404, 658, 387, 169, 13, 22, 147, 91, 73, 176, 322, 24],
        [540, 852, 497, 294, 13, 45, 199, 193, 73, 176, 306, 22],
        [630, 975, 584, 417, 12, 101, 257, 267, 73, 176, 271, 7],
        [725, 1096, 731, 475, 9, 178, 301, 349, 73, 176, 227, 4],
        [796, 1167, 791, 533, 7, 252, 342, 398, 73, 176, 169, 2]
    ],
    'SWE': [
        [394, 638, 393, 169, 13, 25, 142, 91, 73, 176, 322, 24],
        [531, 830, 516, 294, 13, 53, 187, 204, 73, 176, 306, 22],
        [620, 952, 610, 417, 12, 112, 243, 279, 73, 176, 271, 7],
        [701, 1066, 760, 483, 9, 180, 288, 364, 73, 176, 227, 4],
        [775, 1138, 818, 541, 7, 264, 314, 411, 73, 176, 169, 2]
    ]
}

difference_data = {
    'DYN': [
        [16, 31, 2, 0, 0, 0, 8, 2, 0, 0, 0, 0],
        [25, 47, 3, 1, 0, 3, 14, 0, 0, 0, 0, 0],
        [28, 57, 4, 0, 0, 9, 17, -5, 0, 0, 0, 0],
        [42, 60, -4, -1, 0, 17, 21, -7, 0, 0, 0, 0],
        [51, 70, -2, -1, 0, 21, 30, -9, 0, 0, 0, 0]
    ],
    'SIM': [
        [15, 30, 1, 0, 0, 0, 8, 1, 0, 0, 0, 0],
        [25, 47, -1, 1, 0, 1, 14, -2, 0, 0, 0, 0],
        [27, 55, 0, 0, 0, 5, 17, -5, 0, 0, 0, 0],
        [42, 60, -5, -1, 0, 13, 19, -6, 0, 0, 0, 0],
        [49, 67, -3, -1, 0, 12, 31, -8, 0, 0, 0, 0]
    ],
    'SWE': [
        [5, 10, 6, 0, 0, 2, 3, 1, 0, 0, 0, 0],
        [15, 25, 18, 1, 0, 9, 2, 9, 0, 0, 0, 0],
        [17, 32, 26, 0, 0, 16, 2, 7, 0, 0, 0, 0],
        [17, 29, 24, 7, 0, 14, 6, 9, 0, 0, 0, 0],
        [28, 38, 25, 8, 0, 24, 3, 6, 0, 0, 0, 0]
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
                    ax1.text(current, center_y, f"{int(value)}",
                             ha='center', va='center', fontsize=8, fontweight='bold')

                elif tech == 'Biomass':
                    if year in {2030, 2035}:
                        offset = 0.35 if label_toggle_abs else -0.35
                        ha = 'left' if label_toggle_abs else 'right'
                        ax1.text(current + offset, center_y, f"{int(value)}",
                                 ha=ha, va='center', fontsize=8, fontweight='bold')
                        ax1.plot([current + (width/2 if label_toggle_abs else -width/2),
                                  current + (0.3 if label_toggle_abs else -0.3)],
                                 [center_y, center_y], color='black', linewidth=0.5)
                        label_toggle_abs = not label_toggle_abs
                    else:
                        ax1.text(current, center_y, f"{int(value)}",
                                 ha='center', va='center', fontsize=8, fontweight='bold')

                else:
                    if (
                        (tech == 'Other' and value >= 7) or
                        tech in {'Pumped hydro storage'} or
                        (tech != 'Other' and value > 150)
                    ):
                        ax1.text(current, center_y, f"{int(value)}",
                                 ha='center', va='center', fontsize=8, fontweight='bold')
                    elif tech != 'Other':
                        offset = 0.35 if label_toggle_abs else -0.35
                        ha = 'left' if label_toggle_abs else 'right'
                        ax1.text(current + offset, center_y, f"{int(value)}",
                                 ha=ha, va='center', fontsize=8, fontweight='bold')
                        ax1.plot([current + (width/2 if label_toggle_abs else -width/2),
                                  current + (0.3 if label_toggle_abs else -0.3)],
                                 [center_y, center_y], color='black', linewidth=0.5)
                        label_toggle_abs = not label_toggle_abs

            bottom += value
        current += 1
    current += 1.5

current = 0
for scenario in scenarios:
    if scenario == 'REF':
        for _ in range(len(years)):
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
                ax2.text(current, center_y, f"+{int(diff_value)}", ha='center', va='center',
                         fontsize=8, fontweight='bold', color='black')
                pos_bottom += diff_value

            elif diff_value < -1:
                ax2.bar(current, diff_value, width=width, bottom=neg_bottom, color=color)
                center_y = neg_bottom + diff_value / 2
                ax2.text(current, center_y, f"{int(diff_value)}", ha='center', va='center',
                         fontsize=8, fontweight='bold', color='black')
                neg_bottom += diff_value

        current += 1
    current += 1.5

ax1.set_ylabel('Installed capacity [GW]', fontweight='bold', fontsize=14)
ax1.set_ylim(0, 5000)
ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax1.set_xticks([])
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
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

midpoints = [(x_positions[i*5] + x_positions[i*5+4]) / 2 for i in range(len(scenarios))]
for idx, midpoint in enumerate(midpoints):
    ax2.text(midpoint, ax2.get_ylim()[0] - 0.12 * (ax2.get_ylim()[1] - ax2.get_ylim()[0]),
             scenario_labels[idx], ha='center', va='top', fontsize=14, fontweight='bold')

handles = [mpatches.Patch(color=colors[i], label=technologies[i]) for i in range(len(technologies))]
handles = handles[::-1]
fig.subplots_adjust(right=0.83)
ax1.legend(handles=handles, loc='center left', bbox_to_anchor=(1.01, 0.5), frameon=False)

plt.show()