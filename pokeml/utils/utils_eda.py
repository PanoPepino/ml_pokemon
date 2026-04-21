from pathlib import Path
import re
import json
import pandas as pd
import numpy as np

from rich.table import Table
from rich import box
from pokeml.data.load import *


def describe_data(df):

    df = load_data(df)

    return df['total_stats'].describe()


# Convert a DataFrame-like into a Rich table


def df_to_table(
    obj,
    title: str = None,
    show_index: bool = False,
    index_name: str | None = None,
    hide_columns: list[str] | None = None,
    parse_json_columns: list[str] | None = None,
    table_box=box.ROUNDED,
    border_style: str = "white",
) -> Table:

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

    def _format_value(v):
        if isinstance(v, dict):
            lines = []
            for k, val in v.items():
                if isinstance(val, (float, np.floating)):
                    lines.append(f"{k}: {float(val):.2f}")
                elif isinstance(val, (int, np.integer)):
                    lines.append(f"{k}: {val}")
                else:
                    lines.append(f"{k}: {val}")
            return "\n".join(lines)

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
            return "\n".join(items)

        if pd.isna(v) if not isinstance(v, (list, tuple, set, np.ndarray, dict)) else False:
            return ""

        if isinstance(v, (float, np.floating)):
            return f"{float(v):.2f}"
        if isinstance(v, (int, np.integer)):
            return str(v)

        return str(v)

    if isinstance(obj, pd.Series):
        df = obj.to_frame(name=obj.name if obj.name is not None else "value")
    else:
        df = obj.copy()

    df = _parse_json_columns(df)

    if hide_columns:
        df = df.drop(columns=hide_columns, errors="ignore")

    t = Table(
        title=title,
        show_header=True,
        header_style="bold red",
        show_lines=True,
        box=table_box,
        border_style=border_style,
    )

    if show_index:
        label = index_name if index_name is not None else (df.index.name or "")
        t.add_column(str(label), overflow="fold")

    for col in df.columns:
        t.add_column(str(col), overflow="fold")

    for idx, row in df.iterrows():
        values = [_format_value(idx)] if show_index else []
        values.extend(_format_value(v) for v in row.values)
        t.add_row(*values)

    return t


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
