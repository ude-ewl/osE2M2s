import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

years = [2030, 2035, 2040, 2045, 2050]
scenarios = ['full_avail_ref', 'avg_avail', 'low_avail']
scenario_labels = [
    "Full availability (100%)",
    "Average availability (61%)",
    "Low availability (25%)"
]

technologies = [
    'EV discharging', 'Solar power (PV)', 'Onshore wind power', 'Offshore wind power', 'Biomass',
    'Battery storage', 'Hydrogen', 'Hydropower', 'Pumped hydro storage', 'Conventional', 'Other'
]

colors = ['orange', 'yellow', 'LightSeaGreen', 'darkcyan', 'Salmon', 
          'lightgreen', 'violet', 'cyan', 'dodgerblue', 'red', 'grey']

neg_tech_labels = ['EV charging', 'Battery charging', 'Electrolysis', 'Pumped hydro pumping']
neg_colors = ['orange', 'lightgreen', 'mediumvioletred', 'dodgerblue']

absolute_data = {
    'full_avail_ref': [
        [210, 1309, 748, 525, 0, 111, 38, 503, 21, 1324, 61],
        [247, 1621, 920, 926, 6, 116, 46, 500, 34, 1103, 58],
        [251, 1796, 1127, 1336, 39, 135, 62, 499, 38, 860, 7],
        [320, 1994, 1517, 1536, 62, 148, 136, 498, 61, 620, 4],
        [322, 2147, 1777, 1726, 51, 190, 160, 496, 68, 425, 2]
    ],
    'avg_avail': [
        [169, 1273, 772, 525, 1, 108, 40, 502, 32, 1337, 61],
        [233, 1595, 945, 926, 6, 116, 46, 500, 36, 1103, 59],
        [249, 1763, 1142, 1336, 39, 136, 62, 498, 39, 862, 7],
        [313, 1972, 1527, 1535, 62, 149, 136, 498, 63, 626, 4],
        [317, 2124, 1781, 1726, 51, 189, 161, 496, 67, 425, 2]
    ],
    'low_avail': [
        [47, 1182, 827, 525, 1, 110, 43, 502, 42, 1362, 59],
        [107, 1443, 978, 926, 8, 112, 47, 500, 43, 1108, 58],
        [173, 1665, 1201, 1336, 42, 132, 63, 498, 45, 877, 7],
        [206, 1898, 1574, 1537, 63, 180, 149, 497, 73, 625, 4],
        [198, 2040, 1840, 1727, 52, 243, 178, 495, 78, 425, 2]
    ]
}

charging_data = {
    'full_avail_ref': [
        [-323, -117, -398, -28],
        [-474, -122, -573, -45],
        [-582, -142, -631, -51],
        [-719, -156, -966, -81],
        [-735, -200, -1144, -89]
    ],
    'avg_avail': [
        [-278, -114, -402, -42],
        [-459, -122, -573, -47],
        [-580, -143, -614, -51],
        [-711, -157, -959, -83],
        [-729, -198, -1127, -88]
    ],
    'low_avail': [
        [-142, -115, -401, -56],
        [-319, -118, -473, -56],
        [-495, -139, -602, -59],
        [-592, -189, -954, -97],
        [-598, -256, -1127, -102]
    ]
}

n_years = len(years)
n_techs = len(technologies)
n_neg = len(neg_tech_labels)

TITLE_TEXT = "Battery storage capacity in 2030:+100 GW"
_orig_figure = plt.figure
def _figure_with_title(*args, **kwargs):
    fig = _orig_figure(*args, **kwargs)
    fig.suptitle(TITLE_TEXT, fontsize=16, y=0.985)
    fig.subplots_adjust(top=0.95)
    return fig
plt.figure = _figure_with_title

