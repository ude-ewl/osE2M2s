import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from pathlib import Path
import matplotlib.colors as mcolors

# Adjust your path to the CSV file here
CSV_FILE = Path(r"C:\Users\...\el_prices_V2G.csv")
    
SCENARIOS = [
    ("Full availability (100%)", "#5B84B1"),
    ("Average availability (61%)",  "#E18B6B"),
    ("Low availability (25%)",   "#78B43D"),
]
YEARS = [2030, 2035, 2040, 2045, 2050]

SCENARIO_MAP = {
    "full_avail_ref": "Full availability (100%)",
    "avg_avail":  "Average availability (61%)",
    "low_avail":      "Low availability (25%)",
}

def load_data_from_csv_colA_scenario_colB_year(file: Path):
    try:
        df = pd.read_csv(file)
    except Exception:
        try:
            df = pd.read_csv(file, decimal=',', sep=';')
        except Exception as e:
            raise RuntimeError(f"CSV konnte nicht gelesen werden: {e}")

    if df.shape[1] < 3:
        raise ValueError("Erwartet mind. 3 Spalten: A=Scenario, B=Year, C..=Werte.")

    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    df.rename(columns={df.columns[0]: "ScenarioRaw", df.columns[1]: "Year"}, inplace=True)

    value_cols = df.columns[2:]
    for c in value_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df["ScenarioKey"] = df["ScenarioRaw"].astype(str).str.strip().str.lower()
    df["ScenarioStd"] = df["ScenarioKey"].map(SCENARIO_MAP)
    df = df.dropna(subset=["ScenarioStd"])

    DATA = {y: [[], [], []] for y in YEARS}

    def collect_values(sub_df):
        if len(value_cols) == 1:
            vals = sub_df[value_cols[0]].dropna().to_numpy()
        else:
            vals = sub_df[value_cols].to_numpy().ravel()
            vals = vals[~pd.isna(vals)]
        return vals.tolist()

    for y in YEARS:
        dfy = df[df["Year"] == y]
        ref_vals  = collect_values(dfy[dfy["ScenarioStd"] == "Full availability (100%)"])
        average_vals = collect_values(dfy[dfy["ScenarioStd"] == "Average availability (61%)"])
        low_vals  = collect_values(dfy[dfy["ScenarioStd"] == "Low availability (25%)"])
        DATA[y] = [ref_vals, average_vals, low_vals]

    return DATA


DATA = load_data_from_csv_colA_scenario_colB_year(CSV_FILE)


fig, ax = plt.subplots(figsize=(14, 6), facecolor="white")
ax = plt.gca()

group_gap = 3.0
box_gap   = 0.8
centers = [1 + i*group_gap for i in range(len(YEARS))]

for ci, year in enumerate(YEARS):
    center = centers[ci]
    offsets = [-box_gap, 0.0, box_gap]

    for (sidx, (label, color)), off in zip(enumerate(SCENARIOS), offsets):
        pos = center + off
        values = DATA.get(year, [[], [], []])[sidx]

        if not values:
            continue

        vp = ax.violinplot(
            [values],
            positions=[pos],
            widths=0.9,
            showmeans=False,
            showextrema=False,
            showmedians=False,
        )
        for body in vp["bodies"]:  # type: ignore
            body.set_facecolor(color)
            body.set_edgecolor("none")
            body.set_alpha(1.0)
            body.set_zorder(0.5)

        bp = ax.boxplot(
            [values],
            positions=[pos],
            widths=0.7,
            patch_artist=True,
            showmeans=True,
            showfliers=False,
            boxprops=dict(linewidth=1, color="black"),
            whiskerprops=dict(linewidth=1, color="black"),
            capprops=dict(linewidth=1, color="black"),
            medianprops=dict(linewidth=1.3, color="black"),
            meanprops=dict(marker="x", markersize=6, markeredgecolor="black"),
        )

        box_face = mcolors.to_rgba(color, alpha=0.35)
        for patch in bp["boxes"]:
            patch.set_facecolor(box_face)
            patch.set_edgecolor("black")

        for i in range(0, len(bp['whiskers']), 2):
            lw = bp['whiskers'][i]
            uw = bp['whiskers'][i+1]
            x_lw, y_lw = lw.get_xdata()[1], lw.get_ydata()[1]
            x_uw, y_uw = uw.get_xdata()[1], uw.get_ydata()[1]
            ax.text(x_lw, y_lw - 0.3, f"{y_lw:.2f}", ha="center", va="top", fontsize=9)
            ax.text(x_uw, y_uw + 0.1, f"{y_uw:.2f}", ha="center", va="bottom", fontsize=9)

        for med in bp["medians"]:
            x = np.mean(med.get_xdata())
            y = med.get_ydata()[0]
            ax.text(x, y + 0.1, f"{y:.2f}", ha="center", va="bottom", fontsize=9)

        for mean in bp["means"]:
            x = mean.get_xdata()[0]
            y = mean.get_ydata()[0]
            ax.text(x, y - 0.4, f"{y:.2f}", ha="center", va="top", fontsize=9)

ax.set_xticks([])
ax.set_xticklabels([])
ax.tick_params(axis='x', which='both', length=0)

ax.set_ylabel("Electricity prices [€/MWh]", fontweight="bold", fontsize=14)

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

ymin, ymax = ax.get_ylim()
box_width = 0.7
pad_x = 0.25
x_min = centers[0] - box_gap - box_width/2 - pad_x
x_max = centers[-1] + box_gap + box_width/2 + pad_x
ax.set_xlim(x_min, x_max)

rect_all = Rectangle((x_min, ymin), x_max - x_min, ymax - ymin,
                     fill=False, linewidth=1.4, edgecolor="black", zorder=0.1)
ax.add_patch(rect_all)

for center, year in zip(centers, YEARS):
    ax.text(center, 1.01, f"{year}",
            transform=ax.get_xaxis_transform(),
            ha="center", va="bottom",
            fontweight="bold", fontsize=14,
            clip_on=False)
handles = [
    Line2D([], [], marker='s', linestyle='', markersize=10,
               markerfacecolor=SCENARIOS[0][1], markeredgecolor='black', label=SCENARIOS[0][0]),
    Line2D([], [], marker='s', linestyle='', markersize=10,
               markerfacecolor=SCENARIOS[1][1], markeredgecolor='black', label=SCENARIOS[1][0]),
    Line2D([], [], marker='s', linestyle='', markersize=10,
               markerfacecolor=SCENARIOS[2][1], markeredgecolor='black', label=SCENARIOS[2][0]),
]
leg = ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)
if leg.get_title():
    leg.get_title().set_fontweight("bold")

plt.tight_layout()
plt.show()