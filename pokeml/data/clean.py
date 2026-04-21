"""
Script to clean and arrange the complete scrapped Pkdx
"""


from typing import Callable

import pandas as pd

from pathlib import Path
from pokeml.constants import REGULAR_POKES, REGIONS, BEAST_GEN_9, PARADOX, PARADOX_LEGEND
from pokeml.data.load import load_data


def change_id(df, base_max=1025):
    """
    For rows with id > base_max, reassign ids to a new continuous range
    starting at base_max + 1, preserving order.
    """
    # Mask for rows to change
    mask = df['id'] > base_max

    # Get the unique ids to remap, in order of appearance
    unique_bad_ids = df.loc[mask, 'id'].unique()

    # Build a mapping: old_id -> new_id
    new_start = base_max + 1
    mapping = {
        old: new_start + i
        for i, old in enumerate(unique_bad_ids)
    }

    # Apply mapping only where id > base_max
    df.loc[mask, 'id'] = df.loc[mask, 'id'].map(mapping)

    return df


def parse_and_rename(df):
    """
    Rename pokes for easier manipulation.
    """
    df = df.copy()

    # 0) Special case: Tauros Paldea combat breed -> canonical tauros_paldea

    df.loc[
        (df["name"] == "tauros-paldea-combat-breed") & (df["generation"] == 1),
        "name"
    ] = "tauros_paldea"

    df.loc[
        (df["name"] == "tauros_paldea") & (df["generation"] == 1),
        "generation"
    ] = 9

    # 1) Normalize separators
    df["name"] = df["name"].str.replace("-", "_", regex=False)

    # 3) Normalize Hisuian legendary forms
    df["name"] = df["name"].str.replace("origin", "hisui", regex=False)

    # 4) Strip weird suffixes only for names that are not:
    #    - in REGULAR_POKES, and
    #    - do not end with a known region suffix

    def normalize_name(x: str) -> str:
        if x in REGULAR_POKES:
            return x
        if "_" not in x:
            return x
        if any(x.endswith(region) for region in REGIONS):
            return x
        return x.split("_")[0]

    df["name"] = df["name"].apply(normalize_name)

    # 5) Category normalization -> rarity
    df["category"] = df["category"].replace({
        "mythical": "legendary",
        "baby": "regular",
    })
    df = df.rename(columns={"category": "rarity"})

    return df


def update_generation(df):
    """
    Update target_column where search_column contains word. When a given string (in words) is detected, the generation in gens get updated.
    """

    gens = ['7', '8', '9', '9']
    for word, gen in zip(REGIONS, gens):
        mask = df['name'].str.contains(word, case=False, na=False)
        df.loc[mask, 'generation'] = int(gen)
    return df


def change_stage(df):
    """
    Fix stage and rarity values for special cases.
    """
    df = df.copy()

    df.loc[df["name"].isin(PARADOX), "stage"] = "single"
    df.loc[df["name"].isin(PARADOX_LEGEND), "rarity"] = "legendary"
    df.loc[df["name"] == "meltan", "stage"] = "s1c2"
    df.loc[df["name"] == "melmetal", "stage"] = "s2c2"
    df.loc[df["name"].isin(BEAST_GEN_9), "stage"] = "single"

    return df


def split_type_egg(df):
    """
    Simply to split types and eggs.
    """
    df = df.copy()

    df[["type_1", "type_2"]] = df["types"].str.split(r"\s\|\s", n=1, expand=True)
    df[["egg_group_1", "egg_group_2"]] = df["egg_groups"].str.split(r"\s\|\s", n=1, expand=True)

    df = df.drop(columns=["types", "egg_groups"])

    return df


def clean_pkdx_raw(in_path: Path | str,
                   out_path: Path | str) -> None:

    path_to_pd = Path(in_path)
    out_pd = Path(out_path)

    raw_df = load_data(path_to_pd)

    new_id = change_id(raw_df)
    parname = parse_and_rename(new_id)
    upgen = update_generation(parname)
    chstg = change_stage(upgen)
    type_egg = split_type_egg(chstg)

    out_pd.parent.mkdir(parents=True, exist_ok=True)
    type_egg.to_csv(out_pd, index=False)


def get_pkdx_minimal(
        in_path: Path | str,
        out_path: Path | str,
        features: list[str]) -> None:

    path_to_pd = Path(in_path)
    out_pd = Path(out_path)

    df = load_data(path_to_pd)
    trimmed_pkdx = df[features]

    out_pd.parent.mkdir(parents=True, exist_ok=True)
    trimmed_pkdx.to_csv(out_pd, index=False)
