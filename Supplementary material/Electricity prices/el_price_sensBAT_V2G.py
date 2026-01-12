import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from pathlib import Path
import matplotlib.colors as mcolors
from matplotlib.gridspec import GridSpec


CSV_FILE_TOP = Path(r"C:\Users\delic\...\el_prices_sensBAT_50GW_V2G.csv")
CSV_FILE_BOTTOM = Path(r"C:\Users\delic\...\el_prices_sensBAT_100GW_V2G.csv")

SCENARIOS = [
    ("Full availability (100%)", "#5B84B1"),
    ("Average availability (61%)", "#E18B6B"),
    ("Low availability (25%)", "#78B43D"),
]
YEARS = [2030, 2035, 2040, 2045, 2050]

SCENARIO_MAP = {
    "full_avail_ref_BAT_sens_50": "Full availability (100%)",
    "full_avail_ref_BAT_sens_100": "Full availability (100%)",
    "avg_avail_BAT_sens_50": "Average availability (61%)",
    "avg_avail_BAT_sens_100": "Average availability (61%)",
    "low_avail_BAT_sens_50": "Low availability (25%)",
    "low_avail_BAT_sens_100": "Low availability (25%)",
}


def normalize_key(x: str) -> str:
    return (
        str(x).strip().lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


SCENARIO_MAP = {normalize_key(k): v for k, v in SCENARIO_MAP.items()}


def load_data_from_excel_colA_scenario_colB_year(file: Path, sheet=None):
    try:
        df = pd.read_csv(file)
    except Exception as e:
        raise RuntimeError(f"Could not read file: {e}")

    if df.select_dtypes(include="number").empty:
        try:
            df = pd.read_csv(file, decimal=",")
        except Exception:
            pass

    if df.shape[1] < 3:
        raise ValueError("Expected at least 3 columns: A=Scenario, B=Year, C..=Values.")

    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    df.rename(columns={df.columns[0]: "ScenarioRaw", df.columns[1]: "Year"}, inplace=True)

    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    value_cols = df.columns[2:]
    for c in value_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df["ScenarioKey"] = df["ScenarioRaw"].map(normalize_key)
    df["ScenarioStd"] = df["ScenarioKey"].map(SCENARIO_MAP)
    df = df.dropna(subset=["ScenarioStd", "Year"])

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
        DATA[y] = [
            collect_values(dfy[dfy["ScenarioStd"] == "Full availability (100%)"]),
            collect_values(dfy[dfy["ScenarioStd"] == "Average availability (61%)"]),
            collect_values(dfy[dfy["ScenarioStd"] == "Low availability (25%)"]),
        ]
    return DATA


def plot_boxpanel(
    ax,
    DATA,
    *,
    title=None,
    y_label="Electricity prices [€/MWh]",
    show_bottom_year_labels=False,
    show_ylabel=True,
    group_gap=2.4,
    box_gap=0.80,
    box_width=0.55,
    violin_width=0.50,
    violin_alpha=0.28,
):
    centers = [1 + i * group_gap for i in range(len(YEARS))]

    for ci, year in enumerate(YEARS):
        center = centers[ci]
        offsets = [-box_gap, 0.0, box_gap]

        for (sidx, (label, color)), off in zip(enumerate(SCENARIOS), offsets):
            pos = center + off
            values = DATA.get(year, [[], [], []])[sidx]
            if not values:
                continue

            solid_color = mcolors.to_rgba(color, 1.0)
            vp = ax.violinplot(
                [values],
                positions=[pos],
                widths=violin_width,
                showmeans=False,
                showmedians=False,
                showextrema=False,
            )
            for body in vp["bodies"]:
                body.set_facecolor(solid_color)
                body.set_edgecolor(solid_color)
                body.set_alpha(1.0)
                body.set_linewidth(1.0)
                body.set_zorder(1)

            bp = ax.boxplot(
                [values],
                positions=[pos],
                widths=box_width,
                patch_artist=True,
                showmeans=True,
                showfliers=False,
                boxprops=dict(linewidth=1, color="black"),
                whiskerprops=dict(linewidth=1, color="black"),
                capprops=dict(linewidth=1, color="black"),
                medianprops=dict(linewidth=1.3, color="black"),
                meanprops=dict(marker="x", markersize=6, markeredgecolor="black"),
            )
            for patch in bp["boxes"]:
                patch.set_facecolor("none")
                patch.set_edgecolor("black")
                patch.set_alpha(1.0)
                patch.set_zorder(2)

            for i in range(0, len(bp["whiskers"]), 2):
                lw = bp["whiskers"][i]
                uw = bp["whiskers"][i + 1]
                x_lw, y_lw = lw.get_xdata()[1], lw.get_ydata()[1]
                x_uw, y_uw = uw.get_xdata()[1], uw.get_ydata()[1]
                ax.text(x_lw, y_lw - 0.3, f"{y_lw:.2f}", ha="center", va="top", fontsize=9, zorder=3)
                ax.text(x_uw, y_uw + 0.1, f"{y_uw:.2f}", ha="center", va="bottom", fontsize=9, zorder=3)

            for med in bp["medians"]:
                x = np.mean(med.get_xdata())
                y = med.get_ydata()[0]
                ax.text(x, y + 0.1, f"{y:.2f}", ha="center", va="bottom", fontsize=9, zorder=3)

            for mean in bp["means"]:
                x = mean.get_xdata()[0]
                y = mean.get_ydata()[0]
                ax.text(x, y - 0.4, f"{y:.2f}", ha="center", va="top", fontsize=9, zorder=3)

    if show_bottom_year_labels:
        ax.set_xticks(centers)
        ax.set_xticklabels(YEARS, fontweight="bold", fontsize=12)
        ax.tick_params(axis="x", length=0)
    else:
        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.tick_params(axis="x", bottom=False, labelbottom=False, length=0)

    if show_ylabel:
        ax.set_ylabel(y_label, fontweight="bold", fontsize=12)
        ax.tick_params(axis="y", labelleft=True)
    else:
        ax.set_ylabel("")
        ax.tick_params(axis="y", labelleft=False, length=3)

    ax.set_ylim(-55, 210)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    ymin, ymax = ax.get_ylim()
    pad_x = 0.2
    x_min = centers[0] - (box_gap + box_width / 2) - pad_x
    x_max = centers[-1] + (box_gap + box_width / 2) + pad_x
    ax.set_xlim(x_min, x_max)

    rect_all = Rectangle(
        (x_min, ymin),
        x_max - x_min,
        ymax - ymin,
        fill=False,
        linewidth=1.4,
        edgecolor="black",
        zorder=0.1,
    )
    ax.add_patch(rect_all)

    if title:
        ax.set_title(title, fontsize=13, pad=10)


DATA_TOP = load_data_from_excel_colA_scenario_colB_year(CSV_FILE_TOP)
DATA_BOTTOM = load_data_from_excel_colA_scenario_colB_year(CSV_FILE_BOTTOM)

fig = plt.figure(figsize=(14, 10.5), facecolor="white")
gs = GridSpec(nrows=2, ncols=1, height_ratios=[1, 1], hspace=0.35)

ax_top = fig.add_subplot(gs[0, 0])
ax_bot = fig.add_subplot(gs[1, 0], sharex=ax_top)

plot_boxpanel(
    ax_top,
    DATA_TOP,
    title="Battery storage capacity in 2030:+50 GW",
    show_bottom_year_labels=False,
    show_ylabel=True,
    group_gap=2.4,
    box_gap=0.65,
    box_width=0.55,
    violin_width=0.50,
)

plot_boxpanel(
    ax_bot,
    DATA_BOTTOM,
    title="Battery storage capacity in 2030:+100 GW",
    show_bottom_year_labels=True,
    show_ylabel=True,
    group_gap=2.4,
    box_gap=0.65,
    box_width=0.55,
    violin_width=0.50,
)

legend_handles = [
    Line2D([], [], marker="s", linestyle="", markersize=10,
           markerfacecolor=SCENARIOS[0][1], markeredgecolor="black", label=SCENARIOS[0][0]),
    Line2D([], [], marker="s", linestyle="", markersize=10,
           markerfacecolor=SCENARIOS[1][1], markeredgecolor="black", label=SCENARIOS[1][0]),
    Line2D([], [], marker="s", linestyle="", markersize=10,
           markerfacecolor=SCENARIOS[2][1], markeredgecolor="black", label=SCENARIOS[2][0]),
]
fig.legend(handles=legend_handles, loc="center right", bbox_to_anchor=(1.06, 0.5), frameon=False)

plt.tight_layout()
plt.show()