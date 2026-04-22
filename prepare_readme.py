import pandas as pd
from pathlib import Path
import re
import json
import numpy as np


BEST_ITERATION = '2026_04_22_w_stop'


def df_to_markdown(
    obj,
    show_index: bool = False,
    hide_columns: list[str] | None = None,
    parse_json_columns: list[str] | None = None,
) -> str:
    def _looks_like_json_string(x):
        if not isinstance(x, str):
            return False
        s = x.strip()
        return (s.startswith("[") and s.endswith("]")) or (s.startswith("{") and s.endswith("}"))

    def _parse_json_columns(df):
        df = df.copy()

        if parse_json_columns is not None:
            cols_to_parse = [col for col in parse_json_columns if col in df.columns]
        else:
            cols_to_parse = [
                col for col in df.columns
                if len(df[col].dropna()) > 0 and df[col].dropna().map(_looks_like_json_string).all()
            ]

        for col in cols_to_parse:
            df[col] = df[col].apply(
                lambda x: json.loads(x) if isinstance(x, str) and x.strip() else x
            )

        return df

    def _format_nested(v):
        if isinstance(v, dict):
            lines = []
            for k, val in v.items():
                if isinstance(val, (float, np.floating)):
                    lines.append(f"{k}: {float(val):.2f}")
                elif isinstance(val, (int, np.integer)):
                    lines.append(f"{k}: {val}")
                else:
                    lines.append(f"{k}: {val}")
            return "<br>".join(lines)

        if isinstance(v, (list, tuple, set, np.ndarray)):
            items = []
            for item in v:
                if isinstance(item, (float, np.floating)) and not pd.isna(item):
                    items.append(f"{float(item):.2f}")
                elif isinstance(item, (int, np.integer)) and not pd.isna(item):
                    items.append(str(item))
                elif pd.isna(item) if not isinstance(item, (list, tuple, set, np.ndarray, dict)) else False:
                    continue
                else:
                    items.append(str(item))
            return "<br>".join(items)

        return v

    if isinstance(obj, pd.Series):
        df = obj.to_frame(name=obj.name if obj.name is not None else "value")
    else:
        df = obj.copy()

    df = _parse_json_columns(df)

    if hide_columns:
        df = df.drop(columns=hide_columns, errors="ignore")

    # Format nested/list-like cells before markdown export
    for col in df.columns:
        df[col] = df[col].apply(_format_nested)

    # Round float columns to 2 decimals
    float_cols = df.select_dtypes(include=['float', 'float64', 'float32']).columns
    df[float_cols] = df[float_cols].round(2)

    return df.to_markdown(index=False, floatfmt=".2f", colalign=["center"] * len(df.columns))


def replace_between_markers(file_path: str, marker: str, new_text: str):
    """
    Function to eat a given a given dataframe transformed to md with :func:`df_to_markdown`, find a given marker in the md and replace anything there with the new dataframe. Useful to rewrite things in the README.md
    """

    path = Path(file_path)
    content = path.read_text(encoding="utf-8")

    pattern = re.compile(
        rf"({re.escape(marker)}\s*\n)(.*?)(\n\s*{re.escape(marker)})",
        flags=re.DOTALL
    )

    updated, n = pattern.subn(rf"\1{new_text}\3", content, count=1)

    if n == 0:
        raise ValueError(f"Could not find two '{marker}' markers in {file_path}")

    path.write_text(updated, encoding="utf-8")


def replace_input(file_path: str, old_text: str, new_text: str):
    path = Path(file_path)

    content = path.read_text(encoding="utf-8")

    pattern = re.escape(old_text)

    updated, n = re.subn(pattern, new_text, content, count=1)
    print(updated, n)

    if n == 0:
        raise ValueError(f"Could not find text in {file_path}")

    path.write_text(updated, encoding="utf-8")

# ----------------------------------------------------------------------------------------------

# PREDICTIONS


predictions = pd.read_csv(f'artifacts/predictions/{BEST_ITERATION}_preds.csv')
predictions_md = df_to_markdown(predictions, show_index=False)

replace_between_markers(
    "README.md",
    "<!-- PREDICTIONS -->",
    predictions_md
)

# LEADERBOARDS
dfs = [pd.read_csv(
    f'artifacts/training/metrics_data_{BEST_ITERATION}_{model}.csv') for model in ["cat_native", "cat_ordinal", "light_gbm"]]
metrics_df = pd.concat(dfs, ignore_index=True)
metrics_md = df_to_markdown(metrics_df, show_index=False)

replace_between_markers(
    "README.md",
    "<!-- LEADERBOARD -->",
    metrics_md
)
