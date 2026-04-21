from pathlib import Path
from typing import Dict


import matplotlib.pyplot as plt

from pokeml.data.eda_general import median_gen, split_bst_dist
from pokeml.utils.constants_plot import *


def get_bst_plot(stats_dic: Dict,
                 plot_path: Path = 'plots/eda/'):

    plt.figure(figsize=(10, 8))
    Path('plots/eda').mkdir(parents=True, exist_ok=True)

    # Prepare data for total_stats_interval
    bins = list(stats_dic.keys())
    counts = list(stats_dic.values())

    # Prepare data for median stats

    # Define total_stats_interval
    plt.bar(bins, counts, width=0.9, alpha=ALPHA, color=MAIN_COLOR, edgecolor=SECOND_COLOR)
    plt.xlabel('BST Interval')
    plt.ylabel('Number of Pokemon in interval')
    plt.title('Pokemon total_stats distribution')
    plt.xticks(rotation=45, ha='right')  # ✅ Fixed rotation
    plt.grid(True, alpha=ALPHA, axis='y')
    plt.tight_layout()
    plt.savefig(plot_path + 'total_stats_interval.png', dpi=500, bbox_inches='tight')


def get_median_bst_plot(df,
                        plot_path: Path = 'plots/eda/'):

    # Get values
    min_gen, max_gen, max_legs = split_bst_dist(df)
    median_dic, median_overall = median_gen(df)
    Path('plots/eda').mkdir(parents=True, exist_ok=True)

    # Then, plot it

    plt.figure(figsize=(8, 8))
    bins = list(range(1, 10, 1))
    counts = list(median_dic.values())

    plt.bar(bins, counts, width=0.7, alpha=ALPHA, color=MAIN_COLOR, edgecolor=SECOND_COLOR)
    plt.plot(bins, min_gen, '.', markersize=10, color=SECOND_COLOR, markeredgecolor='black', label='Min no legends')
    plt.plot(bins, max_gen, '.', color=THIRD_COLOR, markersize=10, markeredgecolor='black', label='Max no legends')
    plt.plot(bins, max_legs, '.', color=FOURTH_COLOR, markersize=10, markeredgecolor='black', label='Max legends')

    plt.axhline(median_overall, color=LINE_COLOR, linestyle='--', label='Median of all gens')
    plt.xlabel('Generation')
    plt.ylabel('Median per gen')
    plt.title('Overall median across gens')
    plt.xticks(bins)
    plt.grid(True, alpha=ALPHA, axis='y')
    plt.legend(bbox_to_anchor=(1, 1))

    plt.ylim(min(min_gen)-10, 810)
    plt.savefig(plot_path + 'median_bst_interval_per_gen.png', dpi=500, bbox_inches='tight')
