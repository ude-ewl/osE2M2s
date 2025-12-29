from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

DATA = [
    # Marginal solar rebound
    {"Type": "Marginal", "Reference": "Aydın et al., 2023",        "End": 2014, "SRE": "7.7%"},
    {"Type": "Marginal", "Reference": "Havas et al., 2015",        "End": 2013, "SRE": "15"},
    {"Type": "Marginal", "Reference": "Qiu et al., 2019",          "End": 2017, "SRE": "18%"},
    {"Type": "Marginal", "Reference": "Deng & Newton, 2017",       "End": 2014, "SRE": "16.7%"},
    {"Type": "Marginal", "Reference": "Deng & Newton, 2017",       "End": 2014, "SRE": "20.9%"},
    {"Type": "Marginal", "Reference": "Spiller et al., 2017",      "End": 2015, "SRE": "8.5%"},
    {"Type": "Marginal", "Reference": "Spiller et al., 2017",      "End": 2015, "SRE": "10.%"},
    {"Type": "Marginal", "Reference": "Beppler et al., 2021",      "End": 2018, "SRE": "28.5%"},
    {"Type": "Marginal", "Reference": "Galvin et al., 2022 I",     "End": 2020, "SRE": "14%"},
    {"Type": "Marginal", "Reference": "Galvin et al., 2022 II",    "End": 2018, "SRE": "33%"},
    {"Type": "Marginal", "Reference": "Frondel et al., 2020 I",    "End": 2015, "SRE": "23%"},
    {"Type": "Marginal", "Reference": "Bigler, 2025 I",            "End": 2019, "SRE": "11.1%"},

    # Discrete solar rebound
    {"Type": "Discrete", "Reference": "Toroghi & Oliver, 2019",    "End": 2014, "SRE": "5.8%"},
    {"Type": "Discrete", "Reference": "Toroghi & Oliver, 2019",    "End": 2014, "SRE": "2.9%"},
    {"Type": "Discrete", "Reference": "Boccard & Gautier, 2021",   "End": 2017, "SRE": "35%"},
    {"Type": "Discrete", "Reference": "Nguyen et al., 2024 I",     "End": 2021, "SRE": "16%"},
    {"Type": "Discrete", "Reference": "Nguyen et al., 2024 II",    "End": 2021, "SRE": "3.5%"},
    {"Type": "Discrete", "Reference": "Frondel et al., 2020 II",   "End": 2015, "SRE": "35%"},
    {"Type": "Discrete", "Reference": "Bigler, 2025 II",           "End": 2019, "SRE": "7.96%"},
    {"Type": "Discrete", "Reference": "Kim & Trevena, 2021",       "End": 2018, "SRE": "6.6%"},
]