difference_data = {}
for scen in scenarios:
    if scen == 'full_avail_ref':
        continue
    diff_years = []
    for yi in range(n_years):
        diff_year = []
        for ti in range(n_techs):
            diff = absolute_data[scen][yi][ti] - absolute_data['full_avail_ref'][yi][ti]
            diff_year.append(diff)
        diff_years.append(diff_year)
    difference_data[scen] = diff_years

charging_diff_data = {}
for scen in scenarios:
    if scen == 'full_avail_ref':
        continue
    diff_years = []
    for yi in range(n_years):
        diff_year = []
        for ci in range(n_neg):
            ref_val = charging_data['full_avail_ref'][yi][ci]
            scen_val = charging_data[scen][yi][ci]
            diff = -(scen_val - ref_val)
            diff_year.append(diff)
        diff_years.append(diff_year)
    charging_diff_data[scen] = diff_years

fig = plt.figure(figsize=(18, 14))
gs = fig.add_gridspec(3, 1, height_ratios=[3, 1, 0.8], hspace=0.05)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1)
ax3 = fig.add_subplot(gs[2], sharex=ax1)

width = 0.7
x_positions = []
current = 0

ax1.axhline(0, color='black', linewidth=0.8, linestyle='-')
for scenario in scenarios:
    for idx, year in enumerate(years):
        x_positions.append(current)

        bottom_neg = 0
        label_toggle_neg = False
        for neg_idx, neg_tech in enumerate(neg_tech_labels):
            value = charging_data[scenario][idx][neg_idx]
            ax1.bar(current, value, width=width, bottom=bottom_neg,
            color=neg_colors[neg_idx], edgecolor='none', linewidth=0)
            center_y = bottom_neg + value / 2

            if abs(value) < 0:
                offset = 0.3 if label_toggle_neg else -0.3
                ha = 'left' if label_toggle_neg else 'right'
                ax1.plot([current + (width/2 if label_toggle_neg else -width/2),
                    current + (0.25 if label_toggle_neg else -0.25)],
                    [center_y, center_y], color='black', linewidth=0.5)
                ax1.text(current + offset, center_y, f"{int((value))}", ha=ha, va='center',
                    fontsize=8, fontweight='bold')
                label_toggle_neg = not label_toggle_neg
            else:
                ax1.text(current, center_y, f"{int((value))}", ha='center', va='center',
                    fontsize=8, fontweight='bold')
                bottom_neg += value

        bottom_pos = 0
        label_toggle_pos = False
        for tech_idx, tech in enumerate(technologies):
            value = absolute_data[scenario][idx][tech_idx]
            if value <= 0:
                continue
            ax1.bar(current, value, width=width, bottom=bottom_pos,
                    color=colors[tech_idx], edgecolor='none', linewidth=0)
            center_y = bottom_pos + value/2
            label_allowed = True
            if tech == 'Other':
                label_allowed = True
            if year == 2030 and tech in ['Biomass']:
                label_allowed = False
            if tech == 'Battery storage' and year >= 2035:
                label_allowed = True
            if tech in ['EV discharging', 'Pumped hydro storage'] and value > 0:
                center_y = bottom_pos + value / 2
                ax1.text(current, center_y, f"{int(value)}", ha='center', va='center',
                         fontsize=8, fontweight='bold', color='black') 
            if label_allowed and value > 0:
                if (tech == 'Other' and value >= 7) or tech == 'Battery storage' or (tech != 'Other' and value > 150):
                    ax1.text(current, center_y, f"{int(value)}", ha='center', va='center',
                              fontsize=8, fontweight='bold')
                elif tech != 'Other' and tech not in ['EV discharging', 'Pumped hydro storage']:
                    offset = 0.35 if label_toggle_pos else -0.35
                    ha = 'left' if label_toggle_pos else 'right'
                    ax1.text(current + offset, center_y, f"{int(value)}", ha=ha, va='center',
                              fontsize=8, fontweight='bold')
                    ax1.plot([current + (width/2 if label_toggle_pos else -width/2),
                              current + (0.3 if label_toggle_pos else -0.3)],
                              [center_y, center_y], color='black', linewidth=0.5)
                    label_toggle_pos = not label_toggle_pos
            bottom_pos += value
        current += 1
    current += 1.5

