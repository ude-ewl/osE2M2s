from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter, MultipleLocator

years = [2030, 2035, 2040, 2045, 2050]

scenarios = ["exp_baseline", "hyp_upfront", "hyp_feedin"]
scenario_labels = [
    "Exponential baseline\n(Exponential upfront " + r"$\equiv$"
    + " Exponential feed-in tariff)",
    "Hyperbolic upfront",
    "Hyperbolic feed-in tariff",
]

technologies = [
    "Residential (rooftop) PV", "Utility-scale PV",
    "Onshore wind power", "Offshore wind power",
    "Biomass", "Hydropower",
    "Pumped hydro storage", "Hydrogen",
    "Electrolyzer",
    "Prosumer battery", "Utility battery",
    "Conventional", "Other",
]
colors = [
    "#FEA233", "#FEE484", "#4FCFAD", "#77BACC", "#F3B1BC",
    "#C1EAFE", "#5555FF", "#CF6EEA", "#CA41B1", "#57C35E",
    "#3B8C40", "#FE748B", "#C7C7C7",
]


def reorder(src):
    return [src[0], src[1], src[4], src[5], src[6], src[10], src[9],
            src[7], src[8], src[2], src[3], src[11], src[12]]


capacity_src = {
    "exp_upfront": [
        [293, 376, 111, 88, 418, 177, 13, 112, 8, 73, 176, 322, 24],
        [392, 508, 200, 149, 521, 300, 13, 131, 84, 73, 176, 306, 22],
        [503, 627, 327, 225, 630, 424, 12, 165, 149, 73, 176, 268, 7],
        [605, 758, 418, 298, 756, 540, 9, 188, 265, 73, 176, 216, 4],
        [717, 879, 530, 376, 798, 654, 7, 196, 327, 73, 176, 135, 2],
    ],
    "hyp_upfront": [
        [318, 351, 121, 87, 418, 177, 13, 112, 8, 73, 176, 322, 24],
        [430, 470, 219, 145, 521, 300, 13, 131, 84, 73, 176, 306, 22],
        [541, 589, 352, 217, 630, 424, 12, 165, 149, 73, 176, 268, 7],
        [651, 715, 449, 288, 754, 543, 9, 187, 267, 73, 176, 216, 4],
        [765, 835, 566, 365, 798, 655, 7, 195, 328, 73, 176, 135, 2],
    ],
    "hyp_feedin": [
        [293, 376, 111, 88, 418, 177, 13, 112, 8, 73, 176, 322, 24],
        [391, 509, 199, 149, 520, 300, 13, 131, 84, 73, 176, 306, 22],
        [496, 635, 322, 226, 630, 424, 12, 165, 149, 73, 176, 268, 7],
        [598, 766, 412, 299, 756, 540, 9, 188, 265, 73, 176, 216, 4],
        [709, 886, 525, 378, 798, 653, 7, 196, 327, 73, 176, 135, 2],
    ],
}

capacity_data = {
    "exp_baseline": [reorder(r) for r in capacity_src["exp_upfront"]],
    "hyp_upfront":  [reorder(r) for r in capacity_src["hyp_upfront"]],
    "hyp_feedin":   [reorder(r) for r in capacity_src["hyp_feedin"]],
}

n_years = len(years)
n_techs = len(technologies)

cap_diff_b = [[capacity_data["hyp_upfront"][y][t] - capacity_data["exp_baseline"][y][t]
               for t in range(n_techs)] for y in range(n_years)]
cap_diff_c = [[capacity_data["hyp_feedin"][y][t] - capacity_data["exp_baseline"][y][t]
               for t in range(n_techs)] for y in range(n_years)]
cap_diff_d = [[capacity_data["hyp_feedin"][y][t] - capacity_data["hyp_upfront"][y][t]
               for t in range(n_techs)] for y in range(n_years)]

plt.rcParams.update({
    "font.family": "Arial", "font.size": 8,
    "axes.titlesize": 9, "axes.labelsize": 9,
    "xtick.labelsize": 7, "ytick.labelsize": 7,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8,
    "xtick.major.size": 3, "ytick.major.size": 3,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "pdf.fonttype": 42, "ps.fonttype": 42,
})

SCEN_BARS = 5
SCEN_GAP = 1.5
X_PAD = 0.7
SUB_WSPACE = 0.204
width = 0.7
half_w = width / 2

fig = plt.figure(figsize=(17, 13))
outer_gs = fig.add_gridspec(3, 1, height_ratios=[3.0, 1.4, 1.4], hspace=0.40)

ax_a = fig.add_subplot(outer_gs[0])
bc_gs = outer_gs[1].subgridspec(1, 3, wspace=SUB_WSPACE)
d_gs = outer_gs[2].subgridspec(1, 3, wspace=SUB_WSPACE)

ax_bc = [fig.add_subplot(bc_gs[0, i]) for i in range(3)]
ax_d = [fig.add_subplot(d_gs[0, i]) for i in range(3)]


