import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from matplotlib.patches import Rectangle

cost_data = {
    ('REF', 2030): [0.465, 0.106, 20.675, 2.431],
    ('REF', 2035): [0.234, 0.026, 12.862, 2.386],
    ('REF', 2040): [0.176, 0.000, 8.348, 0.017],

    ('DYN', 2030): [0.480, 0.107, 20.873, 2.457],
    ('DYN', 2035): [0.236, 0.000, 13.135, 2.420],
    ('DYN', 2040): [0.198, 0.000, 8.470, 0.017],

    ('SIM', 2030): [0.484, 0.107, 20.818, 2.451],
    ('SIM', 2035): [0.223, 0.026, 13.023, 2.403],
    ('SIM', 2040): [0.172, 0.000, 8.388, 0.017],

    ('SWE', 2030): [0.458, 0.108, 21.182, 2.489],
    ('SWE', 2035): [0.283, 0.000, 13.967, 2.570],
    ('SWE', 2040): [0.225, 0.000, 8.782, 0.016],
}

co2_data = pd.DataFrame({
    "REF": [89.14, 87.57, 96.47, None, None],
    "DYN": [90.0393, 89.1681, 98.0869, None, None],
    "SIM": [89.82, 88.52, 96.87, None, None],
    "SWE": [91.25, 94.99, 101.91, None, None],
}, index=[2030, 2035, 2040, 2045, 2050])

scenarios = ['REF', 'DYN', 'SIM', 'SWE']

scenario_labels = [
    "Reference (without SRE)",
    "Avg-dyn",
    "Avg-sim",
    "Avg-swe"
]

years = [2030, 2035, 2040]
fuel_types = ['Coal', 'Lignite', 'Gas', 'Other']
colors = ["#A15015", '#F29E4C', '#DEB887', '#778899']

fig, ax1 = plt.subplots(figsize=(14, 5))
width = 0.35
x_positions = []
x_labels = []
current = 0

eps = 1e-9

for scenario in scenarios:
    for year in years:
        x_positions.append(current)
        x_labels.append(str(year))
        values = cost_data[(scenario, year)]
        bottom = 0
        for i, value in enumerate(values):
            ax1.bar(current, value, width=width, bottom=bottom, color=colors[i])
            center_y = bottom + value / 2

            if value == int(value):
                formatted_value = f"{int(value)}"
            else:
                formatted_value = f"{value:.1f}"

            if formatted_value in ("0", "0.0", "-0", "-0.0"):
                bottom += value
                continue

            rounded_1 = round(float(value), 1)
            if abs(rounded_1 - round(rounded_1)) < 1e-9:
                formatted_value = f"{int(round(rounded_1))}"
            else:
                formatted_value = f"{rounded_1:.1f}"

            if formatted_value in ("0", "0.0", "-0", "-0.0"):
                bottom += value
                continue

            if fuel_types[i] == "Lignite":
                offset_y = 0.025
                text_x = current + 0.25
                tick_start = current + width / 2
                tick_end = text_x - 0.01

                ax1.text(text_x, center_y + offset_y, formatted_value,
                        ha="left", va="center", fontsize=9, fontweight="bold")
                ax1.plot([tick_start, tick_end], [center_y, center_y + offset_y],
                        color="black", linewidth=0.5)
            else:
                ax1.text(current, center_y, formatted_value,
                        ha="center", va="center", fontsize=9, fontweight="bold")

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