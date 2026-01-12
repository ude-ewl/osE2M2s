import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

LABEL_FMT = "{:.0f}"
FONT_SIZE_LABEL = 8.5

scenarios = ['full_avail_ref', 'average_avail', 'low_avail']
scenario_labels = [
    "Full availability\n(100%)",
    "Average availability\n(61%)",
    "Low availability\n(25%)"
]

pos_cats = [
    'EV discharging', 'Solar power (PV)', 'Onshore wind power', 'Offshore wind power',
    'Biomass', 'Battery storage', 'Hydrogen', 'Hydropower',
    'Pumped hydro storage', 'Conventional', 'Other'
]
pos_cols = ['orange', 'yellow', 'LightSeaGreen', 'darkcyan', 'Salmon', 
          'lightgreen', 'violet', 'cyan', 'dodgerblue', 'red', 'grey'
]

neg_cats = ['EV charging', 'Battery charging', 'Electrolysis', 'Pumping']
neg_cols = ['orange', 'lightgreen', 'mediumvioletred', 'dodgerblue']

C_POS = dict(zip(pos_cats, pos_cols))
C_NEG = dict(zip(neg_cats, neg_cols))

winter_2030_gen = {
    'full_avail_ref': {'EV discharging': 73.1, 'Solar power (PV)': 0.0, 'Onshore wind power': 112.3, 'Offshore wind power': 80.3, 'Biomass': 0.2, 'Battery storage': 1.4, 'Hydrogen': 7.3, 'Hydropower': 100.6, 'Pumped hydro storage': 3.9, 'Conventional': 229.0, 'Other': 8.0},
    'average_avail': {'EV discharging': 69.7, 'Solar power (PV)': 0.0, 'Onshore wind power': 116.3, 'Offshore wind power': 80.3, 'Biomass': 0.2, 'Battery storage': 1.6, 'Hydrogen': 7.3, 'Hydropower': 97.6, 'Pumped hydro storage': 3.1, 'Conventional': 224.5, 'Other': 8.0},
    'low_avail': {'EV discharging': 41.8, 'Solar power (PV)': 0.0, 'Onshore wind power': 123.6, 'Offshore wind power': 80.3, 'Biomass': 1.6, 'Battery storage': 3.9, 'Hydrogen': 7.9, 'Hydropower': 97.3, 'Pumped hydro storage': 3.4, 'Conventional': 223.7, 'Other': 8.0},
}

winter_2030_neg = {
    'full_avail_ref': {'EV charging': -0.0, 'Battery charging': -0.7, 'Electrolysis': -27.0, 'Pumping': -0.2},
    'average_avail': {'EV charging': -0.0, 'Battery charging': -0.7, 'Electrolysis': -19.7, 'Pumping': -0.2},
    'low_avail': {'EV charging': -0.0, 'Battery charging': -0.5, 'Electrolysis': -1.7, 'Pumping': -0.2},
}

summer_2030_gen = {
    'full_avail_ref': {'EV discharging': 137.8, 'Solar power (PV)': 3.1, 'Onshore wind power': 59.7, 'Offshore wind power': 53.2, 'Biomass': 0.0, 'Battery storage': 1.4, 'Hydrogen': 2.1, 'Hydropower': 89.7, 'Pumped hydro storage': 7.4, 'Conventional': 168.8, 'Other': 7.1},
    'average_avail': {'EV discharging': 128.2, 'Solar power (PV)': 3.0, 'Onshore wind power': 61.2, 'Offshore wind power': 53.2, 'Biomass': 0.0, 'Battery storage': 1.6, 'Hydrogen': 2.1, 'Hydropower': 84.8, 'Pumped hydro storage': 6.7, 'Conventional': 171.2, 'Other': 7.1},
    'low_avail': {'EV discharging': 59.8, 'Solar power (PV)': 2.4, 'Onshore wind power': 63.6, 'Offshore wind power': 53.2, 'Biomass': 0.3, 'Battery storage': 5.4, 'Hydrogen': 2.4, 'Hydropower': 95.8, 'Pumped hydro storage': 16.0, 'Conventional': 196.8, 'Other': 7.1}
}

summer_2030_neg = {
    'full_avail_ref': {'EV charging': -0.0, 'Battery charging': -0.6, 'Electrolysis': -29.0, 'Pumping': -0.0},
    'average_avail': {'EV charging': -0.0, 'Battery charging': -0.6, 'Electrolysis': -17.7, 'Pumping': -0.0},
    'low_avail': {'EV charging': -0.0, 'Battery charging': -0.5, 'Electrolysis': -1.6, 'Pumping': -0.0}
}

winter_2040_gen = {
    'full_avail_ref': {'EV discharging': 109.0, 'Solar power (PV)': 0.0, 'Onshore wind power': 186.6, 'Offshore wind power': 195.4, 'Biomass': 6.5, 'Battery storage': 18.6, 'Hydrogen': 13.3, 'Hydropower': 81.8, 'Pumped hydro storage': 4.8, 'Conventional': 129.2, 'Other': 1.0},
    'average_avail': {'EV discharging': 106.7, 'Solar power (PV)': 0.0, 'Onshore wind power': 185.8, 'Offshore wind power': 195.4, 'Biomass': 6.5, 'Battery storage': 18.5, 'Hydrogen': 13.2, 'Hydropower': 82.3, 'Pumped hydro storage': 4.5, 'Conventional': 129.5, 'Other': 1.0},
    'low_avail': {'EV discharging': 97.6, 'Solar power (PV)': 0.0, 'Onshore wind power': 194.2, 'Offshore wind power': 196.5, 'Biomass': 6.6, 'Battery storage': 22.7, 'Hydrogen': 13.1, 'Hydropower': 79.8, 'Pumped hydro storage': 3.6, 'Conventional': 129.9, 'Other': 1.0},
}

