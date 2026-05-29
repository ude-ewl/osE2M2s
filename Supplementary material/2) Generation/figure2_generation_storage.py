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
    "Prosumer battery", "Utility battery",
    "Conventional", "Other",
]
colors = [
    "#FEA233", "#FEE484", "#4FCFAD", "#77BACC",
    "#F3B1BC", "#C1EAFE", "#5555FF", "#CF6EEA",
    "#57C35E", "#3B8C40", "#FE748B", "#C7C7C7",
]

neg_tech_labels = [
    "Prosumer battery charging", "Utility battery charging",
    "Electrolysis", "Pumped hydro pumping", "EV charging",
]
neg_colors = [
    "#57C35E", "#3B8C40", "#CA41B1", "#5555FF", "#E47B38",
]


def reorder(src):
    return [
        src[0], src[1], src[4], src[5], src[6], src[9],
        src[8], src[7], src[2], src[3], src[10], src[11],
    ]


generation_src = {
    "exp_upfront": [
        [286, 369, 117, 45, 918, 548, 8, 259, 11, 504, 1465, 94],
        [386, 501, 204, 81, 1169, 953, 43, 280, 15, 502, 1185, 89],
        [500, 624, 328, 112, 1434, 1371, 70, 370, 19, 500, 902, 8],
        [608, 761, 429, 147, 1742, 1735, 76, 494, 20, 498, 628, 5],
        [728, 888, 613, 184, 1834, 2112, 62, 491, 23, 497, 424, 3],
    ],
    "hyp_upfront": [
        [312, 344, 124, 41, 917, 549, 8, 258, 11, 504, 1466, 93],
        [424, 463, 218, 74, 1170, 954, 42, 279, 14, 502, 1185, 89],
        [538, 586, 343, 103, 1433, 1370, 70, 370, 19, 500, 902, 8],
        [653, 717, 447, 134, 1736, 1744, 76, 493, 19, 499, 627, 5],
        [775, 845, 642, 169, 1834, 2116, 62, 490, 22, 496, 424, 3],
    ],
    "hyp_feedin": [
        [286, 369, 117, 45, 918, 548, 8, 259, 11, 504, 1465, 94],
        [385, 502, 204, 81, 1169, 953, 43, 280, 15, 502, 1185, 89],
        [492, 631, 325, 114, 1434, 1371, 70, 370, 19, 500, 902, 8],
        [600, 768, 427, 150, 1742, 1734, 76, 495, 20, 498, 628, 5],
        [720, 896, 608, 187, 1835, 2110, 62, 491, 24, 497, 424, 3],
    ],
}

generation_data = {
    "exp_baseline": [reorder(r) for r in generation_src["exp_upfront"]],
    "hyp_upfront":  [reorder(r) for r in generation_src["hyp_upfront"]],
    "hyp_feedin":   [reorder(r) for r in generation_src["hyp_feedin"]],
}

storage_src = {
    "exp_upfront": [
        [123, 48, 24, 15, 90], [215, 85, 185, 19, 200],
        [346, 118, 362, 26, 303], [452, 155, 833, 26, 363],
        [645, 194, 1077, 31, 377],
    ],
    "hyp_upfront": [
        [131, 43, 24, 15, 90], [229, 77, 185, 19, 200],
        [362, 109, 361, 25, 303], [470, 141, 837, 25, 363],
        [675, 178, 1084, 29, 377],
    ],
    "hyp_feedin": [
        [123, 48, 24, 15, 90], [215, 86, 184, 19, 200],
        [343, 120, 363, 26, 303], [449, 157, 832, 27, 363],
        [640, 197, 1076, 31, 377],
    ],
}

storage_data = {
    "exp_baseline": [[-v for v in row] for row in storage_src["exp_upfront"]],
    "hyp_upfront":  [[-v for v in row] for row in storage_src["hyp_upfront"]],
    "hyp_feedin":   [[-v for v in row] for row in storage_src["hyp_feedin"]],
}

n_years = len(years)
n_techs = len(technologies)
n_neg = len(neg_tech_labels)

gen_diff_b = [[generation_data["hyp_upfront"][y][t] - generation_data["exp_baseline"][y][t]
               for t in range(n_techs)] for y in range(n_years)]
