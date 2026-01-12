import numpy as np
import matplotlib.pyplot as plt

years = np.array([2030, 2035, 2040, 2045, 2050])
ev_number_mio = np.array([49, 101, 150, 182, 188])

color_full = "#37607e"
color_avg  = "#e98935"
bar_color  = "0.8"

sys_25_100_gas = np.array([9.4, 6.8, 4.8, 4.4, 4.6])
sys_25_61_gas  = np.array([7.4, 6.1, 4.5, 4.2, 4.3])

av_25_100_gas  = np.array([190.8, 67.1, 32.1, 24.3, 24.5])
av_25_61_gas   = np.array([150.5, 60.6, 29.8, 23.2, 23.1])

def draw_panel(axL, years, ev_mio, sys_25_100, sys_25_61,
               av_25_100, av_25_61,
               color_full="#37607e", color_avg="#e98935", bar_color="0.8"):

    bars = axL.bar(
        years, ev_mio, width=1.75, color=bar_color, alpha=0.7,
        edgecolor="none", label="EV stock"
    )

    l1, = axL.plot(
        years, av_25_100, "--", color=color_full, marker="o",
        markersize=5, linewidth=1.5,
        label=r'Change in per-vehicle added value – $\mathit{low}$ (25%) compared with $\mathit{full}$ (100%)'
    )
    l2, = axL.plot(
        years, av_25_61, "--", color=color_avg, marker="o",
        markersize=5, linewidth=1.5,
        label=r'Change in per-vehicle added value – $\mathit{low}$ (25%) compared with $\mathit{average}$ (61%)'
    )
    axL.set_ylabel("EV stock [m] & value added [€/yr]",
                   fontsize=14, fontweight="bold")

    axR = axL.twinx()
    l3, = axR.plot(
        years, sys_25_100, "-", color=color_full, marker="s",
        markersize=5, linewidth=1.5,
        label=r'Change in system costs – $\mathit{low}$ (25%) compared with $\mathit{full}$ (100%)'
    )
    l4, = axR.plot(
        years, sys_25_61, "-", color=color_avg, marker="s",
        markersize=5, linewidth=1.5,
        label=r'Change in system costs – $\mathit{low}$ (25%) compared with $\mathit{average}$ (61%)'
    )
    axR.set_ylabel("Additional system costs [bn€/yr]",
                   fontsize=14, fontweight="bold",
                   rotation=-90, labelpad=17)

    axL.set_xticks(years)
    axL.set_xlim(years.min() - 0.6, years.max() + 0.6)

    axR.set_xticks(years)
    axR.set_xlim(years.min() - 1.6, years.max() + 1.6)

    for rect, val in zip(bars, ev_number_mio):
        axL.text(
            rect.get_x() + rect.get_width() / 2,
            rect.get_height() - 5,
            f"{val:.0f}",
            ha="center",
            va="top",
            fontsize=10,
            color="black",
            fontweight="bold"
        )

    for x, y in zip(years, av_25_100):
        axL.text(
            x, y + 5,
            f"{y:.1f}".rstrip('0').rstrip('.'),
            ha="center", va="bottom",
            fontsize=11, color=color_full
        )
    for x, y in zip(years, av_25_61):
        axL.text(
            x, y - 5,
            f"{y:.1f}".rstrip('0').rstrip('.'),
            ha="center", va="top",
            fontsize=11, color=color_avg
        )
    for x, y in zip(years, sys_25_100):
        axR.text(
            x, y + 0.3,
            f"{y:.1f}".rstrip('0').rstrip('.'),
            ha="center", va="bottom",
            fontsize=11, color=color_full
        )
    for x, y in zip(years, sys_25_61):
        axR.text(
            x, y + 0.3,
            f"{y:.1f}".rstrip('0').rstrip('.'),
            ha="center", va="bottom",
            fontsize=11, color=color_avg
        )

    handles = [l1, l2, l3, l4, bars]
    return handles, axR

fig, axL = plt.subplots(figsize=(7.5, 5.4))

fig.subplots_adjust(left=0.125, right=0.9, bottom=0.18, top=0.95)

handles_gas, axR = draw_panel(
    axL, years, ev_number_mio,
    sys_25_100_gas, sys_25_61_gas,
    av_25_100_gas, av_25_61_gas,
    color_full=color_full, color_avg=color_avg, bar_color=bar_color
)

axR.set_ylim(0, 10)
axR.set_yticks([0, 2, 4, 6, 8, 10])

ymin, ymax = 0, 210
ticks_25 = np.arange(ymin, ymax + 1, 25)
axL.set_ylim(ymin, ymax)
axL.set_yticks(ticks_25)

h_l1, h_l2, h_l3, h_l4, h_bars = handles_gas
all_handles = [h_l1, h_l2, h_l3, h_l4, h_bars]
all_labels  = [h.get_label() for h in all_handles]

leg_ax = fig.add_axes((0.0, 0.0, 1.0, 0.075))
leg_ax.set_facecolor("white")
leg_ax.axis("off")

leg_ax.legend(
    all_handles, all_labels,
    loc="center",
    ncol=1,
    frameon=False,
    fontsize=9,
    handlelength=2.5
)

plt.tight_layout()
plt.show()