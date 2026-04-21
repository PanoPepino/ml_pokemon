import pandas as pd

from pokeml.data.load import *


def bst_dist(df):
    """
    Basic max and mins for each type of poke based on stats
    """

    df = load_data(df)

    # Extremes
    max_min_overall = pd.concat([get_extremes(df, desired_value='total_stats', rarity=cat)
                                for cat in ['legendary', 'regular']])
    max_min_reg_gen = pd.concat([get_extremes(df, desired_value='total_stats',
                                rarity='regular', generation=i) for i in range(1, 10)])

    max_min_legends = pd.concat([get_extremes(df, desired_value='total_stats', rarity='legendary',
                                              generation=i) for i in range(1, 10)])
    return max_min_overall, max_min_reg_gen, max_min_legends


def split_bst_dist(df):
    """
    This func extracts max and mins of a DataFrame. It will normally take info from :func:`bst_dist` and extract in the form of dics max and min of bst for each generation and pokémon rarity.

    Args:
        df (DataFrame):

    Returns:
        set of dicts with max and min.
    """

    max_min_over, max_min_reg, max_min_legs = bst_dist(df)

    min_gen = max_min_reg[max_min_reg['extreme'] == 'min']['total_stats'].to_list()
    max_gen = max_min_reg[max_min_reg['extreme'] == 'max']['total_stats'].to_list()
    max_legs = max_min_legs[max_min_legs['extreme'] == 'max']['total_stats'].to_list()

    return min_gen, max_gen, max_legs


def median_gen(df: str):
    """
    Extract overall median distribution by generation and in general. To be plotted.

    Args:
        df (str): The pat to database

    Returns:
        median_dic, median_verall: dict, float
    """

    df = load_data(df)
    median_dic = {i: float(df[df['generation'] == i]['total_stats'].median()) for i in range(1, 10)}
    median_overall = df['total_stats'].median()
    return median_dic, median_overall


def interval_bst(data: pd.DataFrame,
                 start,
                 interval):
    """
    Basic Func to get the overall BST in intervals
    """

    mask = data[(data['total_stats'] > start) & (data['total_stats'] <= start + interval)]
    count = mask['total_stats'].count()
    return f"{start} - {start + interval}", float(count)


def stats_by_generation(minimal_df: pd.DataFrame,
                        rarity: str,
                        stage: list = None) -> dict:
    """
    This is a function that will create groups based on a given stage, rarity and generation. It will be useful to determine how different evo chains have mean and median accross generations.

    Args:
        minimal_df (pd.DataFrame): The input_dataframe.
        rarity (str): The rarity to group (regular or legendary pokes)
        stage (list, optional): The stage to group. It correspond to the evolution chian.

    Returns:
        dict: For each stage and rarity, returns a dict with the info on how the median/mean stats have changed for each generation.
    """

    mask = minimal_df['rarity'] == rarity
    if stage is not None:
        mask = mask & (minimal_df['stage'].isin(stage))  # Ojito al condicional!

    my_dict = (
        minimal_df[mask].groupby("generation")["total_stats"]
        .agg(mean="mean", median="median", count="count")
        .round(2)
    )
    # .to_dict("index") produces {gen: {metric: value, ...}}
    return my_dict.to_dict("index")


def stats_by_stage(df, conf_stage_cat):
    """
    This is a function that will create groups based on a given stage, rarity and generation. It will be useful to determine how different evo chains have mean and median accross generations.

    Args:
        minimal_df (pd.DataFrame): The input_dataframe.
        rarity (str): The rarity to group (regular or legendary pokes)
        stage (list, optional): The stage to group. It correspond to the evolution chian.

    Returns:
        dict: For each stage and rarity, returns a dict with the info on how the median/mean stats have changed for each generation.
    """

    mean_stage_cat = {}

    for name, (stage_vals, rarity) in conf_stage_cat.items():
        mask = df["rarity"].eq(rarity)
        if stage_vals is not None:
            mask &= df["stage"].isin(stage_vals)

        grouped = (
            df.loc[mask]
            .groupby("generation", observed=True)["total_stats"]
            .agg(["mean", "median", "count"])
        )

        mean_stage_cat[name] = grouped.to_dict(orient="index")

    return mean_stage_cat


def compute_baseline(df):
    """
    Function to compute the median of a given group/stage.
    """

    baseline = (
        df.groupby(["rarity", "stage"], observed=True)["total_stats"]
        .median()
    )

    regular_order = ["single", "s1c2", "s2c2", "s1c3", "s2c3", "s3c3"]
    regular_baseline = [float(baseline.loc[("regular", s)]) for s in regular_order]
    legendary_baseline = float(df.loc[df["rarity"].eq("legendary"), "total_stats"].median())

    return regular_baseline + [legendary_baseline]


def get_extremes(df,
                 desired_value,
                 out_features: list = None,
                 **kwargs):
    """
    Function to extract the min and max values of a value (total_stats, height, weight...) with a set of kwargs in the mask (i.e. total_stats for gen 5 in stage s3c3 for regular pokes)

    Args:
        df (DataFrame): The dataframe to evaluate.
        desired_value ('string'): The chosen column to inspect (any stat, weight, height)
        **kwargs: any conditional to pass to the mask.


    Returns:
        DataFrame: with seletect values
    """

    mask = pd.Series(True, index=df.index)  # This selects all initial rows.
    for col, val in kwargs.items():
        #  this adds to the mask all all **kwargs (i.e. (df['name'] == 'pepe ) & (df['stats'] == ...) &))
        mask &= (df[col] == val)

    filtered = df[mask]
    if filtered.empty:
        return pd.DataFrame(columns=[desired_value])  # Create the data frame with specific cols.

    # Get the extreme values
    min_row = filtered.loc[filtered[desired_value].idxmin()]
    max_row = filtered.loc[filtered[desired_value].idxmax()]

    # ✅ DataFrame with labels
    result = pd.DataFrame([min_row, max_row])
    result['extreme'] = ['min', 'max']  # Label rows
    base_cols = ['extreme', 'name', desired_value, 'generation']
    # Add out_features if provided
    display_cols = base_cols.copy()
    if out_features:
        display_cols += out_features
    else:
        display_cols = display_cols

    return result[display_cols].reset_index(drop=True)
