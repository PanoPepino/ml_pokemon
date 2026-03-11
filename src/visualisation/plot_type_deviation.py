import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .coloring import TYPE_COLORS

# Here, together with the help of AI, I create a func to display the total_stats median deviation for each type construction and stage.


def plot_type_deviations(stage,
                         category='regular',
                         baseline=pd.DataFrame,
                         df=pd.DataFrame,
                         save_path=None):
    """
    Plot type total_stats deviations by construction for a given stage and category.

    Parameters:
    -----------
    stage : str
        Stage to plot (e.g., 's2c2', 's3c3')
    category : str
        Category to filter (default: 'regular')
    baseline: DataFrame
        The dataframe to be use as a regular baseline (the horizontal line)
    df: DataFrame
        The dataframe withe the information counting all pokemon with monotype, type as first, type as second to compute respective medians and deviations from baseline. MUST BE FLAT!
    """

    # Get overall median of a given stage
    my_baseline = baseline[stage]

    # Pivot data for deviations. It basically rearrange previous tables for easy column comparison/finding.
    pivot = df[
        (df['stage'] == stage) &
        (df['category'] == category)
    ].pivot_table(
        index='type_1',
        columns='construction',
        values='deviation',
        aggfunc='first'
    )

    # Pivot data for counts.
    counts = df[
        (df['stage'] == stage) &
        (df['category'] == category)
    ].pivot_table(
        index='type_1',
        columns='construction',
        values='count',
        aggfunc='first'
    ).fillna(0).astype(int)

    # Check which constructions are available
    available_constructions = [c for c in ['mono', 'dual_t1', 'dual_t2'] if c in pivot.columns]

    if len(available_constructions) == 0:
        print(f"ERROR: No data for {stage}/{category}")
        return

    # Create plot
    fig, ax = plt.subplots(figsize=(15, 5))

    # Bar positions
    x = np.arange(len(pivot))
    width = 0.8 / len(available_constructions)

    # Construction styles
    construction_styles = {
        'mono': ('', 1.0),
        'dual_t1': ('///', 0.85),
        'dual_t2': ('...', 0.85)
    }

    for i, constr in enumerate(available_constructions):
        pattern, alpha = construction_styles[constr]
        values = pivot[constr].values
        colors = [TYPE_COLORS[type_name] for type_name in pivot.index]

        bars = ax.bar(x + i*width, values, width,
                      label=constr,
                      color=colors,
                      alpha=alpha,
                      hatch=pattern,
                      edgecolor='indigo',
                      linewidth=0.8)

        # Add count labels
        for j, (bar, type_name) in enumerate(zip(bars, pivot.index)):
            if pd.notna(values[j]):
                count_val = counts.loc[type_name, constr]
                y_pos = values[j] + (1 if values[j] > 0 else -2)
                ax.text(bar.get_x() + bar.get_width()/2, y_pos,
                        f'{count_val}', ha='center',
                        va='bottom' if values[j] > 0 else 'top',
                        fontsize=7, fontweight='bold')

    # my_Baseline line
    ax.axhline(0, color='gray', linestyle='--', linewidth=2, label=f'my_Baseline ({my_baseline})')

    # Formatting
    ax.set_ylabel('Deviation from stage median', fontsize=12, fontweight='bold')
    ax.set_xlabel('Type', fontsize=12, fontweight='bold')
    ax.set_title(f'Stage: {stage} | Category: {category} | my_Baseline: {my_baseline}',
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x + width * (len(available_constructions) - 1) / 2)
    ax.set_xticklabels([t.capitalize() for t in pivot.index], rotation=0, ha='right')
    ax.legend(title='Construction', loc='lower right', fontsize=9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=500, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()