current = 0
for scenario in scenarios:
    if scenario == 'full_avail_ref':
        current += len(years) + 1.5
        continue

    for idx, year in enumerate(years):
        pos_bottom = 0
        neg_bottom = 0
        label_toggle_pos = True
        label_toggle_neg = True

        for tech_idx, tech in enumerate(technologies):
            diff_value = difference_data[scenario][idx][tech_idx]
            color = colors[tech_idx]

            if diff_value > 2:
                ax2.bar(current, diff_value, width=width, bottom=pos_bottom,
                        color=color, edgecolor='none', linewidth=0)
                center_y = pos_bottom + diff_value / 2
                if tech != 'Other' and diff_value >= 2:
                    label = f"+{int(diff_value)}"
                    if diff_value > 2 or tech == 'Battery storage':
                        ax2.text(current, center_y, label, ha='center', va='center',
                                 fontsize=8, fontweight='bold')
                    else:
                        offset = 0.35 if label_toggle_pos else -0.35
                        ha = 'left' if label_toggle_pos else 'right'
                        ax2.text(current + offset, center_y, label, ha=ha, va='center',
                                 fontsize=8, fontweight='bold')
                        ax2.plot([current + (width / 2 if label_toggle_pos else -width / 2),
                                  current + (0.3 if label_toggle_pos else -0.3)],
                                 [center_y, center_y], color='black', linewidth=0.5)
                        label_toggle_pos = not label_toggle_pos
                pos_bottom += diff_value

            elif diff_value < -2:
                ax2.bar(current, diff_value, width=width, bottom=neg_bottom,
                        color=color, edgecolor='none', linewidth=0)
                center_y = neg_bottom + diff_value / 2
                always_inside = tech in ['Residential (rooftop) PV', 'Utility-scale PV', 'Onshore wind power', 'Offshore wind power','Battery storage', 'Hydrogen', 'Conventional']
                show_label = always_inside or (tech != 'Other' and abs(diff_value) >= 2)
                if show_label:
                    label = f"{int(diff_value)}"
                    if always_inside or abs(diff_value) > 15:
                        ax2.text(current, center_y, label, ha='center', va='center',
                                 fontsize=8, fontweight='bold')
                    else:
                        offset = 0.35 if label_toggle_neg else -0.35
                        ha = 'left' if label_toggle_neg else 'right'
                        ax2.text(current + offset, center_y, label, ha=ha, va='center',
                                 fontsize=8, fontweight='bold')
                        ax2.plot([current + (width / 2 if label_toggle_neg else -width / 2),
                                  current + (0.3 if label_toggle_neg else -0.3)],
                                 [center_y, center_y], color='black', linewidth=0.5)
                        label_toggle_neg = not label_toggle_neg
                neg_bottom += diff_value
        current += 1
    current += 1.5