gen_diff_c = [[generation_data["hyp_feedin"][y][t] - generation_data["exp_baseline"][y][t]
               for t in range(n_techs)] for y in range(n_years)]
sto_diff_d = [[storage_data["hyp_upfront"][y][c] - storage_data["exp_baseline"][y][c]
               for c in range(n_neg)] for y in range(n_years)]
sto_diff_e = [[storage_data["hyp_feedin"][y][c] - storage_data["exp_baseline"][y][c]
               for c in range(n_neg)] for y in range(n_years)]
gen_diff_f = [[generation_data["hyp_feedin"][y][t] - generation_data["hyp_upfront"][y][t]
               for t in range(n_techs)] for y in range(n_years)]
sto_diff_g = [[storage_data["hyp_feedin"][y][c] - storage_data["hyp_upfront"][y][c]
               for c in range(n_neg)] for y in range(n_years)]

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
BAR_WIDTH = 0.7
X_PAD = 0.7
SUB_WSPACE = 0.30

fig = plt.figure(figsize=(17, 19))
outer_gs = fig.add_gridspec(5, 1, height_ratios=[3.0, 1.3, 1.3, 1.4, 1.4], hspace=0.40)

ax_a = fig.add_subplot(outer_gs[0])

b_gs = outer_gs[1].subgridspec(1, 3, wspace=SUB_WSPACE)
c_gs = outer_gs[2].subgridspec(1, 3, wspace=SUB_WSPACE)
d_gs = outer_gs[3].subgridspec(1, 3, wspace=SUB_WSPACE)
e_gs = outer_gs[4].subgridspec(1, 3, wspace=SUB_WSPACE)
ax_b = [fig.add_subplot(b_gs[0, i]) for i in range(3)]
ax_c = [fig.add_subplot(c_gs[0, i]) for i in range(3)]
ax_d = [fig.add_subplot(d_gs[0, i]) for i in range(3)]
ax_e = [fig.add_subplot(e_gs[0, i]) for i in range(3)]


def collect_and_place_labels(ax, candidates, y_range, fontsize: float = 6,
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


width = BAR_WIDTH
half_w = width / 2

scenario_start_pos = [0.0, SCEN_BARS + SCEN_GAP, 2 * (SCEN_BARS + SCEN_GAP)]
scenario_end_pos = [s + SCEN_BARS - 1 for s in scenario_start_pos]

x_positions_a = []
ax_a.axhline(0, color="black", linewidth=0.8, linestyle="-")

all_candidates_a = []

PANEL_A_YMIN = -2500
PANEL_A_YMAX = 8000
LABEL_MIN = 2

for si, scen in enumerate(scenarios):
    for yi in range(n_years):
        current = scenario_start_pos[si] + yi
        x_positions_a.append(current)

        bottom_neg = 0.0
        for ni in range(n_neg):
            v = storage_data[scen][yi][ni]
            ax_a.bar(current, v, width=width, bottom=bottom_neg,
                     color=neg_colors[ni], edgecolor="none", linewidth=0)
            if abs(v) >= LABEL_MIN:
                all_candidates_a.append({
                    "x": current,
                    "y_center": bottom_neg + v / 2.0,
                    "text": f"{int(v)}",
                    "seg_height": abs(v),
                })
            bottom_neg += v

        bottom_pos = 0.0
        for ti in range(n_techs):
            v = generation_data[scen][yi][ti]
            if v <= 0:
                continue
            ax_a.bar(current, v, width=width, bottom=bottom_pos,
                     color=colors[ti], edgecolor="none", linewidth=0)
            if v >= LABEL_MIN:
                all_candidates_a.append({
                    "x": current,
                    "y_center": bottom_pos + v / 2.0,
                    "text": f"{int(v)}",
                    "seg_height": v,
                })
            bottom_pos += v

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
        mid, -0.075, "Year",
        transform=ax_a.get_xaxis_transform(),
        ha="center", va="top",
        fontsize=plt.rcParams["axes.labelsize"],
        clip_on=False
    )

