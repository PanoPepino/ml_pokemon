import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pokeml.utils.constants_plot import ALPHA, MAIN_COLOR
from pokeml.visualisation.coloring import TYPE_COLORS
from pokeml.data.eda_types import compare_type_ordering


import math
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def type_order_deviation_plot(stage_list,
                              baseline,
                              df,
                              min_count,
                              rarity_list=("regular",),
                              plot_path: Path = 'plots/eda/'):
    if isinstance(stage_list, str):
        stage_list = [stage_list]
    if isinstance(rarity_list, str):
        rarity_list = [rarity_list]

    if not isinstance(baseline, (list, tuple)) or len(baseline) != 2:
        raise ValueError("baseline must be [regular_baseline, legendary_baseline]")

    regular_baseline, legendary_baseline = baseline

    plot_specs = []
    for stage in stage_list:
        for rarity in rarity_list:
            if rarity == "regular":
                plot_specs.append((stage, rarity))
    plot_specs.append((None, "legendary"))

    n_plots = len(plot_specs)
    ncols = 3
    nrows = math.ceil(n_plots / ncols)

    fig, axes = plt.subplots(nrows, ncols, figsize=(5.5 * ncols, 5.3 * nrows))
    axes = np.array(axes).reshape(nrows, ncols)

    for ax in axes.flat:
        ax.set_visible(False)

    if n_plots == 7 and nrows == 3 and ncols == 3:
        positions = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 1),
        ]
    else:
        positions = [(i // ncols, i % ncols) for i in range(n_plots)]

    for i, (stage_value, rarity) in enumerate(plot_specs):
        row, col = positions[i]
        ax = axes[row, col]
        ax.set_visible(True)

        if rarity == "legendary":
            comparison = compare_type_ordering(
                stage=None,
                baseline=legendary_baseline,
                df=df,
                rarity="legendary",
                min_count=min_count
            )
            title_stage = "All stages"
            current_baseline = float(legendary_baseline)
        else:
            comparison = compare_type_ordering(
                stage=stage_value,
                baseline=regular_baseline,
                df=df,
                rarity="regular",
                min_count=min_count
            )
            title_stage = stage_value
            current_baseline = float(regular_baseline.loc[stage_value])

        if comparison is None or comparison.empty:
            ax.set_title(f"{title_stage} | {rarity} (no data)")
            ax.axis("off")
            continue

        note = stability_label(comparison)

        ax.text(
            0.03, 0.97,
            note,
            transform=ax.transAxes,
            fontsize=8,
            verticalalignment='top',
            horizontalalignment='left',
            bbox=dict(boxstyle='round', facecolor='white', alpha=ALPHA, edgecolor=MAIN_COLOR)
        )

        for _, row_data in comparison.iterrows():
            type_name = row_data['type_2']
            x = row_data['dual_t1_dev']
            y = row_data['dual_t2_dev']
            size = min(row_data['n_t1'], row_data['n_t2']) * 160

            ax.scatter(
                x, y,
                s=size,
                color=TYPE_COLORS.get(type_name, 'gray'),
                edgecolor='black',
                linewidth=1,
                alpha=0.7
            )

            ax.text(
                x, y, type_name[:3].upper(),
                fontsize=7, ha='center', va='center', fontweight='bold'
            )

        lims = [
            min(comparison['dual_t1_dev'].min(), comparison['dual_t2_dev'].min()) - 30,
            max(comparison['dual_t1_dev'].max(), comparison['dual_t2_dev'].max()) + 30
        ]

        ax.plot(lims, lims, 'b--', linewidth=1, alpha=ALPHA, label='No ordering effect (y=x)')
        ax.axhline(0, color=MAIN_COLOR, linestyle=':', linewidth=1)
        ax.axvline(0, color=MAIN_COLOR, linestyle=':', linewidth=1)
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.grid(alpha=0.3)

        ax.set_xlabel('Deviation PRIMARY type', fontsize=12, fontweight='bold')
        ax.set_ylabel('Deviation SECONDARY type', fontsize=12, fontweight='bold')
        ax.set_title(
            f'Type Ordering Effect on BST\n'
            f'{title_stage} | {rarity} | baseline={current_baseline:.1f}\n'
            f'(bubble size = min sample size)',
            fontsize=13,
            fontweight='bold'
        )
        ax.legend(fontsize=10)

    for ax in axes.flat:
        if not ax.has_data():
            ax.set_visible(False)

    Path(plot_path).mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(Path(plot_path) / 'type_ordering.png', dpi=500, bbox_inches='tight')
    plt.show()


def stability_label(comparison):
    if comparison is None or comparison.empty:
        return "Stability: no data"

    paired_n = np.minimum(comparison["n_t1"], comparison["n_t2"])
    min_support = int(paired_n.min())
    median_support = int(np.median(paired_n))
    n_points = len(comparison)

    if min_support < 5:
        level = "Low"
    elif min_support < 10:
        level = "Moderate"
    else:
        level = "Higher"

    return (
        f"Stability: {level}\n"
        f"points = {n_points}\n"
        f"min paired n = {min_support}\n"
        f"median paired n = {median_support}"
    )
