from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.ticker import FuncFormatter, MultipleLocator
from matplotlib.lines import Line2D
from typing import Any
from matplotlib.artist import Artist
from matplotlib.legend_handler import HandlerBase

scenario_colors = {
    "exp_baseline":  "#7B4A8F",
    "hyp_upfront":   "#6B5B4A",
    "hyp_feedin":    "#4A6B8F",
    "hyp_feedin_eq": "#a85410",
}
scenario_labels = {
    "exp_baseline":  "Exponential baseline",
    "hyp_upfront":   "Hyperbolic upfront",
    "hyp_feedin":    "Hyperbolic feed-in tariff",
    "hyp_feedin_eq": "Hyperbolic feed-in tariff\n(upfront-equivalent)",
}
scenario_short = {
    "exp_baseline":  "Exponential\nbaseline",
    "hyp_upfront":   "Hyperbolic\nupfront",
    "hyp_feedin":    "Hyperbolic\nfeed-in tariff",
    "hyp_feedin_eq": "Hyperbolic\nfeed-in tariff\n(upfront-equivalent)",
}

years = [2030, 2035, 2040, 2045, 2050]

gov_support_yearly = {
    "exp_baseline":  [80.2, 71.2, 59.2, 46.7, 36.3],
    "hyp_upfront":   [87.3, 78.0, 64.0, 50.5, 39.0],
    "hyp_feedin":    [61.0, 54.0, 44.5, 35.2, 27.3],
    "hyp_feedin_eq": [114.9, 102.7, 84.2, 66.4, 51.3],
}
gov_support_total = {
    "exp_baseline":  293.7,
    "hyp_upfront":   318.7,
    "hyp_feedin":    222.0,
    "hyp_feedin_eq": 419.5,
}

hh_support_yearly = {
    "exp_baseline":  [55.4, 48.6, 44.5, 41.0, 38.6],
    "hyp_upfront":   [60.2, 53.3, 48.0, 44.3, 41.5],
    "hyp_feedin":    [42.1, 36.9, 33.4, 30.8, 29.1],
    "hyp_feedin_eq": [60.2, 53.3, 48.0, 44.3, 41.5],
}
hh_support_total = {
    "exp_baseline":  228.2,
    "hyp_upfront":   247.3,
    "hyp_feedin":    172.3,
    "hyp_feedin_eq": 325.6,
}

sum_gov_mio = {
    "exp_baseline":  49739.46,
    "hyp_upfront":   59289.59,
    "hyp_feedin":    37250.15,
    "hyp_feedin_eq": 78045.07,
}
sum_hh_mio = {
    "exp_baseline":  35718.43,
    "hyp_upfront":   42415.25,
    "hyp_feedin":    26736.51,
    "hyp_feedin_eq": 42415.27,
}
sum_cap_gw = {
    "exp_baseline":  310.43,
    "hyp_upfront":   358.78,
    "hyp_feedin":    303.04,
    "hyp_feedin_eq": 358.78,
}

cap_new_total = {
    "exp_baseline":  310.43,
    "hyp_upfront":   358.78,
    "hyp_feedin":    303.04,
    "hyp_feedin_eq": 358.78,
}

scenarios_order = ["exp_baseline", "hyp_upfront", "hyp_feedin", "hyp_feedin_eq"]

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 8,
    "axes.titlesize": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8,
    "xtick.major.size": 3, "ytick.major.size": 3,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "hatch.linewidth": 0.45,
})

fig = plt.figure(figsize=(18, 9))
gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 0.50],
                      width_ratios=[1.0, 1.0, 1.0],
                      hspace=0.18, wspace=0.22,
                      left=0.05, right=0.99, top=0.94, bottom=0.05)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])
ax_tab = fig.add_subplot(gs[1, :])


def closed_box(ax):
    for side in ["top", "right", "bottom", "left"]:
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(0.8)
        ax.spines[side].set_color("black")


def stagger_labels(ax, ydata_per_scen, scens, ylim_range, fontsize=7,
                   fmt="{:.1f}"):
    dy_unit = ylim_range * 0.030
    for xi, year in enumerate(years):
        pairs = [(s, ydata_per_scen[s][xi]) for s in scens]
        pairs.sort(key=lambda p: p[1])
        n = len(pairs)
        for rank, (s, val) in enumerate(pairs):
            color = scenario_colors[s]
            if rank == 0:
                dy, va = -dy_unit * 1.7, "top"
            elif rank == n - 1:
                dy, va = +dy_unit * 1.7, "bottom"
            elif rank < n / 2:
                dy, va = -dy_unit * 0.7, "top"
            else:
                dy, va = +dy_unit * 0.7, "bottom"
            ax.text(year, val + dy, fmt.format(val),
                    ha="center", va=va, fontsize=fontsize,
                    fontweight="bold", color=color)