def collect_and_place_labels(ax, candidates, y_range, fontsize=6.0,
                             min_gap_units=None, bar_half_width=0.35):
    if min_gap_units is None:
        min_gap_units = y_range * 0.014

    from collections import defaultdict
    per_x = defaultdict(list)
    for c in candidates:
        per_x[round(c["x"], 3)].append(c)

    for x_key, group in per_x.items():
        group.sort(key=lambda d: d["y_center"])
        for c in group:
            c["place"] = "inline"

        changed = True
        max_iter = 10
        while changed and max_iter > 0:
            changed = False
            max_iter -= 1
            inline_only = [c for c in group if c["place"] == "inline"]
            inline_only.sort(key=lambda d: d["y_center"])
            for i in range(len(inline_only) - 1):
                a = inline_only[i]
                b = inline_only[i + 1]
                if b["y_center"] - a["y_center"] < min_gap_units:
                    if a["seg_height"] <= b["seg_height"]:
                        a["place"] = "outside"
                    else:
                        b["place"] = "outside"
                    changed = True
                    break

        side_right = True
        for c in group:
            if c["place"] == "inline":
                ax.text(c["x"], c["y_center"], c["text"],
                        ha="center", va="center",
                        fontsize=fontsize, fontweight="bold")
            else:
                if side_right:
                    x_label = c["x"] + bar_half_width + 0.08
                    x_line = c["x"] + bar_half_width
                    ha = "left"
                else:
                    x_label = c["x"] - bar_half_width - 0.08
                    x_line = c["x"] - bar_half_width
                    ha = "right"
                side_right = not side_right
                ax.text(x_label, c["y_center"], c["text"],
                        ha=ha, va="center",
                        fontsize=fontsize, fontweight="bold")
                ax.plot([x_line, x_label - (0.02 if ha == "left" else -0.02)],
                        [c["y_center"], c["y_center"]],
                        color="black", linewidth=0.4)


scenario_start_pos = [0.0, SCEN_BARS + SCEN_GAP, 2 * (SCEN_BARS + SCEN_GAP)]
scenario_end_pos = [s + SCEN_BARS - 1 for s in scenario_start_pos]

x_positions_a = []
PANEL_A_YMIN = 0
PANEL_A_YMAX = 5500
LABEL_MIN = 2

all_candidates_a = []

for si, scen in enumerate(scenarios):
    for yi in range(n_years):
        current = scenario_start_pos[si] + yi
        x_positions_a.append(current)

        bottom = 0.0
        for ti in range(n_techs):
            v = capacity_data[scen][yi][ti]
            if v <= 0:
                continue
            ax_a.bar(current, v, width=width, bottom=bottom,
                     color=colors[ti], edgecolor="none", linewidth=0)
            if v >= LABEL_MIN:
                all_candidates_a.append({
                    "x": current,
                    "y_center": bottom + v / 2.0,
                    "text": f"{int(v)}",
                    "seg_height": v,
                })
            bottom += v

collect_and_place_labels(ax_a, all_candidates_a,
                         y_range=PANEL_A_YMAX - PANEL_A_YMIN,
                         fontsize=5.5, bar_half_width=half_w)

for start_x, end_x, label in zip(scenario_start_pos, scenario_end_pos, scenario_labels):
    mid = (start_x + end_x) / 2
    ax_a.text(mid, 1.02, label, transform=ax_a.get_xaxis_transform(),
              ha="center", va="bottom", fontsize=9, clip_on=False)

ax_a.set_xticks(x_positions_a)
ax_a.set_xticklabels([str(y) for y in years] * len(scenarios))

for start_x, end_x in zip(scenario_start_pos, scenario_end_pos):
    mid = (start_x + end_x) / 2
    ax_a.text(
        mid, -0.05, "Year",
        transform=ax_a.get_xaxis_transform(),
        ha="center", va="top",
        fontsize=plt.rcParams["axes.labelsize"],
        clip_on=False
    )

ax_a.set_ylabel("Installed capacity (GW)")
ax_a.set_ylim(PANEL_A_YMIN, PANEL_A_YMAX)
ax_a.set_xlim(-X_PAD, scenario_end_pos[-1] + X_PAD)
ax_a.spines["top"].set_visible(False)
ax_a.spines["right"].set_visible(False)
ax_a.yaxis.set_major_locator(MultipleLocator(500))
ax_a.text(-0.025, 1.08, "a", transform=ax_a.transAxes,
          fontsize=14, fontweight="bold", va="bottom", ha="left")


