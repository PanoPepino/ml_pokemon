from pokeml.utils.utils_eda import df_to_markdown, replace_between_markers
import pandas as pd


BEST_ITERATION = '2026_04_21_w_stop'


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

# PREDICTIONS

predictions = pd.read_csv(f'artifacts/predictions/{BEST_ITERATION}.csv')
predictions_md = df_to_markdown(predictions, show_index=False)

replace_between_markers(
    "README.md",
    "<!-- PREDICTIONS -->",
    predictions_md
)
