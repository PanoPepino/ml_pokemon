import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from pokeml.utils.constants_plot import *


def residual_scatter(name_model, y_val, y_pred, uncs):
    residuals = y_val-y_pred

    fig, ax = plt.subplots(1, 3, figsize=(18, 5))

    # Actual vs Pred
    ax[0].scatter(y_val, y_pred, alpha=ALPHA, color=MAIN_COLOR, edgecolor=SECOND_COLOR)
    mn, mx = min(y_val.min(), y_pred.min()), max(y_val.max(), y_pred.max())
    ax[0].plot([mn, mx], [mn, mx], color=LINE_COLOR, linestyle="--")
    ax[0].set_title("Actual vs Predicted")
    ax[0].set_xlabel("Actual")
    ax[0].set_ylabel('Predicted')

    # Residual vs Pred
    ax[1].scatter(y_pred, residuals, alpha=ALPHA, color=MAIN_COLOR, edgecolor=SECOND_COLOR)
    ax[1].axhline(0, color=LINE_COLOR, linestyle="--")
    ax[1].set_title("Residuals vs Predicted")
    ax[1].set_xlabel("Predicted")
    ax[1].set_ylabel("Residual deviation")

    ax[2].hist(residuals, bins=40, alpha=ALPHA, color=MAIN_COLOR, edgecolor=SECOND_COLOR)
    ax[2].set_title("Residual Histogram")
    ax[2].set_xlabel("Residual deviation in BST")
    ax[2].set_ylabel("# of Pokes")

    Path('plots/evaluation').mkdir(parents=True, exist_ok=True)

    fig.suptitle(f"Residuals for {name_model}", fontsize=14)
    fig.savefig(f'plots/evaluation/{name_model}_residual_plot.png', dpi=300, bbox_inches='tight')
    plt.tight_layout()
    plt.close(fig)
