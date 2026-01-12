import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

years = [2030, 2035, 2040, 2045, 2050]
scenarios = ['full_avail_ref', 'avg_avail', 'low_avail']
scenario_labels = [
    "Full availability (100%)",
    "Average availability (61%)",
    "Low availability (25%)"
]

technologies = [
    'Solar power (PV)', 'Onshore wind power', 'Offshore wind power', 'Biomass',
    'Battery storage', 'Hydrogen', 'Electrolysis', 'Hydropower', 'Pumped hydro storage', 'Conventional', 'Other'
]
colors = ['yellow', 'LightSeaGreen', 'darkcyan', 'Salmon', 
          'lightgreen', 'violet', 'mediumvioletred', 'cyan', 'dodgerblue', 'red', 'grey']

absolute_data = {
    'full_avail_ref': [
        [1226, 369, 169, 13, 3, 150, 66, 176, 73, 322, 24],
        [1447, 444, 291, 13, 15, 204, 134, 176, 73, 306, 22],
        [1647, 539, 413, 12, 51, 276, 215, 176, 73, 268, 7],
        [1910, 661, 475, 9, 92, 392, 287, 176, 73, 216, 4],
        [2069, 766, 533, 7, 148, 454, 347, 176, 73, 135, 2]
    ],
    'avg_avail': [
        [1204, 375, 169, 13, 4, 149, 77, 176, 73, 322, 24],
        [1441, 445, 291, 13, 15, 204, 140, 176, 73, 306, 22],
        [1647, 539, 413, 12, 49, 277, 221, 176, 73, 268, 7],
        [1915, 656, 475, 9, 91, 395, 289, 176, 73, 216, 4],
        [2074, 764, 533, 7, 147, 457, 351, 176, 73, 135, 2]
    ],
    'low_avail': [
        [1040, 387, 169, 13, 8, 147, 86, 176, 73, 322, 24],
        [1328, 463, 291, 13, 12, 202, 162, 176, 73, 306, 22],
        [1572, 561, 415, 12, 49, 271, 239, 176, 73, 268, 7],
        [1826, 698, 475, 9, 133, 331, 315, 176, 73, 216, 4],
        [1983, 803, 535, 7, 200, 386, 366, 176, 73, 135, 2]
    ]
}

difference_data = {
    'avg_avail': [
        [-21, 7, 0, 0, 0, 0, 10, 0, 0, 0, 0],
        [-7, 0, 0, 0, -1, 0, 6, 0, 0, 0, 0],
        [1, 0, 0, 0, -1, 1, 6, 0, 0, 0, 0],
        [5, -4, 0, 0, -1, 3, 2, 0, 0, 0, 0],
        [5, -1, 0, 0, -1, 3, 4, 0, 0, 0, 0]
    ],
    'low_avail': [
        [-185, 18, 0, 0, 4, -3, 20, 0, 0, 0, 0],
        [-119, 18, 0, 0, -3, -2, 28, 0, 0, 0, 0],
        [-75, 22, 3, 0, -2, -5, 24, 0, 0, 0, 0],
        [-84, 37, 0, 0, 41, -61, 29, 0, 0, 0, 0],
        [-86, 38, 1, 0, 53, -68, 19, 0, 0, 0, 0]
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

            label_allowed = True
            if tech == 'Other':
                label_allowed = True
            if year == 2030 and tech in ['Battery storage']:
                label_allowed = False
            if tech == 'Battery storage' and year >= 2035:
                label_allowed = True

            if tech in ['Battery storage', 'Conventional', 'Pumped hydro storage', 'Electrolysis'] and value > 0:
                center_y = bottom + value / 2
                ax1.text(current, center_y, f"{int(value)}", ha='center', va='center',
                         fontsize=8, fontweight='bold', color='black')
            elif label_allowed and value > 0:
                center_y = bottom + value / 2
                if (tech == 'Other' and value >= 7) or tech == 'Hydrogen' or (tech != 'Other' and value > 150):
                    ax1.text(current, center_y, f"{int(value)}", ha='center', va='center',
                            fontsize=8, fontweight='bold')
                elif tech != 'Other':
                    offset = 0.35 if label_toggle_abs else -0.35
                    ha = 'left' if label_toggle_abs else 'right'
                    ax1.text(current + offset, center_y, f"{int(value)}", ha=ha, va='center',
                            fontsize=8, fontweight='bold')
                    ax1.plot([current + (width/2 if label_toggle_abs else -width/2),
                            current + (0.3 if label_toggle_abs else -0.3)],
                            [center_y, center_y], color='black', linewidth=0.5)
                    label_toggle_abs = not label_toggle_abs
            bottom += value
        current += 1
    current += 1.5

difference_data.pop('full_avail_ref', None)
current = 0
for scenario in scenarios:
    if scenario == 'full_avail_ref':
        for idx in range(len(years)):
            ax2.hlines(y=0, xmin=current - width/2, xmax=current + width/2, color='white', linewidth=1)
            current += 1
        current += 1.5
        continue

    for idx, year in enumerate(years):
        pos_bottom = 0
        neg_bottom = 0

        for tech_idx, tech in enumerate(technologies):
            diff_value = difference_data[scenario][idx][tech_idx]
            color = colors[tech_idx]

            if diff_value > 0:
                ax2.bar(current, diff_value, width=width, bottom=pos_bottom, color=color)
                if diff_value >= 2:
                    center_y = pos_bottom + diff_value / 2
                    ax2.text(current, center_y, f"+{int(diff_value)}", ha='center', va='center',
                            fontsize=8, fontweight='bold', color='black')
                pos_bottom += diff_value

            elif diff_value < 0:
                ax2.bar(current, diff_value, width=width, bottom=neg_bottom, color=color)
                if diff_value <= -2:
                    center_y = neg_bottom + diff_value / 2
                    ax2.text(current, center_y, f"{int(diff_value)}", ha='center', va='center',
                            fontsize=8, fontweight='bold', color='black')
                neg_bottom += diff_value

        current += 1
    current += 1.5

ax1.set_xticks([])
ax1.set_ylabel('Installed capacity [GW]', fontweight='bold', fontsize=14)
ax1.set_ylim(0, 5000)
ax1.spines['bottom'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.axhline(color='black', alpha=0.7, linestyle='-')

ax2.set_xticks(x_positions)
ax2.set_xticklabels([str(year) for year in years] * len(scenarios))
ax2.set_ylabel('Difference to the\nfull availability [GW]', fontweight='bold', fontsize=14)
ax2.set_ylim(-210, 150)
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

plt.tight_layout()
plt.show()