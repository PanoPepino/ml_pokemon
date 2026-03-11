import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .coloring import TYPE_COLORS
from ..data_related.data_selector import compare_type_ordering


def plot_type_order_deviation(stage,
                              baseline,
                              df,
                              min_count,
                              category='regular',
                              save_path=None):
    """
    Scatter plot: dual_t1 vs dual_t2 deviations.
    Points on diagonal = no ordering effect.
    """
    comparison = compare_type_ordering(stage, baseline, df, category, min_count)

    if len(comparison) == 0:
        print(f"Not enough data for {stage}/{category} with min_count={min_count}")
        return

    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot each type
    for _, row in comparison.iterrows():
        type_name = row['type_2']
        x = row['dual_t1_dev']
        y = row['dual_t2_dev']

        # Bubble size = minimum count
        size = min(row['n_t1'], row['n_t2']) * 160

        ax.scatter(x, y, s=size, color=TYPE_COLORS.get(type_name, 'gray'),
                   edgecolor='black', linewidth=1, alpha=0.7)

        # Label
        ax.text(x, y, type_name[:3].upper(),
                fontsize=7, ha='center', va='center', fontweight='bold')

    # Diagonal line (y=x) = no difference
    lims = [
        min(comparison['dual_t1_dev'].min(), comparison['dual_t2_dev'].min()) - 30,
        max(comparison['dual_t1_dev'].max(), comparison['dual_t2_dev'].max()) + 30
    ]
    ax.plot(lims, lims, 'b--', linewidth=1, alpha=0.7, label='No ordering effect (y=x)')

    # Labels
    ax.set_xlabel('Deviation PRIMARY type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Deviation SECONDARY type', fontsize=12, fontweight='bold')
    ax.set_title(
        f'Type Ordering Effect on BST \n{stage} | {category} | (bubble size = min sample size)', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.axhline(0, color='gray', linestyle=':', linewidth=1)
    ax.axvline(0, color='gray', linestyle=':', linewidth=1)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()
