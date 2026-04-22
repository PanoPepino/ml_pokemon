import typer
import pandas as pd

from rich.console import Console
from pathlib import Path
from pokeml.utils.utils_commands import CliUI
from pokeml.evaluation.eval import real_vs_predicted
from pokeml.features.preprocess import prepare_data_train
from pokeml.utils.utils_eda import df_to_table

app = typer.Typer()
console = Console()

ui = CliUI()


@app.command('residual', help='Plot the residuals for your trained models')
def plot_residual(
    input_path: str = 'datasets/pkdx_min.csv',
    model_iter: str = None,
):
    console.print('')
    ui.rule("PokéML Evaluation")
    ui.info(f"Predicted vs Actual values for run: [bold]{model_iter}_models.joblib[/bold]")
    prepared_data = prepare_data_train(input_path)

    [real_vs_predicted(f"{model_iter}_{model}", prepared_data)
     for model in ["cat_native", "cat_ordinal", "light_gbm"]]

    # Defining path for out
    p = Path(model_iter)
    out_dir = p.parent
    last = p.name

    out_dir.mkdir(parents=True, exist_ok=True)

    dfs = [pd.read_csv(
        f'artifacts/training/metrics_data_{last}_{model}.csv') for model in ["cat_native", "cat_ordinal", "light_gbm"]]
    metrics_df = pd.concat(dfs, ignore_index=True)

    console.print(df_to_table(metrics_df, show_index=False), justify='center')
    ui.success("Plots complete")
    ui.panel(
        f"Residual plots: [bold]plots/evaluation/{last}_model_name.png[/bold]",
        title=f"[bold red] Residual information [/bold red]",
    )

    console.print('')
