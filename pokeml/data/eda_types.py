import pandas as pd
import numpy as np


def compare_type_ordering(stage,
                          baseline,
                          df,
                          rarity='regular',
                          min_count=3):
    required_cols = {'rarity', 'stage', 'type', 'construction', 'count', 'deviation'}
    missing = required_cols - set(df.columns)
    if missing:
        raise KeyError(
            f"Missing required columns: {sorted(missing)}. "
            f"Available columns: {list(df.columns)}"
        )

    if rarity == 'legendary':
        subset = df[
            (df['rarity'] == 'legendary') &
            (df['construction'].isin(['dual_t1', 'dual_t2']))
        ].copy()
    else:
        subset = df[
            (df['stage'] == stage) &
            (df['rarity'] == 'regular') &
            (df['construction'].isin(['dual_t1', 'dual_t2']))
        ].copy()

    if subset.empty:
        return pd.DataFrame()

    pivot_dev = subset.pivot_table(
        index='type',
        columns='construction',
        values='deviation',
        aggfunc='first'
    )

    pivot_count = subset.pivot_table(
        index='type',
        columns='construction',
        values='count',
        aggfunc='first'
    ).fillna(0).astype(int)

    if not {'dual_t1', 'dual_t2'}.issubset(pivot_dev.columns):
        return pd.DataFrame()
    if not {'dual_t1', 'dual_t2'}.issubset(pivot_count.columns):
        return pd.DataFrame()

    comparison = pd.DataFrame({
        'type_2': pivot_dev.index,
        'dual_t1_dev': pivot_dev['dual_t1'],
        'dual_t2_dev': pivot_dev['dual_t2'],
        'n_t1': pivot_count['dual_t1'],
        'n_t2': pivot_count['dual_t2']
    }).reset_index(drop=True)

    comparison = comparison[
        (comparison['n_t1'] >= min_count) &
        (comparison['n_t2'] >= min_count)
    ].copy()

    if comparison.empty:
        return comparison

    comparison['difference'] = comparison['dual_t1_dev'] - comparison['dual_t2_dev']
    comparison['abs_diff'] = comparison['difference'].abs()

    if rarity == 'regular':
        comparison['baseline'] = baseline.loc[stage]
    else:
        comparison['baseline'] = float(baseline)

    return comparison.sort_values('abs_diff', ascending=False)


def extract_type_deviations(df):
    mono = df[df['type_2'].isna()].groupby(['type_1', 'stage', 'rarity'])['total_stats'].agg(
        mean='mean', median='median', count='count'
    )
    dual_t1 = df[df['type_2'].notna()].groupby(['type_1', 'stage', 'rarity'])['total_stats'].agg(
        mean='mean', median='median', count='count'
    )
    dual_t2 = df[df['type_2'].notna()].groupby(['type_2', 'stage', 'rarity'])['total_stats'].agg(
        mean='mean', median='median', count='count'
    )

    flat_mono = mono.reset_index()
    flat_dual_t1 = dual_t1.reset_index()
    flat_dual_t2 = dual_t2.reset_index()

    regular = df[df['rarity'].eq('regular')]
    legendary = df[df['rarity'].eq('legendary')]

    regular_baseline = regular.groupby('stage')['total_stats'].median()
    legendary_baseline = legendary['total_stats'].median()

    flat_mono['deviation'] = np.nan
    flat_dual_t1['deviation'] = np.nan
    flat_dual_t2['deviation'] = np.nan

    regular_mask = flat_mono['rarity'].eq('regular')
    legendary_mask = flat_mono['rarity'].eq('legendary')

    flat_mono.loc[regular_mask, 'deviation'] = (
        flat_mono.loc[regular_mask, 'median'] - flat_mono.loc[regular_mask, 'stage'].map(regular_baseline)
    )
    flat_mono.loc[legendary_mask, 'deviation'] = (
        flat_mono.loc[legendary_mask, 'median'] - legendary_baseline
    )
    flat_mono['construction'] = 'mono'

    regular_mask = flat_dual_t1['rarity'].eq('regular')
    legendary_mask = flat_dual_t1['rarity'].eq('legendary')

    flat_dual_t1.loc[regular_mask, 'deviation'] = (
        flat_dual_t1.loc[regular_mask, 'median'] - flat_dual_t1.loc[regular_mask, 'stage'].map(regular_baseline)
    )
    flat_dual_t1.loc[legendary_mask, 'deviation'] = (
        flat_dual_t1.loc[legendary_mask, 'median'] - legendary_baseline
    )
    flat_dual_t1['construction'] = 'dual_t1'

    flat_dual_t2 = dual_t2.reset_index().rename(columns={'type_2': 'type_1'})
    regular_mask = flat_dual_t2['rarity'].eq('regular')
    legendary_mask = flat_dual_t2['rarity'].eq('legendary')

    flat_dual_t2['deviation'] = np.nan
    flat_dual_t2.loc[regular_mask, 'deviation'] = (
        flat_dual_t2.loc[regular_mask, 'median'] - flat_dual_t2.loc[regular_mask, 'stage'].map(regular_baseline)
    )
    flat_dual_t2.loc[legendary_mask, 'deviation'] = (
        flat_dual_t2.loc[legendary_mask, 'median'] - legendary_baseline
    )
    flat_dual_t2['construction'] = 'dual_t2'

    flat_all = pd.concat([flat_mono, flat_dual_t1, flat_dual_t2], ignore_index=True)
    flat_all = flat_all.rename(columns={'type_1': 'type'})
    new_df = flat_all.reindex(columns=["rarity", "stage", "type", "construction",
                              "count", "mean", "median", "deviation"])
    new_df['mean'] = new_df['mean'].round(1)

    return new_df, regular_baseline, legendary_baseline
