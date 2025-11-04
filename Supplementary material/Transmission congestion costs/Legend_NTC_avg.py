import matplotlib.pyplot as plt
import numpy as np

def create_linewidth_legend_custom(
    linestyles,
    line_length=0.5,
    x_start=0.6,
    label_dx=0.15,
    unit_label="m€/MW/yr",
    unit_fontsize=13,
    label_fontsize=11
):
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Open Sans', 'DejaVu Sans', 'Arial']

    fig, ax = plt.subplots(figsize=(3.5, 2.7))
    ax.axis('off')

    line_color = '#243b6b'

    n_lines = len(linestyles)
    total_height = 1.5
    spacing = total_height / (n_lines + 1)
    y_positions = [total_height - (i + 0.5) * spacing for i in range(n_lines)]

    x_center = x_start + line_length / 2.0
    unit_y = total_height + 0.25
    ax.text(
        x_center, 0.15, unit_label,
        ha='center', va='top',
        fontsize=unit_fontsize, fontfamily='sans-serif',
        fontweight='bold'
    )

    ax.set_xlim(0, x_start + line_length + label_dx + 0.8)
    ax.set_ylim(0, unit_y + 0.35)

    for (shadow_price, linewidth), y_pos in zip(linestyles, y_positions):
        ax.plot(
            [x_start, x_start + line_length], [y_pos, y_pos],
            color=line_color, linewidth=linewidth, solid_capstyle='round'
        )
        ax.text(
            x_start + line_length + label_dx, y_pos, f'{shadow_price}',
            ha='left', va='center',
            fontsize=label_fontsize, fontfamily='sans-serif'
        )

    plt.tight_layout()
    return fig


linestyles_example = [
    (0, 2),
    (0.4, 5),
    (0.7, 8),
    (1.1, 12)
]

custom_legend = create_linewidth_legend_custom(linestyles_example)
plt.show()