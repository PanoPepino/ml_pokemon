import pandas as pd


# This function creates a dictionary where each key is the generation and the values is a sublist with the mean, the median and the count for each category and stage.

def stats_by_generation(minimal_df: pd.DataFrame,
                        category: str,
                        stage: list = None) -> dict:
    """
    This is a function that will create groups based on a given stage, category and generation. It will be useful to determine how different evo chains have mean and median accross generations.

    Args:
        minimal_df (pd.DataFrame): The input_dataframe.
        category (str): The category to group (regular or legendary pokes)
        stage (list, optional): The stage to group. It correspond to the evolution chian.

    Returns:
        dict: For each stage and category, returns a dict with the info on how the median/mean stats have changed for each generation.
    """

    mask = minimal_df['category'] == category
    if stage is not None:
        mask = mask & (minimal_df['stage'].isin(stage))  # Ojito al condicional!

    my_dict = (
        minimal_df[mask].groupby("generation")["total_stats"]
        .agg(mean="mean", median="median", count="count")
        .round(2)
    )
    # .to_dict("index") produces {gen: {metric: value, ...}}
    return my_dict.to_dict("index")

###################################################################################


# This function will create a dataframe explaining how, for a given type combination of a given stage, order of types may matter or not.

def compare_type_ordering(stage,
                          baseline,
                          df,
                          category='regular',
                          min_count=3):
    """
    This function compares dual_t1 vs dual_t2 for each type to test if ordering matters.

    Parameters:
    -----------
    stage : str
        Stage to analyze (e.g., 's3c3')
    category : str
        Category to filter (default: 'regular')
    min_count : int
        Minimum sample size required for each construction (default: 3) 

    Returns:
    --------
    For a given stage, returns a dataframe with ALL pokes with a given type as first. It then compares how much their mean deviates from stage's one. It does the same with all pokes with the same type as second. It then checks the difference between both deviations! 

    OBS: There is a minimum number for the counting!
    """

    # Filter data by stage and category
    subset = df[
        (df['stage'] == stage) &
        (df['category'] == category)
    ]

    # Pivot deviations. Create a table to see how pokes with a given type ordering deviate.
    pivot_dev = subset.pivot_table(
        index='type_1',
        columns='construction',
        values='deviation',
        aggfunc='first'
    )

    # Pivot counts
    pivot_count = subset.pivot_table(
        index='type_1',
        columns='construction',
        values='count',
        aggfunc='first'
    ).fillna(0).astype(int)

    # Build comparison dataframe
    comparison = pd.DataFrame({
        'type_2': pivot_dev.index,
        'dual_t1_dev': pivot_dev['dual_t1'],
        'dual_t2_dev': pivot_dev['dual_t2'],
        'n_t1': pivot_count['dual_t1'],
        'n_t2': pivot_count['dual_t2']
    })

    # Filter by minimum count (To have a realistic way of compare only 2/3 pokes with different type ordering could be missleading)
    comparison = comparison[
        (comparison['n_t1'] >= min_count) &
        (comparison['n_t2'] >= min_count)
    ].copy()

    # Calculate difference
    comparison['difference'] = comparison['dual_t1_dev'] - comparison['dual_t2_dev']
    comparison['abs_diff'] = comparison['difference'].abs()

    # Add baseline for reference
    my_baseline = baseline[stage]
    comparison['baseline'] = my_baseline

    return comparison.sort_values('abs_diff', ascending=False)


####################################################################

def get_extremes(df,
                 desired_value,
                 out_features: list,
                 **kwargs):
    """Function to extract the min and max values of a value (total_stats, height, weight...) with a set of kwargs in the mask (i.e. total_stats for gen 5 in stage s3c3 for regular pokes)

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
