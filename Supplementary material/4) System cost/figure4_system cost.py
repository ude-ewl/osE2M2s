from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter, MultipleLocator
from matplotlib.lines import Line2D

years = [2030, 2035, 2040, 2045, 2050]

scenario_colors = {
    "exp_baseline": "#7B4A8F",
    "hyp_upfront":  "#6B5B4A",
    "hyp_feedin":   "#4A6B8F",
}

tcost = {
    "exp_baseline": [384.29, 442.92, 487.71, 523.49, 547.59],
    "hyp_upfront":  [382.66, 440.57, 484.58, 519.79, 543.32],
    "hyp_feedin":   [385.07, 443.72, 488.42, 524.22, 548.30],
}

support_cost = {
    "exp_baseline": [80.2, 71.2, 59.2, 46.7, 36.3],
    "hyp_upfront":  [87.3, 78.0, 64.0, 50.5, 39.0],
    "hyp_feedin":   [61.0, 54.0, 44.5, 35.2, 27.3],
}

support_share = {
    scen: [s / t * 100 for s, t in zip(support_cost[scen], tcost[scen])]
    for scen in scenario_colors
}

scenario_names = {
    "exp_baseline": "Exponential baseline",
    "hyp_upfront":  "Hyperbolic upfront",
    "hyp_feedin":   "Hyperbolic feed-in tariff",
}

waterfall_components = [
    "Residential (rooftop) PV", "Utility-scale PV", "Other Renewables",
    "Prosumer battery", "Utility battery",
    r"H$_{2}$ import",
]

component_colors = {
    "Residential (rooftop) PV": "#FEA233",
    "Utility-scale PV":        "#FEE484",
    "Other Renewables":        "#4FCFAD",
    "Prosumer battery":        "#57C35E",
    "Utility battery":         "#3B8C40",
    r"H$_{2}$ import":         "#CF6EEA",
}

component_labels = {
    "Residential (rooftop) PV": "Residential\n(rooftop) PV",
    "Utility-scale PV":        "Utility-\nscale PV",
    "Other Renewables":        "Other\nrenewables",
    "Prosumer battery":        "Prosumer\nbattery",
    "Utility battery":         "Utility\nbattery",
    r"H$_{2}$ import":         r"H$_{2}$ import",
}

wf_b = {
    "start_label": "Exponential\nbaseline",
    "end_label":   "Hyperbolic\nupfront",
    "start_value": 807.8, "end_value": 814.5,
    "components": [
        ("Residential (rooftop) PV", 8.1), ("Utility-scale PV", -2.5), ("Other Renewables", 0.0),
        ("Prosumer battery", 1.8), ("Utility battery", -0.6),
        (r"H$_{2}$ import", -0.1),
    ],
}

wf_d = {
    "start_label": "Exponential\nbaseline",
    "end_label":   "Hyperbolic\nfeed-in tariff",
    "start_value": 807.8, "end_value": 803.7,
    "components": [
        ("Residential (rooftop) PV", -5.6), ("Utility-scale PV", 0.2), ("Other Renewables", 0.0),
        ("Prosumer battery", 0.4), ("Utility battery", 0.1),
        (r"H$_{2}$ import", 0.0),
    ],
}

wf_f = {
    "start_label": "Hyperbolic\nupfront",
    "end_label":   "Hyperbolic\nfeed-in tariff",
    "start_value": 814.5, "end_value": 803.7,
    "components": [
        ("Residential (rooftop) PV", -10.2), ("Utility-scale PV", -4.1), ("Other Renewables", -0.1),
        ("Prosumer battery", 0.8), ("Utility battery", 2.7),
        (r"H$_{2}$ import", 0.2),
    ],
}

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

fig = plt.figure(figsize=(15, 12))
gs = fig.add_gridspec(3, 2, width_ratios=[1.0, 1.3], wspace=0.20, hspace=0.40,
                      left=0.06, right=0.97, top=0.96, bottom=0.06)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[1, 0])
ax_d = fig.add_subplot(gs[1, 1])
ax_e = fig.add_subplot(gs[2, 0])
ax_f = fig.add_subplot(gs[2, 1])


