import typer
from rich.console import Console

from pokeml.commands import data_comm, eda_comm, model_comm, eval_comm

app = typer.Typer(help="Pokémon ML package to predict stats of new pokémon in incoming generation 10")
console = Console()


app.add_typer(data_comm.app, name='data', help="Download, store and clean full Pokédex")
app.add_typer(eda_comm.app, name='eda', help='Display several stats and deploy plots')
app.add_typer(model_comm.app, name='model', help='Tune, train and predict stats')
app.add_typer(eval_comm.app, name='evaluation', help='Evaluate the training and get graphical insights')


def main():
    # Only dispatch to Typer. Do NOT call acquire() here.
    app()


if __name__ == "__main__":
    main()
