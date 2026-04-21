import typer
import pandas as pd
import json

from pathlib import Path
from rich.console import Console
from pokeml.models.predict import predict_stats, predict_all_models
from pokeml.models.tuning import tuning
from pokeml.models.train import train
from pokeml.features.preprocess import prepare_data_train, prepare_data_predict
from pokeml.utils.utils_eda import df_to_table
from pokeml.utils.utils_train import load_json
from pokeml.utils.utils_commands import CliUI

app = typer.Typer()
console = Console()

ui = CliUI()


@app.command('tuning', help='Find the best suited set of parameters. Extract best params')
def tune_data(
        input_path: str = 'datasets/pkdx_min.csv',
        input_config: str = 'configs/tuning_easy.json',
        iterations: int = 1,
        output_name: str = 'yyyy_mm_dd_something',  # Declare name of your json output (w/o extension)
):
    console.print('')
    ui.rule("PokéML Tuning")
    ui.info(f"Preparing initial data from [bold]{input_path}[/bold]")
    to_tune = prepare_data_train(input_path)
    with console.status(
        f"[bold green]Tuning models[/bold green] ({iterations} iterations) ..."
    ):
        result = tuning(to_tune,
                        my_grid=f'configs/{input_config}.json',
                        search_iter=iterations,
                        output_name=output_name)

    ui.success("Tuning complete")
    ui.info(f"Relevant information for the best run:")
    df = pd.read_csv(Path(f'artifacts/tuning/{output_name}_cv.csv'))
    console.print(df_to_table(df, parse_json_columns=['top_features', 'top_feature_weights']), justify='center')
    ui.panel(
        f"Best parameters: [bold]artifacts/tuning/{output_name}_bp.json[/bold]\n"
        f"CV summary: [bold]artifacts/tuning/{output_name}_cv.csv[/bold]",
        title=f"[bold red] Tuning information [/bold red]",
    )

    console.print('')


@app.command('train', help='Based on parameters found with tune, train the model. Create training curves')
def train_data(
    input_json: str = 'yyyy_mm_dd_something',
    input_path: str = 'datasets/pkdx_min.csv',
    output_joblib: str = 'yyyy_mm_dd_something',
    stop_loss: bool = False,
    early_stop: int = 40,
):
    console.print('')
    ui.rule('PokéML Training')
    ui.info(f"Preparing initial data from [bold]{input_path}[/bold]")

    chosen_tuning = f"artifacts/tuning/{input_json}.json"
    ui.info(f"Tuning .json file: [bold]{chosen_tuning}[/bold]")
    to_train = prepare_data_train(input_path)
    params = load_json(chosen_tuning)

    info_stop = []
    if stop_loss:
        ui.info(f"Stop loss activated. Early stopping rounds at: {early_stop}")
        info_stop.append('w_stop')
        for key in params.keys():
            params[key]["early_stopping_rounds"] = early_stop
    else:
        info_stop.append('no_stop')

    with console.status(
        f"[bold green]Training models[/bold green] ..."
    ):

        result = train(to_train, params=params, output_name=output_joblib)

    ui.success("Training complete")
    ui.panel(
        f"Trained models: [bold]artifacts/models/{output_joblib}.joblib[/bold]\n"
        f"Training curves: [bold]plots/training/{output_joblib}_all_models_loss.png[/bold]",
        title=f"[bold red] Training information [/bold red]",
    )

    console.print('')


@app.command('predict', help='Load a database of new pokémon without defined BST and predict their stats')
def predict_data(
        input_run: str = 'yyyy_mm_dd_info',  # Declare name of joblibs (no extension)
        new_poke_data: str = 'datasets/new_pokes.csv',
        output_preds: str = 'yyyy_mm_dd_name'):  # Declare name of csv (no ext)

    to_predict = prepare_data_predict(new_poke_data)
    predict_all_models(run=input_run,
                       new_poke_data=to_predict,
                       output_preds=output_preds)