def empty_panel(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def plot_diff(ax, diff_data, palette, n_cats, ylim, title=None,
              xlabel="Year", fontsize=6):
    ax.axhline(0, color="black", linewidth=0.8)
    candidates = []
    x_pos = []
    for yi in range(n_years):
        cur = float(yi)
        x_pos.append(cur)
        pos_bottom = 0.0
        neg_bottom = 0.0
        for ci in range(n_cats):
            v = diff_data[yi][ci]
            if abs(v) < 0.5:
                continue
            ax.bar(cur, v, width=width,
                   bottom=pos_bottom if v > 0 else neg_bottom,
                   color=palette[ci], edgecolor="none", linewidth=0)
            if abs(v) >= LABEL_MIN:
                if v > 0:
                    y_center = pos_bottom + v / 2.0
                    text = f"+{int(v)}"
                else:
                    y_center = neg_bottom + v / 2.0
                    text = f"{int(v)}"
                candidates.append({
                    "x": cur,
                    "y_center": y_center,
                    "text": text,
                    "seg_height": abs(v),
                })
            if v > 0:
                pos_bottom += v
            else:
                neg_bottom += v

    collect_and_place_labels(ax, candidates, y_range=2 * ylim,
                             fontsize=fontsize, bar_half_width=half_w)

    ax.set_xticks(x_pos)
    ax.set_xticklabels([str(y) for y in years])
    ax.set_xlabel(xlabel)
    ax.set_xlim(-X_PAD, SCEN_BARS - 1 + X_PAD)

    if ylim == 100:
        ax.set_ylim(-103, 103)
        ax.set_yticks([-100, -50, 0, 50, 100])
    else:
        ax.set_ylim(-ylim, ylim)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if title:
        ax.set_title(title, fontsize=9, pad=6)


def plot_diff_asym(ax, diff_data, palette, n_cats, ymin, ymax, title=None,
                   xlabel="Year", fontsize=6):
    ax.axhline(0, color="black", linewidth=0.8)
    candidates = []
    x_pos = []
    for yi in range(n_years):
        cur = float(yi)
        x_pos.append(cur)
        pos_bottom = 0.0
        neg_bottom = 0.0
        for ci in range(n_cats):
            v = diff_data[yi][ci]
            if abs(v) < 0.5:
                continue
            ax.bar(cur, v, width=width,
                   bottom=pos_bottom if v > 0 else neg_bottom,
                   color=palette[ci], edgecolor="none", linewidth=0)
            if abs(v) >= LABEL_MIN:
                if v > 0:
                    y_center = pos_bottom + v / 2.0
                    text = f"+{int(v)}"
                else:
                    y_center = neg_bottom + v / 2.0
                    text = f"{int(v)}"
                candidates.append({
                    "x": cur,
                    "y_center": y_center,
                    "text": text,
                    "seg_height": abs(v),
                })
            if v > 0:
                pos_bottom += v
            else:
                neg_bottom += v

    collect_and_place_labels(ax, candidates, y_range=ymax - ymin,
                             fontsize=fontsize, bar_half_width=half_w)

    ax.set_xticks(x_pos)
    ax.set_xticklabels([str(y) for y in years])
    ax.set_xlabel(xlabel)
    ax.set_xlim(-X_PAD, SCEN_BARS - 1 + X_PAD)
    ax.set_ylim(ymin, ymax)
    if ymin == -103 and ymax == 103:
        ax.set_yticks([-100, -50, 0, 50, 100])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if title:
        ax.set_title(title, fontsize=9, pad=6)


def panel_letter(ax, letter, x_offset=-0.10, y_offset=1.12):
    ax.text(x_offset, y_offset, letter, transform=ax.transAxes,
            fontsize=14, fontweight="bold", va="bottom", ha="left")


BC_YLIM = 100

empty_panel(ax_bc[0])
plot_diff(ax_bc[1], cap_diff_b, colors, n_techs, BC_YLIM,
          title=r"$\Delta$ Hyperbolic upfront $-$ Exponential baseline"
                + "\n(discounting effect)")
plot_diff(ax_bc[2], cap_diff_c, colors, n_techs, BC_YLIM,
          title=r"$\Delta$ Hyperbolic feed-in tariff $-$ Exponential baseline"
                + "\n(discounting effect)")
ax_bc[1].set_ylabel("Difference — capacity (GW)")
ax_bc[2].set_ylabel("Difference — capacity (GW)")
panel_letter(ax_bc[1], "b")
panel_letter(ax_bc[2], "c")


empty_panel(ax_d[0])
empty_panel(ax_d[1])

plot_diff_asym(ax_d[2], cap_diff_d, colors, n_techs, -103, 103,
               title=r"$\Delta$ Hyperbolic feed-in tariff $-$ Hyperbolic upfront"
                     + "\n(instrument effect)")
ax_d[2].set_ylabel("Difference — capacity (GW)")
panel_letter(ax_d[2], "d")


def yfmt(x, _pos):
    return f"{x:,.0f}"


for ax in [ax_a] + ax_bc + ax_d:
    if not ax.get_visible():
        continue
    ax.ticklabel_format(axis="y", style="plain", useOffset=False)
    ax.yaxis.set_major_formatter(FuncFormatter(yfmt))


handles = [mpatches.Patch(color=colors[i], label=technologies[i])
           for i in range(n_techs)][::-1]

fig.subplots_adjust(right=0.83, top=0.94, bottom=0.05, left=0.07)
fig.legend(handles=handles, loc="center left",
           bbox_to_anchor=(0.84, 0.5), frameon=False,
           fontsize=8, handlelength=1.5, handletextpad=0.5)

plt.show()