def draw_alternating_arrow(ax, x0, x1, y,
                           color1="#7e3f8f", color2="#a85410",
                           n_segments=34, linewidth=4.5,
                           head_len=0.08):
    direction = 1 if x1 >= x0 else -1
    x_line_end = x1 - direction * head_len
    xs = np.linspace(x0, x_line_end, n_segments + 1)

    for i in range(n_segments):
        ax.plot(
            [xs[i], xs[i + 1]],
            [y, y],
            color=color1 if i % 2 == 0 else color2,
            linewidth=linewidth,
            solid_capstyle="butt",
            clip_on=False,
            zorder=6
        )

    ax.annotate(
        "",
        xy=(x1, y),
        xytext=(x_line_end, y),
        arrowprops=dict(
            arrowstyle="->",
            color=color2,
            lw=linewidth,
            shrinkA=0,
            shrinkB=0,
            mutation_scale=14
        ),
        zorder=7
    )


YLIM = 130
YTICK = 20

for scen in scenarios_order:
    ax_a.plot(years, gov_support_yearly[scen],
              color=scenario_colors[scen], linewidth=2.0,
              marker="o", markersize=5, linestyle="-")

stagger_labels(ax_a, gov_support_yearly, scenarios_order,
               ylim_range=YLIM, fontsize=7, fmt="{:.1f}")

ax_a.set_xlabel("Year")
ax_a.set_ylabel("Public expenditure (bn €)")
ax_a.set_xticks(years)
ax_a.set_xlim(2028, 2052)
ax_a.set_ylim(0, YLIM)
ax_a.yaxis.set_major_locator(MultipleLocator(YTICK))
closed_box(ax_a)
ax_a.set_title("Government perspective (exponentially discounted)",
               fontsize=10, pad=8)
ax_a.text(-0.10, 1.04, "a", transform=ax_a.transAxes,
          fontsize=14, fontweight="bold", va="bottom", ha="left")

a_handles = [
    Line2D([0], [0], color=scenario_colors[s], linewidth=2.0,
           marker="o", markersize=4, linestyle="-",
           label=scenario_labels[s])
    for s in scenarios_order
]
ax_a.legend(handles=a_handles, loc="upper right",
            fontsize=7, frameon=False, handlelength=2.2, handletextpad=0.5)

for scen in scenarios_order:
    ax_b.plot(years, hh_support_yearly[scen],
              color=scenario_colors[scen], linewidth=1.6,
              marker="s", markersize=4, linestyle="--")

stagger_labels(ax_b, hh_support_yearly, scenarios_order,
               ylim_range=YLIM, fontsize=7, fmt="{:.1f}")

ax_b.set_xlabel("Year")
ax_b.set_ylabel("Perceived support value (bn €)")
ax_b.set_xticks(years)
ax_b.set_xlim(2028, 2052)
ax_b.set_ylim(0, YLIM)
ax_b.yaxis.set_major_locator(MultipleLocator(YTICK))
closed_box(ax_b)
ax_b.set_title("Household perspective (hyperbolically discounted)",
               fontsize=10, pad=8)
ax_b.text(-0.10, 1.04, "b", transform=ax_b.transAxes,
          fontsize=14, fontweight="bold", va="bottom", ha="left")

b_handles = [
    Line2D([0], [0], color=scenario_colors[s], linewidth=1.6,
           marker="s", markersize=4, linestyle="--",
           label=scenario_labels[s])
    for s in scenarios_order
]
ax_b.legend(handles=b_handles, loc="upper right",
            fontsize=7, frameon=False, handlelength=2.2, handletextpad=0.5)


def lighten_color(color, amount=0.70):
    rgb = np.array(mcolors.to_rgb(color))
    white = np.array([1.0, 1.0, 1.0])
    lightened_rgb = (1 - amount) * rgb + amount * white
    return mcolors.rgb2hex(tuple(lightened_rgb))