def closed_box(ax):
    for side in ["top", "right", "bottom", "left"]:
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(0.8)
        ax.spines[side].set_color("black")
        ax.spines[side].set_zorder(10)


def closed_box_twinx(ax, ax2):
    for side in ["top", "right", "bottom", "left"]:
        for a in (ax, ax2):
            a.spines[side].set_visible(True)
            a.spines[side].set_linewidth(0.8)
            a.spines[side].set_color("black")
            a.spines[side].set_zorder(10)


def plot_line_pair(ax, scens, title, letter):
    ax2 = ax.twinx()

    max_share = max(max(support_share[s]) for s in scens)
    right_ymax = max(31, int(max_share / 5) * 5 + 5)

    if tcost[scens[0]][-1] >= tcost[scens[1]][-1]:
        above_scen, below_scen = scens[0], scens[1]
    else:
        above_scen, below_scen = scens[1], scens[0]

    for scen in scens:
        ax.plot(years, tcost[scen],
                color=scenario_colors[scen], linewidth=2.0,
                marker="o", markersize=5, linestyle="-")
        for i, year in enumerate(years):
            if scen == above_scen:
                offset_y = 14
                va = "bottom"
            else:
                offset_y = -14
                va = "top"
            ax.text(year, tcost[scen][i] + offset_y, f"{tcost[scen][i]:.1f}",
                    color=scenario_colors[scen], fontsize=6.5,
                    fontweight="bold", ha="center", va=va)

    if support_share[scens[0]][-1] >= support_share[scens[1]][-1]:
        above_share_scen, below_share_scen = scens[0], scens[1]
    else:
        above_share_scen, below_share_scen = scens[1], scens[0]

    for scen in scens:
        ax2.plot(years, support_share[scen],
                 color=scenario_colors[scen], linewidth=1.5,
                 marker="s", markersize=4, linestyle="--")
        for i, year in enumerate(years):
            if scen == above_share_scen:
                offset_share = 1.2
                va = "bottom"
            else:
                offset_share = -1.2
                va = "top"
            ax2.text(year, support_share[scen][i] + offset_share,
                     f"{support_share[scen][i]:.1f}%",
                     color=scenario_colors[scen], fontsize=6.5,
                     fontweight="bold", ha="center", va=va)

    ax.set_xlabel("Year")
    ax.set_ylabel("System cost (bn €/yr)")
    ax2.set_ylabel("Support cost share (of yearly system cost)")

    ax.set_xticks(years)
    ax.set_xlim(2028, 2052)
    ax.set_ylim(355, 605)
    ax2.set_ylim(0, right_ymax)

    ax.yaxis.set_major_locator(MultipleLocator(50))
    ax2.yaxis.set_major_locator(MultipleLocator(5))

    closed_box_twinx(ax, ax2)

    ax2.yaxis.label.set_rotation(270)
    ax2.yaxis.label.set_va("bottom")
    ax2.yaxis.set_label_coords(1.045, 0.5)

    def hide_zero(x, pos):
        if x == 0:
            return ""
        return f"{x:.0f}"
    ax2.yaxis.set_major_formatter(FuncFormatter(hide_zero))

    ax.set_title(title, fontsize=9, pad=8)
    ax.text(-0.05, 1.10, letter, transform=ax.transAxes,
            fontsize=14, fontweight="bold", va="bottom", ha="left")

    handles = []
    for scen in scens:
        handles.append(Line2D([0], [0],
                              color=scenario_colors[scen], linewidth=2.0,
                              marker="o", markersize=4,
                              label=scenario_names[scen]))
    ax.legend(handles=handles, loc="upper left",
              fontsize=6.5, frameon=False)


