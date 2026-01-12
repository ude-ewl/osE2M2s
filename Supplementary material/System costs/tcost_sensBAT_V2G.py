import numpy as np
import matplotlib.pyplot as plt

years = np.array([2030, 2035, 2040, 2045, 2050])
ev_number_mio = np.array([49, 101, 150, 182, 188])

color_full = "#37607e"
color_avg  = "#e98935"
bar_color  = "0.8"

sys_25_100_50 = np.array([5.1, 4.3, 1.7, 2.2, 2.4])
sys_25_61_50  = np.array([3.9, 3.8, 1.8, 2.3, 2.4])

av_25_100_50  = np.array([103.1, 42.0, 11.5, 12.2, 12.5])
av_25_61_50   = np.array([78.7, 37.9, 11.8, 12.5, 13.0])

sys_25_100_100 = np.array([4.5, 4.5, 2.1, 2.1, 2.4])
sys_25_61_100  = np.array([3.5, 4.0, 1.9, 2.0, 2.0])

av_25_100_100  = np.array([91.3, 44.2, 13.8, 11.5, 12.8])
av_25_61_100   = np.array([71.7, 39.9, 12.8, 10.7, 10.8])

def draw_panel(axL, years, ev_mio, sys_25_100, sys_25_61, av_25_100, av_25_61,
               title, color_full="#37607e", color_avg="#e98935", bar_color="0.8"):
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
            x, y + 3,
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
            x, y + 0.12,
            f"{y:.1f}".rstrip('0').rstrip('.'),
            ha="center", va="bottom",
            fontsize=11, color=color_full
        )
    for x, y in zip(years, sys_25_61):
        axR.text(
            x, y + 0.12,
            f"{y:.1f}".rstrip('0').rstrip('.'),
            ha="center", va="bottom",
            fontsize=11, color=color_avg
        )

    axL.set_title(title, fontsize=11, pad=8)

    handles = [l1, l2, l3, l4, bars]
    return handles, axR

fig, (axL1, axL2) = plt.subplots(1, 2, figsize=(14, 5.4), sharey=False)

handles_50, axR1 = draw_panel(
    axL1, years, ev_number_mio,
    sys_25_100_50, sys_25_61_50,
    av_25_100_50, av_25_61_50,
    title="Battery storage capacity in 2030:+50 GW",
    color_full=color_full, color_avg=color_avg, bar_color=bar_color
)

handles_100, axR2 = draw_panel(
    axL2, years, ev_number_mio,
    sys_25_100_100, sys_25_61_100,
    av_25_100_100, av_25_61_100,
    title="Battery storage capacity in 2030:+100 GW",
    color_full=color_full, color_avg=color_avg, bar_color=bar_color
)

axR2.set_ylim(0, 5.5)
axR2.set_yticks([0, 1, 2, 3, 4, 5])
axR1.set_ylim(axR2.get_ylim())
axR1.set_yticks(axR2.get_yticks())
axR1.set_ylabel('')
axR1.tick_params(right=True, labelright=False)
axR1.spines['right'].set_visible(True)

ymin, ymax = 0, 210
ticks_25 = np.arange(ymin, ymax + 1, 25)

axL1.set_ylim(ymin, ymax)
axL1.set_yticks(ticks_25)

axL2.set_ylim(ymin, ymax)
axL2.set_yticks(ticks_25)
axL2.set_ylabel('')
axL2.tick_params(left=True, labelleft=False)
axL2.spines['left'].set_visible(True)

h_l1, h_l2, h_l3, h_l4, h_bars = handles_50

left_handles = [h_l1, h_l2, h_bars]
left_labels = [h.get_label() for h in left_handles]
fig.legend(
    left_handles, left_labels,
    loc='upper left', bbox_to_anchor=(0.10, 0.08),
    frameon=False
)

right_handles = [h_l3, h_l4]
right_labels = [h.get_label() for h in right_handles]
fig.legend(
    right_handles, right_labels,
    loc='upper right', bbox_to_anchor=(0.90, 0.08),
    frameon=False
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.16)
plt.show()