def main() -> None:
    df = pd.DataFrame(DATA)
    df["SRE_pct"] = df["SRE"].str.rstrip("%").astype(float)

    scale = 1.25

    plt.style.use("default")
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.labelsize": 14 * scale,
        "axes.labelweight": "bold",
        "axes.titlesize": 14 * scale,
        "axes.titleweight": "bold",
        "xtick.labelsize": 10 * scale,
        "ytick.labelsize": 10 * scale,
        "legend.fontsize": 10 * scale,
    })

    placements = {
        ("Frondel et al., 2020 II", 2015, 35.00): dict(dx=-8, dy=0,  ha="right", va="center"),
        ("Boccard & Gautier, 2021", 2017, 35.00): dict(dx=8,  dy=0,  ha="left",  va="center"),
        ("Galvin et al., 2022 II",  2018, 33.00): dict(dx=8,  dy=0,  ha="left",  va="center"),
        ("Beppler et al., 2021",    2018, 28.50): dict(dx=-8, dy=0,  ha="right", va="center"),
        ("Frondel et al., 2020 I",  2015, 23.00): dict(dx=8,  dy=0,  ha="left",  va="center"),
        ("Deng & Newton, 2017",     2014, 20.90): dict(dx=8,  dy=0,  ha="left",  va="center"),
        ("Deng & Newton, 2017",     2014, 16.70): dict(dx=8,  dy=0,  ha="left",  va="center"),
        ("Qiu et al., 2019",        2017, 18.00): dict(dx=8,  dy=0,  ha="left",  va="center"),
        ("Havas et al., 2015",      2013, 15.00): dict(dx=8,  dy=0,  ha="left",  va="center"),
        ("Galvin et al., 2022 I",   2020, 14.00): dict(dx=-8, dy=-2, ha="right", va="center"),
        ("Bigler, 2025 I",          2019, 11.10): dict(dx=8,  dy=-1, ha="left",  va="center"),
        ("Bigler, 2025 II",         2019, 7.96):  dict(dx=8,  dy=0,  ha="left",  va="center"),
        ("Kim & Trevena, 2021",     2018, 6.60):  dict(dx=8,  dy=0,  ha="left",  va="center"),
        ("Spiller et al., 2017",    2015, 10.00): dict(dx=8,  dy=0,  ha="left",  va="center"),
        ("Spiller et al., 2017",    2015, 8.50):  dict(dx=8,  dy=0,  ha="left",  va="center"),
        ("Aydın et al., 2023",      2014, 7.70):  dict(dx=-8, dy=-2, ha="right", va="center"),
        ("Toroghi & Oliver, 2019",  2014, 5.80):  dict(dx=8,  dy=-1, ha="left",  va="center"),
        ("Toroghi & Oliver, 2019",  2014, 2.90):  dict(dx=8,  dy=-1, ha="left",  va="center"),
        ("Nguyen et al., 2024 I",   2021, 16.00): dict(dx=-8, dy=0,  ha="right", va="center"),
        ("Nguyen et al., 2024 II",  2021, 3.50):  dict(dx=8,  dy=-1, ha="left",  va="center"),
    }

    colors = {"Marginal": "black", "Discrete": "0.5"}
    markers = {"Marginal": "o", "Discrete": "s"}

    means = df.groupby("Type")["SRE_pct"].mean()

    base_w, base_h = 10, 5.6
    fig, ax = plt.subplots(figsize=(base_w * scale, base_h * scale))

    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.5)
    ax.grid(False, axis="x")

    for s in ax.spines.values():
        s.set_visible(True)

    marker_size = 42 * (scale ** 2)
    for typ in ["Discrete", "Marginal"]:
        sub = df[df["Type"] == typ]
        ax.scatter(
            sub["End"], sub["SRE_pct"],
            s=marker_size,
            marker=markers[typ],
            color=colors[typ],
            edgecolor="none",
            zorder=3,
            label=("Discrete solar rebound" if typ == "Discrete" else "Marginal solar rebound"),
        )

    ax.axhline(means["Marginal"], color=colors["Marginal"], linestyle="--", linewidth=1.5, zorder=2)
    ax.axhline(means["Discrete"], color=colors["Discrete"], linestyle="--", linewidth=1.5, zorder=2)

    ax.text(
        2021.7, means["Marginal"] + 0.6,
        f"Average marginal SRE (≈ {means['Marginal']:.1f}%)",
        color=colors["Marginal"], fontsize=10 * scale, fontweight="bold",
        ha="left", va="bottom"
    )
    ax.text(
        2021.7, means["Discrete"] + 0.6,
        f"Average discrete SRE (≈ {means['Discrete']:.1f}%)",
        color=colors["Discrete"], fontsize=10 * scale, fontweight="bold",
        ha="left", va="bottom"
    )

    for _, r in df.iterrows():
        ref = r["Reference"]
        end = int(r["End"])
        sre = float(r["SRE_pct"])
        key = (ref, end, round(sre, 2))
        p = placements.get(key, dict(dx=6, dy=0, ha="left", va="center"))

        ax.annotate(
            ref, (end, sre),
            textcoords="offset points", xytext=(float(p["dx"]), float(p["dy"])),
            ha=p["ha"], va=p["va"],
            fontsize=10 * scale,
            color=colors[r["Type"]],
            zorder=4
        )

    ax.set_xlim(2012, 2025)
    ax.set_xticks(range(2012, 2026))
    ax.set_ylim(0, 42)
    ax.set_yticks([0, 10, 20, 30, 40])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{int(y)}"))
    ax.set_ylabel("Effect strength [%]")

    leg = ax.legend(loc="upper right", frameon=False)
    handles = getattr(leg, "legend_handles", None) or getattr(leg, "legendHandles", [])
    texts   = leg.get_texts()

    for h, t in zip(handles, texts):
        label = t.get_text()
        if "Discrete" in label:
            try:
                h.set_facecolor(colors["Discrete"])
                h.set_edgecolor("none")
            except Exception:
                h.set_color(colors["Discrete"])
            t.set_color(colors["Discrete"])

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()