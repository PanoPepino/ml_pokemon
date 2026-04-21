import matplotlib.pyplot as plt

from pathlib import Path
import matplotlib.pyplot as plt

from pokeml.utils.constants_plot import MAIN_COLOR, SECOND_COLOR


def plot_loss(name_model: str, evals: dict, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if 'cat_ordinal' in name_model or 'cat_native' in name_model:
        learn = evals['learn']['RMSEWithUncertainty']
        validation = evals['validation_1']['RMSEWithUncertainty']

    elif 'light_gbm' in name_model:
        learn = evals['training']['quantile']
        validation = evals['valid_1']['quantile']

    else:
        raise ValueError(
            f"Unknown model name: {name_model}. Available eval keys: {list(evals.keys())}"
        )

    ax.plot(learn, label='Train Loss', color=MAIN_COLOR)
    ax.plot(validation, label='Val Loss', color=SECOND_COLOR)
    ax.set_title(f'{name_model}')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Loss')
    ax.legend()

    return ax
