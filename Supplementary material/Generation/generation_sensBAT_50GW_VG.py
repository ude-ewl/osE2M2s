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
        [224, 1291, 762, 525, 1, 69, 39, 503, 25, 1331, 61],
        [240, 1565, 959, 926, 7, 75, 46, 500, 35, 1108, 58],
        [251, 1732, 1173, 1335, 40, 88, 63, 499, 43, 867, 7],
        [340, 1956, 1532, 1537, 62, 108, 138, 498, 65, 629, 4],
        [333, 2117, 1784, 1726, 51, 163, 162, 496, 67, 426, 2]
    ],
    'avg_avail': [
        [181, 1255, 782, 525, 1, 69, 40, 502, 35, 1347, 61],
        [228, 1530, 968, 926, 8, 73, 46, 500, 37, 1108, 59],
        [244, 1702, 1190, 1335, 41, 89, 63, 499, 45, 867, 7],
        [335, 1939, 1539, 1535, 62, 110, 139, 498, 64, 628, 4],
        [325, 2099, 1786, 1726, 51, 164, 163, 496, 68, 426, 2]
    ],
    'low_avail': [
        [52, 1157, 835, 525, 1, 70, 44, 503, 46, 1366, 59],
        [109, 1409, 986, 926, 9, 75, 48, 501, 45, 1111, 58],
        [175, 1638, 1261, 1335, 42, 86, 64, 499, 49, 882, 7],
        [213, 1870, 1606, 1537, 63, 154, 153, 498, 74, 626, 4],
        [203, 2038, 1853, 1726, 52, 228, 177, 495, 79, 424, 2]
    ]
}

charging_data = {
    'full_avail_ref': [
        [-340, -73, -401, -34],
        [-467, -78, -564, -46],
        [-582, -93, -622, -57],
        [-741, -113, -953, -85],
        [-748, -171, -1126, -88]
    ],
    'avg_avail': [
        [-291, -72, -403, -46],
        [-453, -77, -539, -49],
        [-574, -94, -610, -59],
        [-736, -116, -943, -85],
        [-739, -173, -1111, -89]
    ],
    'low_avail': [
        [-148, -74, -390, -60],
        [-321, -79, -452, -59],
        [-498, -90, -641, -65],
        [-600, -162, -963, -98],
        [-603, -240, -1135, -104]
    ]
}

n_years = len(years)
n_techs = len(technologies)
n_neg = len(neg_tech_labels)

TITLE_TEXT = "Battery storage capacity in 2030:+50 GW"
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
ax2.set_ylim(-320, 220)
ax2.yaxis.set_major_locator(MultipleLocator(100))
ax2.axhline(0, color='black', linewidth=0.8)
ax2.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

ax3.set_xticks(x_positions)
ax3.set_xticklabels([str(year) for year in years * len(scenarios)])
ax3.tick_params(axis='x', pad=2)
ax3.set_ylim(-320, 120)
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