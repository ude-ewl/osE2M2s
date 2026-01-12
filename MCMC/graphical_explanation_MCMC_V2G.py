import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow, FancyArrowPatch


def cm_to_in(cm: float) -> float:
    return cm / 2.54


def show_markov_mcmc_figure():
    """
    Paper-aligned schematic (Markov chain + MCMC scaling to E2M2s input).
    Show-only version: no saving, just plt.show().

    Tuning:
      - SCALE: global scaling for fonts/line widths/arrow heads
      - GAP_* / heights: spacing and vertical balance
    """

    SCALE = 1.15

    blue = "#0B4F8A"
    border = blue
    grey = "#7A7A7A"
    light_grey = "#8E8E8E"

    FS_BASE = 10.0 * SCALE
    FS_TITLE = 11.5 * SCALE
    FS_TIME = 12.0 * SCALE
    FS_DOTS = 18.0 * SCALE
    FS_BOX_TITLE = 10.5 * SCALE
    FS_STATE = 10.5 * SCALE
    FS_MATH = 10.5 * SCALE
    FS_MCMC_HDR = 10.8 * SCALE
    FS_MCMC_LINE = 9.6 * SCALE
    FS_BAR_1 = 9.5 * SCALE
    FS_BAR_2 = 9.0 * SCALE

    LW_BORDER = 2.0 * SCALE
    LW_INNER = 1.6 * SCALE
    MUTATION = 11.0 * SCALE

    plt.rcParams.update({
        "font.family": "Aptos Sans",
        "mathtext.fontset": "dejavusans",
        "font.size": FS_BASE,
    })

    fig = plt.figure(figsize=(cm_to_in(18), cm_to_in(12.8)), facecolor="white")

    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
    ax.set_axis_off()

    LEFT = 0.05
    RIGHT = 0.05
    GAP_X = 0.06

    box_w = (1.0 - LEFT - RIGHT - 2 * GAP_X) / 3.0
    x0 = LEFT
    x1 = x0 + box_w + GAP_X
    x2 = x1 + box_w + GAP_X

    y_bottom_bar = 0.04
    h_bottom_bar = 0.075

    GAP_BOTTOM_TO_MCMC = 0.040
    y_mcmc = y_bottom_bar + h_bottom_bar + GAP_BOTTOM_TO_MCMC
    h_mcmc = 0.145

    GAP_MCMC_TO_BOXES = 0.060
    y_boxes = y_mcmc + h_mcmc + GAP_MCMC_TO_BOXES
    h_boxes = 0.400

    y_time_label = y_boxes + h_boxes + 0.035
    y_time_arrow = y_time_label - 0.040
    y_timeline = y_time_label + 0.070

    ax.add_patch(FancyArrow(
        0.06, y_timeline, 0.89, 0,
        width=0.040, head_width=0.070, head_length=0.040,
        length_includes_head=True, color=blue, transform=ax.transAxes
    ))
    ax.text(
        0.51, y_timeline + 0.022, "Discrete timeline (hourly states)",
        ha="center", va="center", fontsize=FS_TITLE, color="white",
        fontweight="bold", transform=ax.transAxes
    )

    x_t0 = x0 + box_w / 2
    x_tn = x1 + box_w / 2
    x_t23 = x2 + box_w / 2

    for x, lab in [(x_t0, r"$t_0$"), (x_tn, r"$t_n$"), (x_t23, r"$t_{23}$")]:
        ax.text(x, y_time_label, lab, ha="center", va="bottom",
                fontsize=FS_TIME, transform=ax.transAxes)
        ax.add_patch(FancyArrow(
            x, y_time_arrow, 0, 0.040,
            width=0.0036, head_width=0.014, head_length=0.012,
            length_includes_head=True, color=blue, transform=ax.transAxes
        ))

    ax.text((x_t0 + x_tn) / 2, y_time_label, r"$\cdots$",
            ha="center", va="bottom", fontsize=FS_DOTS, transform=ax.transAxes)
    ax.text((x_tn + x_t23) / 2, y_time_label, r"$\cdots$",
            ha="center", va="bottom", fontsize=FS_DOTS, transform=ax.transAxes)

    def draw_container(x, y, w, h, title):
        ax.add_patch(Rectangle(
            (x, y), w, h, facecolor="white",
            edgecolor=border, linewidth=LW_BORDER, transform=ax.transAxes
        ))
        ax.text(
            x + w / 2, y + h - 0.06 * h, title,
            ha="center", va="top",
            fontsize=FS_BOX_TITLE, fontweight="bold",
            transform=ax.transAxes, linespacing=1.15
        )

    def state_block(x, y, w, h, label):
        ax.add_patch(Rectangle(
            (x, y), w, h, facecolor=blue, edgecolor="none",
            transform=ax.transAxes
        ))
        ax.text(
            x + w / 2, y + h / 2, label,
            ha="center", va="center",
            fontsize=FS_STATE, color="white",
            fontweight="bold", transform=ax.transAxes
        )

    def draw_initial(x, y, w, h):
        draw_container(x, y, w, h, "Initial distribution\nin $t_0$")
        bx, bw, bh = x + 0.20 * w, 0.60 * w, 0.14 * h
        y_conn, y_disc = y + 0.60 * h, y + 0.32 * h
        state_block(bx, y_conn, bw, bh, "Connected")
        state_block(bx, y_disc, bw, bh, "Disconnected")
        ax.text(x + 0.10 * w, y_conn + 0.5 * bh, r"$p_1^{t_0}$",
                ha="center", va="center", fontsize=FS_MATH, transform=ax.transAxes)
        ax.text(x + 0.10 * w, y_disc + 0.5 * bh, r"$p_2^{t_0}$",
                ha="center", va="center", fontsize=FS_MATH, transform=ax.transAxes)

    def draw_transition(x, y, w, h, sup):
        draw_container(x, y, w, h, f"Transition matrix\nin $t_{{{sup}}}$")
        bx, bw, bh = x + 0.20 * w, 0.60 * w, 0.14 * h
        y_conn, y_disc = y + 0.58 * h, y + 0.30 * h
        state_block(bx, y_conn, bw, bh, "Connected")
        state_block(bx, y_disc, bw, bh, "Disconnected")

        x_mid = bx + bw / 2

        ax.add_patch(FancyArrowPatch(
            (x_mid, y_conn - 0.015 * h), (x_mid, y_disc + bh + 0.015 * h),
            arrowstyle="<->", mutation_scale=MUTATION,
            linewidth=LW_INNER, color=blue, transform=ax.transAxes
        ))
        ax.text(x_mid - 0.12 * w, y_disc + bh + 0.09 * h, rf"$p_{{12}}^{{t_{{{sup}}}}}$",
                ha="right", va="center", fontsize=FS_MATH, transform=ax.transAxes)
        ax.text(x_mid + 0.12 * w, y_disc + bh + 0.09 * h, rf"$p_{{21}}^{{t_{{{sup}}}}}$",
                ha="left", va="center", fontsize=FS_MATH, transform=ax.transAxes)

        ax.add_patch(FancyArrowPatch(
            (bx + 0.05 * bw, y_conn + 0.75 * bh), (bx + 0.55 * bw, y_conn + 0.75 * bh),
            connectionstyle="arc3,rad=0.7", arrowstyle="-|>",
            mutation_scale=MUTATION, linewidth=LW_INNER,
            color=blue, transform=ax.transAxes
        ))
        ax.text(bx + 0.30 * bw, y_conn + 0.95 * bh + 0.06 * h, rf"$p_{{11}}^{{t_{{{sup}}}}}$",
                ha="center", va="bottom", fontsize=FS_MATH, transform=ax.transAxes)

        ax.add_patch(FancyArrowPatch(
            (bx + 0.55 * bw, y_disc + 0.25 * bh), (bx + 0.05 * bw, y_disc + 0.25 * bh),
            connectionstyle="arc3,rad=-0.7", arrowstyle="-|>",
            mutation_scale=MUTATION, linewidth=LW_INNER,
            color=blue, transform=ax.transAxes
        ))
        ax.text(bx + 0.30 * bw, y_disc - 0.12 * h, rf"$p_{{22}}^{{t_{{{sup}}}}}$",
                ha="center", va="top", fontsize=FS_MATH, transform=ax.transAxes)

    draw_initial(x0, y_boxes, box_w, h_boxes)
    draw_transition(x1, y_boxes, box_w, h_boxes, "n")
    draw_transition(x2, y_boxes, box_w, h_boxes, "23")

    ax.text((x0 + x1) / 2 + box_w / 2, y_boxes + 0.52 * h_boxes, r"$\cdots$",
            ha="center", va="center", fontsize=FS_DOTS, transform=ax.transAxes)
    ax.text((x1 + x2) / 2 + box_w / 2, y_boxes + 0.52 * h_boxes, r"$\cdots$",
            ha="center", va="center", fontsize=FS_DOTS, transform=ax.transAxes)

    ax.add_patch(Rectangle(
        (LEFT, y_mcmc), 1.0 - LEFT - RIGHT, h_mcmc,
        facecolor="white", edgecolor=border, linewidth=1.8 * SCALE,
        transform=ax.transAxes
    ))

    hdr_h = 0.24 * h_mcmc
    ax.add_patch(Rectangle(
        (LEFT, y_mcmc + h_mcmc - hdr_h), 1.0 - LEFT - RIGHT, hdr_h,
        facecolor=blue, edgecolor="none", transform=ax.transAxes
    ))
    ax.text(
        LEFT + 0.01 * (1.0 - LEFT - RIGHT), y_mcmc + h_mcmc - hdr_h / 2,
        "MCMC simulation and scaling to E2M2s input",
        ha="left", va="center", fontsize=FS_MCMC_HDR,
        color="white", fontweight="bold", transform=ax.transAxes
    )

    lines = [
        r"1) Simulate trajectories: $s_i(t)\in\{0,1\}$ using $(p^{t_0},\,P^{t})$",
        r"2) Sample EV attributes: battery capacity $C_i$ and willingness $w_i$ (slice sampling)",
        r"3) Aggregate: $A(t)=\sum_i s_i(t)\,C_i\,w_i$  $\rightarrow$  $prob^{EV,plug\!-\!in}_{r,u,t}$",
    ]
    yy = y_mcmc + h_mcmc - hdr_h - 0.12 * h_mcmc
    for ln in lines:
        ax.text(LEFT + 0.02 * (1.0 - LEFT - RIGHT), yy, ln,
                ha="left", va="top", fontsize=FS_MCMC_LINE, transform=ax.transAxes)
        yy -= 0.28 * h_mcmc

    for x in [x_t0, x_tn, x_t23]:
        ax.add_patch(FancyArrow(
            x, y_boxes - 0.01, 0, -(y_boxes - (y_mcmc + h_mcmc)) + 0.01,
            width=0.0048, head_width=0.020, head_length=0.014,
            length_includes_head=True, color=light_grey, transform=ax.transAxes
        ))

    ax.add_patch(Rectangle(
        (LEFT, y_bottom_bar), 1.0 - LEFT - RIGHT, h_bottom_bar,
        facecolor=grey, edgecolor="none", transform=ax.transAxes
    ))
    ax.text(
        0.50, y_bottom_bar + 0.62 * h_bottom_bar,
        "Input (survey): hourly plug-in status (0/1), battery capacity, willingness-to-share",
        ha="center", va="center", fontsize=FS_BAR_1, color="white", transform=ax.transAxes
    )
    ax.text(
        0.50, y_bottom_bar + 0.28 * h_bottom_bar,
        r"Output: empirical $p^{t_0}$, time-specific $P^t$, and $prob^{EV,plug\!-\!in}_{r,u,t}$ profiles",
        ha="center", va="center", fontsize=FS_BAR_2, color="white", transform=ax.transAxes
    )

    plt.show()
    return fig


if __name__ == "__main__":
    fig = show_markov_mcmc_figure()