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
    'Hydrogen', 'Pumped hydro storage', 
    'Hydropower', 'Conventional', 
    'Other'
]
colors = ['gold', 'yellow', 
          'mediumturquoise', 'cadetblue', 
          'salmon', 'forestgreen', 
          'violet', 'dodgerblue', 
          'cyan', 'red', 
          'gray']

neg_tech_labels = ['Battery charging', 'Electrolysis', 'Pumped hydro pumping', 'EV charging']
neg_colors = ['forestgreen', 'mediumvioletred', 'royalblue', 'chocolate']
                                            
absolute_data = {
            'REF': [
                [385, 661, 840, 525, 6, 28, 254, 69, 501, 1448, 93],
                [502, 829, 1119, 931, 32, 57, 286, 72, 499, 1165, 90],
                [589, 949, 1347, 1346, 67, 123, 365, 100, 498, 1002, 8],
                [673, 1071, 1698, 1538, 78, 206, 507, 105, 498, 754, 5],
                [740, 1140, 1835, 1726, 63, 279, 512, 96, 498, 765, 3]
            ],
            'DYN': [
                [400, 691, 844, 525, 6, 28, 254, 70, 501, 1447, 92],
                [527, 877, 1125, 932, 33, 60, 287, 71, 499, 1168, 90],
                [618, 1007, 1358, 1345, 67, 131, 366, 102, 498, 1002, 8],
                [716, 1133, 1687, 1537, 78, 224, 512, 104, 498, 754, 5],
                [793, 1213, 1830, 1725, 63, 298, 515, 92, 498, 765, 3]
            ],
            'SIM': [
                [400, 690, 842, 525, 6, 28, 254, 69, 501, 1448, 93],
                [526, 876, 1115, 932, 33, 59, 286, 70, 499, 1168, 90],
                [617, 1006, 1348, 1345, 68, 127, 365, 101, 498, 1003, 8],
                [716, 1133, 1685, 1537, 78, 218, 508, 103, 498, 753, 5],
                [791, 1211, 1828, 1725, 63, 290, 512, 93, 498, 765, 3]
            ],
            'SWE': [
                [391, 671, 856, 525, 7, 30, 258, 71, 501, 1445, 92],
                [517, 854, 1166, 933, 38, 69, 292, 74, 499, 1160, 89],
                [607, 982, 1411, 1346, 66, 140, 369, 113, 498, 999, 8],
                [691, 1101, 1755, 1556, 78, 222, 521, 109, 498, 754, 5],
                [769, 1180, 1893, 1746, 63, 304, 526, 96, 498, 763, 3]
            ]
        }

charging_data = {
    'REF': [
        [-29, -273, -92, -90],
        [-60, -522, -96, -200],
        [-130, -748, -132, -303],
        [-217, -1098, -139, -363],
        [-293, -1325, -126, -377]
    ],
    'DYN': [
        [-30, -277, -92, -90],
        [-64, -511, -93, -200],
        [-138, -721, -135, -303],
        [-236, -1058, -137, -363],
        [-314, -1288, -122, -377]
    ],
    'SIM': [
        [-29, -275, -92, -90],
        [-62, -507, -93, -200],
        [-134, -720, -133, -303],
        [-229, -1064, -137, -363],
        [-305, -1293, -123, -377]
    ],
    'SWE': [
        [-32, -262, -93, -90],
        [-73, -529, -98, -200],
        [-148, -745, -150, -303],
        [-234, -1110, -144, -363],
        [-320, -1342, -127, -377]
    ]
}

n_years = len(years)
n_techs = len(technologies)
n_neg = len(neg_tech_labels)

difference_data = {}
for scen in scenarios:
    if scen == 'REF':
        continue
    diff_years = []
    for yi in range(n_years):
        diff_year = []
        for ti in range(n_techs):
            diff = absolute_data[scen][yi][ti] - absolute_data['REF'][yi][ti]
            diff_year.append(diff)
        diff_years.append(diff_year)
    difference_data[scen] = diff_years