current = 0
for scenario in scenarios:
    if scenario == 'full_avail_ref':
        current += len(years) + 1.5
        continue

    for idx, year in enumerate(years):
        pos_bottom = neg_bottom = 0
        pos_toggle = neg_toggle = True
        stacked_values = []

        for neg_idx, neg_tech in enumerate(neg_tech_labels):
            diff_val = charging_diff_data[scenario][idx][neg_idx]
            if diff_val == 0:
                continue

            color = neg_colors[neg_idx]
            if diff_val > 0:
                ax3.bar(current, diff_val, width=width,
                        bottom=pos_bottom, color=color, edgecolor='none')
                stacked_values.append((pos_bottom, pos_bottom + diff_val, True, neg_idx))
                pos_bottom += diff_val
            else:
                ax3.bar(current, diff_val, width=width,
                        bottom=neg_bottom, color=color, edgecolor='none')
                stacked_values.append((neg_bottom, neg_bottom + diff_val, False, neg_idx))
                neg_bottom += diff_val

        for i, (bottom, top, is_pos, tech_idx) in enumerate(stacked_values):
            diff_val  = top - bottom
            if abs(diff_val) <= 1:
                continue

            tech_name = neg_tech_labels[tech_idx]
            y_pos     = (bottom + top) / 2
            value_str = f"+{int(diff_val)}" if is_pos else f"{int(diff_val)}"

            overlapping = any(
                (bottom < o_top and top > o_bottom)
                for j, (o_bottom, o_top, _, _) in enumerate(stacked_values)
                if j != i
            )

            if not overlapping:
                ax3.text(current, y_pos, value_str,
                         ha='center', va='center', fontsize=8, fontweight='bold')
                continue

            if is_pos:
                offset = 0.35 if pos_toggle else -0.35
                ha     = 'left' if pos_toggle else 'right'
                pos_toggle = not pos_toggle
            else:
                offset = 0.35 if neg_toggle else -0.35
                ha     = 'left' if neg_toggle else 'right'
                neg_toggle = not neg_toggle

            ax3.text(current + offset, y_pos, value_str,
                     ha=ha, va='center', fontsize=8, fontweight='bold')
            ax3.plot([current + (width/2 if ha == 'left' else -width/2),
                      current + (0.25  if ha == 'left' else -0.25)],
                     [y_pos, y_pos], color='black', linewidth=0.5)

        current += 1
    current += 1.5

ax1.set_xticks([])
ax1.set_ylabel('Charging/pumping & production [TWh/yr]', fontweight='bold', fontsize=14)
ax1.set_ylim(-2200, 8000)
ax1.spines['bottom'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

ax2.set_xticks([])
ax2.set_ylabel('Difference to\nthe full avail. —\nproduction\n[TWh/yr]', fontweight='bold', fontsize=14)
ax2.set_ylim(-420, 220)
ax2.yaxis.set_major_locator(MultipleLocator(100))
ax2.grid(axis='y', which='major', linestyle='--', alpha=0.7)
ax2.axhline(0, color='black', linewidth=0.8)
ax2.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

ax3.set_xticks(x_positions)
ax3.set_xticklabels([str(year) for year in years] * len(scenarios))
ax3.tick_params(axis='x', pad=2)
ax3.set_ylim(-320, 150)
ax3.yaxis.set_major_locator(MultipleLocator(100))
ax3.grid(axis='y', which='major', linestyle='--', alpha=0.7)
for ax in (ax1, ax2):
    ax.tick_params(axis='x',
                   which='both',
                   bottom=False,
                   labelbottom=False)
ax3.axhline(0, color='black', linewidth=0.8)
ax3.grid(axis='y', linestyle='--', alpha=0.7)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.set_ylabel('Difference to\nthe full avail. —\ncharging/pumping\n[TWh/yr]', fontweight='bold', fontsize=14)

midpoints = [(x_positions[i*5] + x_positions[i*5+4]) / 2
             for i in range(len(scenarios))]

for idx, midpoint in enumerate(midpoints):
    ax3.text(
        midpoint,
        -0.17,
        scenario_labels[idx],
        transform=ax3.get_xaxis_transform(),
        ha='center', va='top',
        fontsize=14, fontweight='bold'
    )

pos_handles = [mpatches.Patch(color=colors[i], label=technologies[i]) for i in range(len(technologies))]
neg_handles = [mpatches.Patch(color=neg_colors[i], label=neg_tech_labels[i]) for i in range(len(neg_tech_labels))]
handles = pos_handles[::-1] + neg_handles
fig.subplots_adjust(right=0.83)
ax1.legend(handles=handles, loc='center left', bbox_to_anchor=(1.01, 0.5), frameon=False)

plt.tight_layout()
plt.show()