def plot_waterfall(ax, wf, title, letter, fontsize=6.5):
    start = wf["start_value"]
    end = wf["end_value"]
    components = wf["components"]
    n_components = len(components)
    n_total = n_components + 2

    x_positions = list(range(n_total))
    labels = (
        [wf["start_label"]]
        + [component_labels.get(c[0], c[0]) for c in components]
        + [wf["end_label"]]
    )

    all_vals = [start, end]
    cum = start
    for _, v in components:
        all_vals.append(cum + v)
        cum += v
    vmin = min(all_vals)
    vmax = max(all_vals)
    vrange = vmax - vmin if vmax > vmin else 1.0
    ylim_min = vmin - vrange * 0.30
    ylim_max = vmax + vrange * 0.35

    label_offset = (ylim_max - ylim_min) * 0.022
    bar_width = 0.7
    connector_color = "#BDBDBD"
    connector_lw = 0.7

    ax.bar(0, start, width=bar_width, color="#555555", edgecolor="none")
    ax.text(0, start + label_offset, f"{start:.1f}",
            ha="center", va="bottom", fontsize=fontsize + 1, fontweight="bold")

    cumulative = start
    for i, (comp_name, value) in enumerate(components):
        x = i + 1

        ax.plot(
            [x - 1 + bar_width / 2, x - bar_width / 2],
            [cumulative, cumulative],
            color=connector_color,
            linewidth=connector_lw,
            zorder=1
        )

        if abs(value) < 0.05:
            ax.bar(x, 0.08, width=bar_width, bottom=cumulative - 0.04,
                   color="#dddddd", edgecolor="none")
            ax.text(x, cumulative, "0.0", ha="center", va="center",
                    fontsize=fontsize - 0.5, color="#888888")
        else:
            if value > 0:
                ax.bar(x, value, width=bar_width, bottom=cumulative,
                       color=component_colors[comp_name], edgecolor="none")
                ax.text(x, cumulative + value + label_offset,
                        f"+{value:.1f}", ha="center", va="bottom",
                        fontsize=fontsize, fontweight="bold")
            else:
                ax.bar(x, value, width=bar_width, bottom=cumulative,
                       color=component_colors[comp_name], edgecolor="none")
                ax.text(x, cumulative + value - label_offset,
                        f"{value:.1f}", ha="center", va="top",
                        fontsize=fontsize, fontweight="bold")
        cumulative += value

    ax.bar(n_total - 1, end, width=bar_width, color="#555555", edgecolor="none")
    ax.text(n_total - 1, end + label_offset, f"{end:.1f}",
            ha="center", va="bottom", fontsize=fontsize + 1, fontweight="bold")
    ax.plot(
        [n_total - 2 + bar_width / 2, n_total - 1 - bar_width / 2],
        [cumulative, cumulative],
        color=connector_color,
        linewidth=connector_lw,
        zorder=1
    )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=6.5)
    ax.set_xlim(-0.7, n_total - 1 + 0.7)
    ax.set_ylim(ylim_min, ylim_max)

    closed_box(ax)

    ax.set_ylabel("Cost (bn €)")
    ax.set_title(title, fontsize=9, pad=8)
    ax.text(-0.05, 1.10, letter, transform=ax.transAxes,
            fontsize=14, fontweight="bold", va="bottom", ha="left")


plot_line_pair(ax_a, ["exp_baseline", "hyp_upfront"],
               title="Cost trajectories (discounting effect)",
               letter="a")
plot_waterfall(ax_b, wf_b,
               title=r"Cost shift decomposition (discounting effect)",
               letter="b")

plot_line_pair(ax_c, ["exp_baseline", "hyp_feedin"],
               title="Cost trajectories (discounting effect)",
               letter="c")
plot_waterfall(ax_d, wf_d,
               title=r"Cost shift decomposition (discounting effect)",
               letter="d")

plot_line_pair(ax_e, ["hyp_upfront", "hyp_feedin"],
               title="Cost trajectories (instrument effect)",
               letter="e")
plot_waterfall(ax_f, wf_f,
               title=r"Cost shift decomposition (instrument effect)",
               letter="f")


def yfmt(x, _pos):
    return f"{x:,.0f}"


for ax in [ax_a, ax_b, ax_c, ax_d, ax_e, ax_f]:
    ax.yaxis.set_major_formatter(FuncFormatter(yfmt))

plt.show()