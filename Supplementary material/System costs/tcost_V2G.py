import numpy as np
import matplotlib.pyplot as plt

years = np.array([2030, 2035, 2040, 2045, 2050])

full_abs = np.array([403.5, 457.9, 484.9, 518.7, 550.8])
avg_abs = np.array([404.8, 458.4, 485.1, 518.9, 551.0])
low_abs = np.array([409.3, 461.3, 486.6, 520.8, 553.0])

sys_25_100 = np.array([5.7, 3.4, 1.8, 2.0, 2.3])
sys_25_61 = np.array([4.4, 2.9, 1.5, 1.8, 2.1])
av_25_100 = np.array([116.1, 33.9, 11.8, 11.2, 12.0])
av_25_61 = np.array([89.1, 29.0, 9.9, 10.1, 11.0])

ev_number_mio = np.array([49, 101, 150, 182, 188])

c_ref  = "#37607e"
c_avg = "#e98935"
c_low  = "#78B43D"
ms = 5
lw = 2.0

color_full = "#37607e"
color_avg = "#e98935"
bar_color  = "0.85"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.6, 4.9), sharex=True)

l_full, = axL.plot(years, full_abs, "-o", color=c_ref,  linewidth=lw, markersize=ms,
                   label="Full availability (100%, reference)")
l_avg, = axL.plot(years, avg_abs, "-o", color=c_avg, linewidth=lw, markersize=ms,
                   label="Average availability (61%)")
l_low_, = axL.plot(years, low_abs,  "-o", color=c_low,  linewidth=lw, markersize=ms,
                   label="Low availability (25%)")

axL.set_ylabel("Total system costs [bn€/yr]", fontweight='bold', fontsize=14, labelpad=-0.25)

for x, y in zip(years, full_abs):
    y_avg = avg_abs[np.where(years == x)[0][0]]
    axL.text(x, y_avg - 6.0, f"{y:.1f}".rstrip('0').rstrip('.'), color=c_ref, fontsize=11, fontweight='bold',
             ha='center', va='top')
for x, y in zip(years, avg_abs):
    axL.text(x, y - 1.5, f"{y:.1f}".rstrip('0').rstrip('.'), color=c_avg, fontsize=11, fontweight='bold',
             ha='center', va='top')
for x, y in zip(years, low_abs):
    axL.text(x, y + 1.5, f"{y:.1f}".rstrip('0').rstrip('.'), color=c_low, fontsize=11, fontweight='bold',
             ha='center', va='bottom')

bars = axR.bar(years, ev_number_mio, width=1.75, color=bar_color, alpha=1.0, edgecolor="none", label="EV stock")

for bar in bars:
    height = bar.get_height()
    axR.text(
        bar.get_x() + bar.get_width() / 2, height - 5, f"{height:.0f}", ha="center", va="top", fontsize=10, color="black", fontweight="bold")

lav1, = axR.plot(years, av_25_100, "--o", color=color_full, lw=1.8, ms=5,
                 label=r'Change in per-vehicle added value – $\mathit{low}$ compared with $\mathit{full}$')
lav2, = axR.plot(years, av_25_61,  "--o", color=color_avg, lw=1.8, ms=5,
                 label=r'Change in per-vehicle added value – $\mathit{low}$ compared with $\mathit{average}$')
axR.set_ylabel("EV stock [m] & value added [€/yr]", fontweight='bold', fontsize=14, labelpad=-0.25)

axR2 = axR.twinx()
lsys1, = axR2.plot(years, sys_25_100, "-s", color=color_full, lw=1.8, ms=5,
                   label=r'system cost – $\mathit{low}$ compared with $\mathit{full}$')
lsys2, = axR2.plot(years, sys_25_61,  "-s", color=color_avg, lw=1.8, ms=5,
                   label=r'system cost – $\mathit{low}$ compared with $\mathit{average}$')
axR2.set_ylabel("Additional system costs [bn€/yr]", fontsize=14, fontweight="bold", rotation=-90, labelpad=15)

for ax in (axL, axR):
    ax.set_xticks(years)
    ax.set_xlim(years.min()-2, years.max()+2)

axR.set_ylim(0, 190)
axR.set_yticks(np.arange(0, 190, 20))
axR2.set_ylim(0, 6.5)
axR2.set_yticks(np.arange(0, 6.1, 1))

for x, y in zip(years, av_25_100):
    axR.text(x, y+3, f"{y:.1f}".rstrip('0').rstrip('.'), color=color_full, ha="center", va="bottom", fontsize=11)
for x, y in zip(years, av_25_61):
    axR.text(x, y-3, f"{y:.1f}".rstrip('0').rstrip('.'), color=color_avg, ha="center", va="top", fontsize=11)
for x, y in zip(years, sys_25_100):
    axR2.text(x, y+0.12, f"{y:.1f}".rstrip('0').rstrip('.'), color=color_full, ha="center", va="bottom", fontsize=11)
for x, y in zip(years, sys_25_61):
    axR2.text(x, y+0.12, f"{y:.1f}".rstrip('0').rstrip('.'), color=color_avg, ha="center", va="bottom", fontsize=11)

plt.tight_layout()

posL = axL.get_position()
posR = axR.get_position()
legend_y = min(posL.y0, posR.y0) - 0.002

fig.legend(handles=[l_full, l_avg, l_low_],
           labels=["Full availability (100%)", "Average availability (61%)", "Low availability (25%)"],
           loc="upper left",
           bbox_to_anchor=(posL.x0, legend_y + 0.002),
           bbox_transform=fig.transFigure,
           frameon=False, fontsize=10,
           borderaxespad=0, handletextpad=0.6,
           handlelength=2.0, labelspacing=0.40, borderpad=0.0)

fig.legend(handles=[lav1, lav2, lsys1, lsys2, bars],
           labels=[r'Per-vehicle added value: $\mathit{low}$ relative to $\mathit{full}$',
                   r'Per-vehicle added value: $\mathit{low}$ relative to $\mathit{average}$',
                   r'Additional system costs: $\mathit{low}$ relative to $\mathit{full}$',
                   r'Additional system costs: $\mathit{low}$ relative to $\mathit{average}$',
                   "EV stock"],
           loc="upper left",
           bbox_to_anchor=(posR.x0, legend_y + 0.002),
           bbox_transform=fig.transFigure,
           frameon=False, fontsize=10,
           borderaxespad=0, handletextpad=0.6,
           handlelength=2.0, labelspacing=0.40, borderpad=0.0)

plt.tight_layout()
plt.subplots_adjust(bottom=0.16)
plt.show()