charging_diff_data = {}
for scen in scenarios:
    if scen == 'REF':
        continue
    diff_years = []
    for yi in range(n_years):
        diff_year = []
        for ci in range(n_neg):
            ref_val = charging_data['REF'][yi][ci]
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
            skip_label = (neg_tech == 'Battery charging' and year == 2030)
            ax1.bar(current, value, width=width, bottom=bottom_neg,
                    color=neg_colors[neg_idx], edgecolor='none', linewidth=0)
            center_y = bottom_neg + value / 2

            if neg_tech == 'EV charging':
                center_y -= 45
            elif neg_tech == 'Battery charging':
                center_y -= 25

            if abs(value) >= 35:
                if abs(value) < 50:
                    offset = 0.3 if label_toggle_neg else -0.3
                    ha = 'left' if label_toggle_neg else 'right'
                    ax1.text(current + offset, center_y, f"{int((value))}", ha=ha, va='center',
                            fontsize=8, fontweight='bold')
                    ax1.plot([current + (width/2 if label_toggle_neg else -width/2),
                            current + (0.25 if label_toggle_neg else -0.25)],
                            [center_y, center_y], color='black', linewidth=0.5)
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
            
            if tech == 'Biomass' and year in [2040, 2045, 2050]:
                center_y -= 15
            
            label_allowed = True
            if tech == 'Other':
                label_allowed = True
            if tech == 'Battery storage' and year == 2030:
                offset = 0.35
                ha = 'left'
                ax1.text(current + offset, center_y, f"{int(value)}", ha=ha, va='center',
                         fontsize=8, fontweight='bold')
                ax1.plot([current + width/2, current + 0.3],
                         [center_y, center_y], color='black', linewidth=0.5)
                label_allowed = False
            elif tech == 'Biomass' and year == 2030:
                offset = -0.35
                ha = 'right'
                ax1.text(current + offset, center_y, f"{int(value)}", ha=ha, va='center',
                         fontsize=8, fontweight='bold')
                ax1.plot([current - width/2, current - 0.3],
                         [center_y, center_y], color='black', linewidth=0.5)
                label_allowed = False
            if tech == 'Battery storage' and year >= 2035:
                label_allowed = True
            if tech == 'Biomass' and year in [2040, 2045, 2050]:
                label_allowed = True
            if tech == 'Other' and year >= 2040:
                label_allowed = False
                
            if label_allowed and value > 0:
                if (tech == 'Other' and value >= 7) or tech == 'Battery storage' or tech == 'Pumped hydro storage' or (tech == 'Biomass' and year in [2040, 2045, 2050]) or (tech != 'Other' and value > 150):
                    ax1.text(current, center_y, f"{int(value)}", ha='center', va='center',
                              fontsize=8, fontweight='bold')
                elif tech != 'Other':
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
    if scenario == 'REF':
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
                always_inside = tech in ['Residential (rooftop) PV', 'Utility-scale PV', 'Onshore wind power', 'Offshore wind power','Battery storage', 'Hydrogen']
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
    if scenario == 'REF':
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
ax1.set_ylim(-2500, 8000)
ax1.spines['bottom'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

ax2.set_xticks([])
ax2.set_ylabel('Difference to\nthe reference —\nproduction\n[TWh/yr]', fontweight='bold', fontsize=14)
ax2.axhline(0, color='black', linewidth=0.8)
ax2.set_ylim(-60, 200)
ax2.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

ax3.set_xticks(x_positions)
ax3.set_xticklabels(years * len(scenarios))
ax3.tick_params(axis='x', pad=2)
ax3.set_ylim(-70, 60)
for ax in (ax1, ax2):
    ax.tick_params(axis='x',
                   which='both',
                   bottom=False,       
                   labelbottom=False)     
ax3.axhline(0, color='black', linewidth=0.8)
ax3.grid(axis='y', linestyle='--', alpha=0.7)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.set_ylabel('Difference to\nthe reference —\ncharging/pumping\n[TWh/yr]', fontweight='bold', fontsize=14)

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

plt.show()