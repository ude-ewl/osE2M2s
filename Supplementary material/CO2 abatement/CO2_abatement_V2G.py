import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from matplotlib.patches import Rectangle

cost_data = {
    ('full', 2030): [0.2, 0.9, 17.3, 2.1],
    ('full', 2035): [0.1, 0.3, 10.1, 1.9],
    ('full', 2040): [0.1, 0.3, 5.9, 0.0],

    ('average', 2030): [0.2, 0.8, 18.8, 2.3],
    ('average', 2035): [0.1, 0.3, 10.2, 1.9],
    ('average', 2040): [0.2, 0.2, 6.1, 0.0],

    ('low', 2030): [0.3, 0.2, 20.4, 2.4],
    ('low', 2035): [0.1, 0.1, 12.0, 2.2],
    ('low', 2040): [0.2, 0.0, 6.9, 0.0],
}

co2_data = pd.DataFrame({
    "full": [77.33, 70.38, 71.91, None, None],
    "average": [82.85, 71.12, 73.01, None, None],
    "low": [87.71, 81.69, 79.71, None, None],
}, index=[2030, 2035, 2040, 2045, 2050])

scenarios = ['full', 'average', 'low']
scenario_labels = [
    "Full availability (100%)",
    "Average availability (61%)",
    "Low availability (25%)"
]
years = [2030, 2035, 2040]
fuel_types = ['Coal', 'Lignite', 'Gas', 'Other']
colors = ["#A15015", '#F29E4C', '#DEB887', '#778899']

fig, ax1 = plt.subplots(figsize=(14, 5))
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
                    formatted_value = f"{int(value)}" if value == int(value) else f"{value:.1f}"
                    ax1.text(text_x, center_y + offset_y, formatted_value, ha='left', va='center',
                            fontsize=9, fontweight='bold')
                    ax1.plot([tick_start, tick_end], [center_y, center_y + offset_y],
                            color='black', linewidth=0.5)
            else:
                if round(value, 2) > 0:
                    formatted_value = f"{int(value)}" if value == int(value) else f"{value:.1f}"
                    ax1.text(current, center_y, formatted_value, ha='center', va='center',
                             fontsize=9, fontweight='bold')
            bottom += value
        
        co2_price = co2_data.loc[year, scenario]
        if pd.notna(co2_price):
            ax1.text(current, -1.75, f"{co2_price:.2f} €/t", 
                     ha='center', va='top', fontsize=9, fontweight='bold',
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='green', boxstyle='square'))
        
        current += 1
    current += 0.6

ax1.set_xticks(x_positions)
ax1.set_xticklabels(x_labels, fontsize=10)
ax1.set_ylabel("Costs [bn€]", fontweight='bold', fontsize=14)
ax1.grid(axis='y', linestyle='--', alpha=0.6)
ax1.spines['top'].set_visible(True)
ax1.spines['right'].set_visible(True)

midpoints = [(x_positions[i*3] + x_positions[i*3+2]) / 2 for i in range(len(scenarios))]
y_offset = ax1.get_ylim()[0] - 0.14 * (ax1.get_ylim()[1] - ax1.get_ylim()[0])
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

plt.tight_layout()
plt.show()