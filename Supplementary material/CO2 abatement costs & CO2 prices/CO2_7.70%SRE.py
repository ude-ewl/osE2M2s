import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

cost_data = {
    ('REF', 2030): [0.465, 0.106, 20.675, 2.431],
    ('REF', 2035): [0.234, 0.026, 12.862, 2.386],
    ('REF', 2040): [0.176, 0.000, 8.348, 0.017],

    ('DYN', 2030): [0.470, 0.107, 20.860, 2.452],
    ('DYN', 2035): [0.239, 0.000, 13.064, 2.412],
    ('DYN', 2040): [0.201, 0.000, 8.498, 0.017],

    ('SIM', 2030): [0.474, 0.106, 20.762, 2.443],
    ('SIM', 2035): [0.223, 0.026, 12.954, 2.397],
    ('SIM', 2040): [0.183, 0.000, 8.416, 0.017],

    ('SWE', 2030): [0.454, 0.108, 21.033, 2.470],
    ('SWE', 2035): [0.242, 0.000, 13.306, 2.456],
    ('SWE', 2040): [0.217, 0.000, 8.509, 0.016],
}

co2_data = pd.DataFrame({
            "REF": [89.14, 87.57, 96.47, None, None],
            "DYN": [89.94, 88.74, 98.44, None, None],
            "SIM": [89.55, 88.09, 97.31, None, None],
            "SWE": [90.60, 90.38, 98.74, None, None],
        }, index=[2030, 2035, 2040, 2045, 2050])

scenarios = ['REF', 'DYN', 'SIM', 'SWE']
scenario_labels = [
    "Reference (without SRE)",
    "Low-dyn",
    "Low-sim",
    "Low-swe"
]
years = [2030, 2035, 2040]
fuel_types = ['Coal', 'Lignite', 'Gas', 'Other']
colors = ["#A15015", '#DEB887', '#FF6347', '#778899']

fig, ax1 = plt.subplots(figsize=(14, 5), constrained_layout=True) 
width = 0.35
x_positions = []
x_labels = []
current = 0

for scenario in scenarios:
    for year in years:
        x_positions.append(current)
        x_labels.append(str(year))
        values = cost_data[(scenario, year)]
        bottom = 0
        for i, value in enumerate(values):
            ax1.bar(current, value, width=width, bottom=bottom, color=colors[i])
            center_y = bottom + value / 2

            if fuel_types[i] == 'Lignite':
                if round(value, 2) > 0:
                    offset_y = 0.025
                    text_x = current + 0.25
                    tick_start = current + width / 2
                    tick_end = text_x - 0.01
                    ax1.text(text_x, center_y + offset_y, f"{value:.2f}", ha='left', va='center',
                            fontsize=9, fontweight='bold')
                    ax1.plot([tick_start, tick_end], [center_y, center_y + offset_y],
                            color='black', linewidth=0.5)
            else:
                ax1.text(current, center_y, f"{value:.2f}", ha='center', va='center',
                         fontsize=9, fontweight='bold')
            bottom += value
        
        co2_price = co2_data.loc[year, scenario]
        if pd.notna(co2_price):
            ax1.text(current, -1.75, f"{co2_price:.2f} €/t", 
                     ha='center', va='top', fontsize=9, fontweight='bold',
                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='green', boxstyle='square'))
        
        current += 1
    current += 0.6

ax1.set_xticks(x_positions)
ax1.set_xticklabels(x_labels, fontsize=10)
ax1.set_ylabel("Costs [bn€]", fontweight='bold', fontsize=14)
ax1.grid(axis='y', linestyle='--', alpha=0.6)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

midpoints = [(x_positions[i*3] + x_positions[i*3+2]) / 2 for i in range(len(scenarios))]
y_offset = ax1.get_ylim()[0] - 0.12 * (ax1.get_ylim()[1] - ax1.get_ylim()[0])  
for idx, midpoint in enumerate(midpoints):
    ax1.text(midpoint, y_offset, scenario_labels[idx], ha='center', va='top',
             fontsize=14, fontweight='bold')

fuel_handles = [
    mpatches.Patch(color=colors[i], label=fuel_types[i])
    for i in reversed(range(len(fuel_types)))
]
co2_patch = mpatches.Patch(facecolor='white', edgecolor='green', label='CO₂ price (in each \nscenario year)')
handles = fuel_handles + [co2_patch]

ax1.legend(handles=handles,
           loc='center left',
           bbox_to_anchor=(1.01, 0.5),
           frameon=False,
           fontsize=10)

plt.show()