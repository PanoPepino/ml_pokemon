import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from pokeml.utils.constants_plot import *


def get_bst_vs_stage_plot(mean_stage_cat,
                          baseline,
                          nrows=3,
                          ncols=3,
                          plot_path: Path = 'plots/eda/'):
    """
    This function will return 7 plots (one for each pkmn stage + legendary) where the mean and median bst for a given stage and generation will be displayed.
    """
    fig, axes = plt.subplots(nrows, ncols, figsize=(11, 11.5))
    axes = np.array(axes)

    positions = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 1)   # centered in the third row
    ]

    for idx, (category, gen_data) in enumerate(mean_stage_cat.items()):
        row, col = positions[idx]
        ax = axes[row, col]

        gens = np.array(list(gen_data.keys()))
        means = np.array([v["mean"] for v in gen_data.values()])
        medians = np.array([v["median"] for v in gen_data.values()])
        counts = np.array([v["count"] for v in gen_data.values()])

        x = np.arange(len(gens))
        width = 0.4

        ax.bar(x - width / 2, means, width, label="mean", alpha=ALPHA, color=MAIN_COLOR)
        ax.bar(x + width / 2, medians, width, label="median", alpha=ALPHA, color=SECOND_COLOR)

        for xi, mean, count in zip(x, means, counts):
            ax.text(xi - width / 2, mean, str(count), ha="center", va="bottom", fontsize=10)

        stage_median_of_medians = float(np.median(medians))
        lower_y = min(means.min(), medians.min()) * 0.99
        higher_y = max(means.max(), medians.max()) * 1.1

        ax.set_title(category.capitalize(), fontsize=13, fontweight="bold")
        ax.set_xlabel("Generation")
        ax.set_ylabel("Total Stats")
        ax.axhline(
            stage_median_of_medians,
            color=LINE_COLOR,
            linestyle="--",
            linewidth=1.5,
            label=f"Median of medians: {baseline[idx]:.1f}",
        )
        ax.set_xticks(x)
        ax.set_xticklabels(gens)
        ax.set_ylim(lower_y, higher_y)
        ax.legend()

    axes[2, 0].set_visible(False)
    axes[2, 2].set_visible(False)

    Path('plots/eda').mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(plot_path + 'bst_vs_stage.png', dpi=500, bbox_inches='tight')
