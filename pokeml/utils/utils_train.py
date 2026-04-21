from math import isclose
from itertools import product
import csv
import json
import numpy as np

from datetime import datetime
from pathlib import Path

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def expand_arange(param_def):
    """
    Convert {'start': 0.1, 'stop': 1.0, 'step': 0.1} → [0.1, 0.2, ..., 0.9]
    """

    if isinstance(param_def, dict):
        return np.arange(param_def["start"], param_def["stop"], param_def["step"]).tolist()
    return param_def


def load_tuning_grid(config_path: Path):
    """
    Load compact JSON and expand to full GridSearchCV param_grid.
    """

    with open(config_path) as f:
        config = json.load(f)

    # Expand common params
    common = {k: expand_arange(v) for k, v in config["common_params"].items()}

    # Merge into model-specific grids
    params_grid = {}
    for model_name, model_params in config["params_grid"].items():
        full_params = {**common, **{k: expand_arange(v) for k, v in model_params.items()}}
        params_grid[model_name] = full_params

    return params_grid


def expand_spec(spec):
    start = spec["start"]
    stop = spec["stop"]
    step = spec["step"]

    values = []
    x = start
    while x <= stop or isclose(x, stop, rel_tol=1e-9, abs_tol=1e-12):
        values.append(round(x, 12))
        x += step
    return values


def expand_section(section):
    keys = list(section.keys())
    value_lists = [expand_spec(section[k]) for k in keys]

    combos = []
    for values in product(*value_lists):
        combos.append(dict(zip(keys, values)))
    return combos


def load_combinations(cfg):
    common_combos = expand_section(cfg["common_params"])

    model_combos = {}
    for model_name, section in cfg["params_grid"].items():
        model_specific = expand_section(section)
        all_for_model = []
        for c in common_combos:
            for m in model_specific:
                all_for_model.append({**c, **m})
        model_combos[model_name] = all_for_model

    return model_combos


def load_json(path: str) -> dict:
    path_file = Path(path)
    with path_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: str) -> dict:
    path_file = Path(path)
    with path_file.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))  # Rows as dicts


def get_model(filename):
    parts = filename.rsplit('_', 2)  # Splits into 3 max from right
    if len(parts) == 3:
        return '_'.join(parts[-2:])  # imp1_imp2.png
    return filename  # Fallback


def regression_metrics(y_true, y_pred) -> dict:
    dic_to_return = {
        'R2': float(r2_score(y_true, y_pred)),
        'RMSE': float(np.sqrt(mean_squared_error(y_true, y_pred))),
        'MAE': float(mean_absolute_error(y_true, y_pred))
    }
    return dic_to_return