def add_manual_diagonal_hatch(ax, rect, spacing=8, slope_height=22,
                              color="#666666", linewidth=0.30):
    x0 = rect.get_x()
    x1 = x0 + rect.get_width()
    y0 = rect.get_y()
    y1 = y0 + rect.get_height()
    width = x1 - x0
    y_start = y0 - slope_height

    while y_start < y1:
        xa, ya = x0, y_start
        xb, yb = x1, y_start + slope_height

        if ya < y0:
            frac = (y0 - ya) / (yb - ya)
            xa = x0 + frac * width
            ya = y0

        if yb > y1:
            frac = (y1 - ya) / (yb - ya)
            xb = xa + frac * (x1 - xa)
            yb = y1

        if xa < xb and y0 <= ya <= y1 and y0 <= yb <= y1:
            ax.plot(
                [xa, xb],
                [ya, yb],
                color=color,
                linewidth=linewidth,
                solid_capstyle="butt",
                zorder=rect.get_zorder() + 0.2,
                clip_on=True
            )

        y_start += spacing


gov_eur_per_kw = {s: sum_gov_mio[s] / sum_cap_gw[s] for s in scenarios_order}
hh_eur_per_kw  = {s: sum_hh_mio[s]  / sum_cap_gw[s] for s in scenarios_order}

n_scen = len(scenarios_order)
bar_w = 0.36
x_pos = np.arange(n_scen)

gov_vals = [gov_eur_per_kw[s] for s in scenarios_order]
hh_vals  = [hh_eur_per_kw[s]  for s in scenarios_order]

for i, s in enumerate(scenarios_order):
    x = x_pos[i] - bar_w / 2

    ax_c.bar(
        x,
        gov_vals[i],
        width=bar_w,
        color=scenario_colors[s],
        edgecolor="black",
        linewidth=0.7,
        zorder=2
    )

    ax_c.text(
        x,
        gov_vals[i] + 4,
        f"{gov_vals[i]:.2f}",
        ha="center",
        va="bottom",
        fontsize=7.5,
        fontweight="bold",
        color=scenario_colors[s],
        zorder=4
    )


for i, s in enumerate(scenarios_order):
    x = x_pos[i] + bar_w / 2

    light = lighten_color(scenario_colors[s], amount=0.68)
    hatch_col = lighten_color(scenario_colors[s], amount=0.25)

    bars = ax_c.bar(
        x,
        hh_vals[i],
        width=bar_w,
        color=light,
        edgecolor="black",
        linewidth=0.6,
        zorder=2
    )

    rect = bars.patches[0]

    add_manual_diagonal_hatch(
        ax_c,
        rect,
        spacing=10,
        slope_height=24,
        color=hatch_col,
        linewidth=0.24
    )

    ax_c.text(
        x,
        hh_vals[i] + 4,
        f"{hh_vals[i]:.2f}",
        ha="center",
        va="bottom",
        fontsize=7.5,
        fontweight="bold",
        color=scenario_colors[s],
        zorder=4
    )

ax_c.set_xticks(x_pos)
ax_c.set_xticklabels([scenario_short[s] for s in scenarios_order],
                     fontsize=8)

ax_c.set_ylabel("Support expenditure (€/kW added)")
ax_c.set_ylim(0, max(gov_vals) * 1.35)
ax_c.yaxis.set_major_locator(MultipleLocator(50))
closed_box(ax_c)
ax_c.set_title("Cost intensity of additional residential (rooftop) PV expansion",
               fontsize=10, pad=8)
ax_c.text(-0.10, 1.04, "c", transform=ax_c.transAxes,
          fontsize=14, fontweight="bold", va="bottom", ha="left")

i_up = scenarios_order.index("hyp_upfront")
i_eq = scenarios_order.index("hyp_feedin_eq")

y_up_val = gov_eur_per_kw["hyp_upfront"]
y_eq_val = gov_eur_per_kw["hyp_feedin_eq"]
prem_eur = y_eq_val - y_up_val
prem_pct = prem_eur / y_up_val * 100

arrow_y = y_eq_val + 18
x_up_bar = x_pos[i_up] - bar_w / 2
x_eq_bar = x_pos[i_eq] - bar_w / 2

draw_alternating_arrow(
    ax_c,
    x_up_bar,
    x_eq_bar,
    arrow_y,
    color1=scenario_colors["hyp_upfront"],
    color2=scenario_colors["hyp_feedin_eq"],
    n_segments=34,
    linewidth=4.5
)

mid_x = (x_up_bar + x_eq_bar) / 2

ax_c.text(
    mid_x, arrow_y + 5,
    f"+{prem_eur:.2f} €/kW (+{prem_pct:.1f}%)\nfor equivalent PV expansion",
    ha="center", va="bottom",
    fontsize=9,
)