winter_2040_neg = {
    'full_avail_ref': {'EV charging': -0.4, 'Battery charging': -1.0, 'Electrolysis': -38.0, 'Pumping': -1.5},
    'average_avail': {'EV charging': -0.4, 'Battery charging': -1.1, 'Electrolysis': -37.1, 'Pumping': -0.5},
    'low_avail': {'EV charging': -0.4, 'Battery charging': -1.1, 'Electrolysis': -37.2, 'Pumping': -1.2},
}

summer_2040_gen = {
    'full_avail_ref': {'EV discharging': 165.8, 'Solar power (PV)': 4.2, 'Onshore wind power': 93.1, 'Offshore wind power': 134.2, 'Biomass': 4.9, 'Battery storage': 21.3, 'Hydrogen': 3.7, 'Hydropower': 73.7, 'Pumped hydro storage': 11.3, 'Conventional': 102.6, 'Other': 0.8},
    'average_avail': {'EV discharging': 165.0, 'Solar power (PV)': 4.2, 'Onshore wind power': 93.2, 'Offshore wind power': 134.2, 'Biomass': 4.8, 'Battery storage': 21.0, 'Hydrogen': 3.7, 'Hydropower': 73.5, 'Pumped hydro storage': 11.0, 'Conventional': 104.6, 'Other': 0.8},
    'low_avail': {'EV discharging': 153.9, 'Solar power (PV)': 4.0, 'Onshore wind power': 98.0, 'Offshore wind power': 135.0, 'Biomass': 5.1, 'Battery storage': 27.5, 'Hydrogen': 3.7, 'Hydropower': 68.6, 'Pumped hydro storage': 13.0, 'Conventional': 103.5, 'Other': 0.8},
}

summer_2040_neg = {
    'full_avail_ref': {'EV charging': -0.0, 'Battery charging': -1.1, 'Electrolysis': -42.3, 'Pumping': -0.1},
    'average_avail': {'EV charging': -0.0, 'Battery charging': -1.1, 'Electrolysis': -31.4, 'Pumping': -0.0},
    'low_avail': {'EV charging': -0.0, 'Battery charging': -0.8, 'Electrolysis': -12.3, 'Pumping': -0.1},
}

def draw_stack(ax, gen_dict, neg_dict, title):
    x = np.arange(len(scenarios))
    width = 0.58

    bpos = np.zeros_like(x, dtype=float)
    for cat in pos_cats:
        vals = np.array([gen_dict[s].get(cat, 0.0) for s in scenarios])
        ax.bar(x, vals, width=width, bottom=bpos, color=C_POS[cat], edgecolor='none')
        for i, v in enumerate(vals):
            if abs(v) > 2:
                cy = bpos[i] + v/2
                if cat == 'Battery storage':
                    ax.text(x[i] + 0.08, cy, LABEL_FMT.format(v), ha='left', va='center',
                            fontsize=FONT_SIZE_LABEL, fontweight='bold', color='black')
                else:
                    ax.text(x[i], cy, LABEL_FMT.format(v), ha='center', va='center',
                            fontsize=FONT_SIZE_LABEL, fontweight='bold', color='black')
        bpos += vals

    bneg = np.zeros_like(x, dtype=float)
    for cat in neg_cats:
        vals = np.array([neg_dict[s].get(cat, 0.0) for s in scenarios])
        ax.bar(x, vals, width=width, bottom=bneg, color=C_NEG[cat], edgecolor='none')
        for i, v in enumerate(vals):
            if abs(v) > 2:
                cy = bneg[i] + v/2
                ax.text(x[i], cy, LABEL_FMT.format(v), ha='center', va='center',
                        fontsize=FONT_SIZE_LABEL, fontweight='bold', color='black')
        bneg += vals

    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(scenario_labels, fontsize=9)
    ax.set_title(title, fontsize=11, fontweight='bold', pad=6)

    for side in ('top', 'right', 'left', 'bottom'):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(0.8)
        ax.spines[side].set_color('black')

    return ax

fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.6), sharey=True)

for ax in axes.flat:
    ax.set_box_aspect(1)

fig.subplots_adjust(left=0.10, right=0.80,
                    wspace=0.05,
                    hspace=0.20,
                    bottom=0.12, top=0.98)

draw_stack(axes[0, 0], summer_2030_gen, summer_2030_neg, "Summer peak load: 2030")
draw_stack(axes[0, 1], winter_2030_gen, winter_2030_neg, "Winter peak load: 2030")
draw_stack(axes[1, 0], summer_2040_gen, summer_2040_neg, "Summer peak load: 2040")
draw_stack(axes[1, 1], winter_2040_gen, winter_2040_neg, "Winter peak load: 2040")

for ax in axes.flat:
    ax.set_ylabel("Charging/pumping & production [GW]", fontsize=11, fontweight="bold")

for ax in axes[:, 1]:
    ax.tick_params(labelleft=True)

pos_handles = [mpatches.Patch(color=C_POS[c], label=c) for c in pos_cats[::-1]]
neg_handles = [mpatches.Patch(color=C_NEG[c], label=c) for c in neg_cats[::-1] if c not in ['EV charging', 'Battery charging']]
handles = pos_handles + neg_handles
fig.legend(handles=handles, loc='center left', bbox_to_anchor=(0.78, 0.56),
           frameon=False, fontsize=9, title_fontsize=10)

plt.tight_layout
plt.show()