ax_a.set_ylabel("Charging/pumping & generation (TWh/yr)")
ax_a.set_ylim(PANEL_A_YMIN, PANEL_A_YMAX)
ax_a.set_xlim(-X_PAD, scenario_end_pos[-1] + X_PAD)
ax_a.spines["top"].set_visible(False)
ax_a.spines["right"].set_visible(False)
ax_a.yaxis.set_major_locator(MultipleLocator(1000))
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

    if ylim == 95:
        ax.set_ylim(-100, 100)
        ax.set_yticks([-95, -50, 0, 50, 95])
    elif ylim == 45:
        ax.set_ylim(-48, 48)
        ax.set_yticks([-45, -30, -15, 0, 15, 30, 45])
    else:
        ax.set_ylim(-ylim, ylim)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if title:
        ax.set_title(title, fontsize=9, pad=6)


def panel_letter(ax, letter, x_offset=-0.10, y_offset=1.12):
    ax.text(x_offset, y_offset, letter, transform=ax.transAxes,
            fontsize=14, fontweight="bold", va="bottom", ha="left")


B_C_YLIM = 95

empty_panel(ax_b[0])
plot_diff(ax_b[1], gen_diff_b, colors, n_techs, B_C_YLIM,
          title=r"$\Delta$ Hyperbolic upfront $-$ Exponential baseline"
                + "\n(discounting effect)")
plot_diff(ax_b[2], gen_diff_c, colors, n_techs, B_C_YLIM,
          title=r"$\Delta$ Hyperbolic feed-in tariff $-$ Exponential baseline"
                + "\n(discounting effect)")
ax_b[1].set_ylabel("Difference —\ngeneration (TWh/yr)")
ax_b[2].set_ylabel("Difference —\ngeneration (TWh/yr)")
panel_letter(ax_b[1], "b")
panel_letter(ax_b[2], "c")


D_E_YLIM = 45

empty_panel(ax_c[0])
plot_diff(ax_c[1], sto_diff_d, neg_colors, n_neg, D_E_YLIM,
          title=r"$\Delta$ Hyperbolic upfront $-$ Exponential baseline"
                + "\n(discounting effect)")
plot_diff(ax_c[2], sto_diff_e, neg_colors, n_neg, D_E_YLIM,
          title=r"$\Delta$ Hyperbolic feed-in tariff $-$ Exponential baseline"
                + "\n(discounting effect)")
ax_c[1].set_ylabel("Difference — charging/\npumping (TWh/yr)")
ax_c[2].set_ylabel("Difference — charging/\npumping (TWh/yr)")
panel_letter(ax_c[1], "d")
panel_letter(ax_c[2], "e")


empty_panel(ax_d[0])
empty_panel(ax_d[1])
empty_panel(ax_e[0])
empty_panel(ax_e[1])

F_YLIM = 95

plot_diff(ax_d[2], gen_diff_f, colors, n_techs, F_YLIM,
          title=r"$\Delta$ Hyperbolic Feed-in Tariff $-$ Hyperbolic Upfront"
                + "\n(instrument effect)")
ax_d[2].set_ylabel("Difference —\ngeneration (TWh/yr)")
panel_letter(ax_d[2], "f")

G_YLIM = 45
plot_diff(ax_e[2], sto_diff_g, neg_colors, n_neg, G_YLIM,
          title=r"$\Delta$ Hyperbolic Feed-in Tariff $-$ Hyperbolic Upfront"
                + "\n(instrument effect)")
ax_e[2].set_ylabel("Difference — charging/\npumping (TWh/yr)")
panel_letter(ax_e[2], "g")


def yfmt(x, _pos):
    return f"{x:,.0f}"


for ax in [ax_a] + ax_b + ax_c + ax_d + ax_e:
    if not ax.get_visible():
        continue
    ax.ticklabel_format(axis="y", style="plain", useOffset=False)
    ax.yaxis.set_major_formatter(FuncFormatter(yfmt))


pos_handles = [mpatches.Patch(color=colors[i], label=technologies[i])
               for i in range(n_techs)]
neg_handles = [mpatches.Patch(color=neg_colors[i], label=neg_tech_labels[i])
               for i in range(n_neg)]
handles = pos_handles[::-1] + neg_handles

fig.subplots_adjust(right=0.83, top=0.94, bottom=0.05, left=0.07)
fig.legend(handles=handles, loc="center left",
           bbox_to_anchor=(0.84, 0.5), frameon=False,
           fontsize=8, handlelength=1.5, handletextpad=0.5)

plt.show()