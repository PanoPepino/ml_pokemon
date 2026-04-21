import typer

from rich.console import Console
from pathlib import Path

from pokeml.data.clean import clean_pkdx_raw, get_pkdx_minimal
from pokeml.constants import MINIMAL_FEATURES
from pokeml.data.acquire import acquire_full_pkdx
from pokeml.utils.utils_commands import CliUI

app = typer.Typer()
console = Console()

ui = CliUI()


@app.command('acquire', help='Download the Full Pokédex of existing Pokémon')
def main(
    output_path: Path = typer.Option(
        "datasets/pkdx_raw.csv",
        "--output-path",
        "-o",
        help="Where to save the acquired full Pokédex CSV",
    )
):
    """
    Download the full Pokédex and save it as csv.
    """
    acquire_full_pkdx(output_path, printer=typer.echo)


@app.command('clean', help='Clean a scrapped database for easier manipulation')
def clean(
    input_path: str = "datasets/pkdx_raw.csv",
    output_path_clean: str = "datasets/pkdx_clean.csv",
    output_path_minimal: str = "datasets/pkdx_min.csv",
):
    """
    Run the full acquire_full_pkdx pipeline and save it in output_path.
    """

    console.print('')
    ui.rule('PokéML Cleaning')
    ui.info(f'Modifying wrong entries, cleaning and simplifying raw Pokédex at [bold]{input_path}[/bold]')

    clean_pkdx_raw(input_path, output_path_clean)
    get_pkdx_minimal(output_path_clean, output_path_minimal, MINIMAL_FEATURES)
    ui.success("Cleaning complete")
    ui.panel(
        f"Clean Pkdx: [bold]{output_path_clean}[/bold]\n"
        f"Minimal Pkdx: [bold]{output_path_minimal}[/bold]",
        title=f"[bold red] New Generated Pkdx [/bold red]",
    )

    console.print('')