class HandlerManualHatch(HandlerBase):
    def __init__(
        self,
        facecolor: str = "lightgrey",
        edgecolor: str = "black",
        border_lw: float = 0.8,
        spacing: float = 4.0,
        hatch_color: str = "#666666",
        hatch_lw: float = 0.45,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.border_lw = border_lw
        self.spacing = spacing
        self.hatch_color = hatch_color
        self.hatch_lw = hatch_lw

    def create_artists(
        self,
        legend: Any,
        orig_handle: Artist,
        xdescent: float,
        ydescent: float,
        width: float,
        height: float,
        fontsize: float,
        trans: Any,
    ) -> list[Artist]:

        rect = mpatches.Rectangle(
            (xdescent, ydescent),
            width,
            height,
            facecolor=self.facecolor,
            edgecolor=self.edgecolor,
            linewidth=self.border_lw,
            transform=trans,
        )

        artists: list[Artist] = [rect]

        x0 = xdescent
        x1 = xdescent + width
        y0 = ydescent
        y1 = ydescent + height
        diag_height = height * 1.4

        y_start = y0 - diag_height

        while y_start < y1:
            xa, ya = x0, y_start
            xb, yb = x1, y_start + diag_height

            if ya < y0:
                frac = (y0 - ya) / (yb - ya)
                xa = x0 + frac * width
                ya = y0

            if yb > y1:
                frac = (y1 - ya) / (yb - ya)
                xb = xa + frac * (x1 - xa)
                yb = y1

            if xa < xb and y0 <= ya <= y1 and y0 <= yb <= y1:
                line = Line2D(
                    [xa, xb],
                    [ya, yb],
                    color=self.hatch_color,
                    linewidth=self.hatch_lw,
                    solid_capstyle="butt",
                    transform=trans,
                )
                artists.append(line)

            y_start += self.spacing

        return artists


gov_handle = mpatches.Patch(
    facecolor="grey",
    edgecolor="black",
    linewidth=0.8,
    label="Government (expended)"
)

hh_handle = mpatches.Patch(
    facecolor="lightgrey",
    edgecolor="black",
    linewidth=0.8,
    label="Households (perceived)"
)

ax_c.legend(
    handles=[gov_handle, hh_handle],
    loc="upper left",
    fontsize=7.5,
    frameon=False,
    handler_map={
        hh_handle: HandlerManualHatch(
            facecolor="lightgrey",
            edgecolor="black",
            border_lw=0.8,
            spacing=4.0,
            hatch_color="#666666",
            hatch_lw=0.45,
        )
    }
)


ax_tab.axis("off")

g_exp = gov_support_total["exp_baseline"]
g_hyp_up = gov_support_total["hyp_upfront"]
g_hyp_fi = gov_support_total["hyp_feedin"]
g_hyp_eq = gov_support_total["hyp_feedin_eq"]

cap_exp = cap_new_total["exp_baseline"]
cap_hyp_up = cap_new_total["hyp_upfront"]
cap_hyp_fi = cap_new_total["hyp_feedin"]
cap_hyp_eq = cap_new_total["hyp_feedin_eq"]


def fmt_diff_bn(value, reference):
    if abs(value) < 1e-9:
        return "(-)"
    pct = value / reference * 100
    return f"{value:+.1f} bn € ({pct:+.1f}%)"


def fmt_diff_gw(value):
    if abs(value) < 0.05:
        return "(-)"
    return f"{value:+.1f} GW"


rows_data = [
    {
        "label1": "Exponential\n(neglect of present bias)",
        "label2": "exponential",
        "upfront": f"{g_exp:.1f} bn €\n{cap_exp:.1f} GW",
        "fit":     f"{g_exp:.1f} bn €\n{cap_exp:.1f} GW",
        "diff":    f"{fmt_diff_bn(0.0, g_exp)}\n{fmt_diff_gw(0.0)}",
    },
    {
        "label1": "Exponential\n(neglect of present bias)",
        "label2": "hyperbolic",
        "upfront": f"{g_hyp_up:.1f} bn €\n{cap_hyp_up:.1f} GW",
        "fit":     f"{g_hyp_fi:.1f} bn €\n{cap_hyp_fi:.1f} GW",
        "diff":    f"{fmt_diff_bn(g_hyp_fi - g_hyp_up, g_hyp_up)}\n"
                   f"{fmt_diff_gw(cap_hyp_fi - cap_hyp_up)}",
    },
    {
        "label1": "Hyperbolic\n(anticipation of present bias)",
        "label2": "hyperbolic",
        "upfront": f"{g_hyp_up:.1f} bn €\n{cap_hyp_up:.1f} GW",
        "fit":     f"{g_hyp_eq:.1f} bn €\n{cap_hyp_eq:.1f} GW",
        "diff":    f"{fmt_diff_bn(g_hyp_eq - g_hyp_up, g_hyp_up)}\n"
                   f"{fmt_diff_gw(cap_hyp_eq - cap_hyp_up)}",
    },
]

table_x0 = 0.10
table_x1 = 0.90
table_w = table_x1 - table_x0

rel_col_widths = [0.23, 0.13, 0.18, 0.18, 0.28]
col_widths = [w * table_w for w in rel_col_widths]

col_x = [table_x0]
for w in col_widths[:-1]:
    col_x.append(col_x[-1] + w)

table_top_y = 0.98
header_h = 0.13
data_h = 0.20

y_separators = [
    table_top_y,
    table_top_y - header_h,
    table_top_y - 2 * header_h,
    table_top_y - 2 * header_h - data_h,
    table_top_y - 2 * header_h - 2 * data_h,
    table_top_y - 2 * header_h - 3 * data_h,
]

x_left = table_x0 + 0.04
x_right = table_x1 - 0.04
for i, y in enumerate(y_separators):
    lw = 1.5 if i in (0, 2, 5) else 0.7
    ax_tab.plot([x_left, x_right], [y, y],
                color="black", linewidth=lw,
                transform=ax_tab.transAxes, clip_on=False)

disc_left = col_x[0]
disc_right = col_x[1] + col_widths[1]
supp_left = col_x[2]
supp_right = col_x[4] + col_widths[4]

ax_tab.text((disc_left + disc_right) / 2 + 0.02,
            table_top_y - header_h / 2,
            "Discounting scenario",
            ha="center", va="center",
            fontsize=10, fontweight="bold",
            transform=ax_tab.transAxes)

ax_tab.text((supp_left + supp_right) / 2 - 0.04,
            table_top_y - header_h / 2,
            "Support mechanism outcome",
            ha="center", va="center",
            fontsize=10, fontweight="bold",
            transform=ax_tab.transAxes)

sub_y = table_top_y - 1.5 * header_h

ax_tab.text(col_x[0] + col_widths[0] / 2, sub_y,
            "Government", ha="center", va="center",
            fontsize=9, transform=ax_tab.transAxes)

ax_tab.text(col_x[1] + col_widths[1] / 2, sub_y,
            "Households", ha="center", va="center",
            fontsize=9, transform=ax_tab.transAxes)

ax_tab.text(col_x[2] + col_widths[2] / 2, sub_y,
            "Upfront payment", ha="center", va="center",
            fontsize=9, transform=ax_tab.transAxes)

ax_tab.text(col_x[3] + col_widths[3] / 2, sub_y,
            "Feed-in tariff", ha="center", va="center",
            fontsize=9, transform=ax_tab.transAxes)

ax_tab.text(col_x[4] + col_widths[4] / 2, sub_y,
            r"$\Delta$ Feed-in tariff $-$ upfront payment",
            ha="center", va="center",
            fontsize=9, transform=ax_tab.transAxes)

keys = ["label1", "label2", "upfront", "fit", "diff"]

for ri, row in enumerate(rows_data):
    y_top = y_separators[2 + ri]
    y_bot = y_separators[3 + ri]
    y_center = (y_top + y_bot) / 2

    is_highlight_row = (ri == 2)

    for ci, key in enumerate(keys):
        x = col_x[ci]
        w = col_widths[ci]
        text = row[key]

        weight = "normal"
        color = "black"
        fontsize = 9

        if is_highlight_row and ci in (4,):
            weight = "bold"
            color = "black"
            fontsize = 9.5

        ax_tab.text(x + w / 2, y_center, text,
                    ha="center", va="center",
                    fontsize=fontsize, fontweight=weight,
                    color=color, transform=ax_tab.transAxes)

ax_tab.text(table_x0 + 0.005, table_top_y + 0.005, "d",
            transform=ax_tab.transAxes,
            fontsize=14, fontweight="bold",
            va="bottom", ha="left")


def yfmt_no_zero(x, _pos):
    if abs(x) < 1e-9:
        return ""
    return f"{x:,.0f}"


for ax in [ax_a, ax_b]:
    ax.yaxis.set_major_formatter(FuncFormatter(yfmt_no_zero))

ax_c.yaxis.set_major_formatter(FuncFormatter(yfmt_no_zero))

plt.show()