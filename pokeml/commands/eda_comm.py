import pandas as pd
import typer

from rich.console import Console
from rich.columns import Columns

from pokeml.data.eda_general import bst_dist, compute_baseline, load_data, interval_bst, stats_by_stage
from pokeml.utils.utils_eda import df_to_table, describe_data
from pokeml.visualisation.bst_vs_stage_plot import get_bst_vs_stage_plot
from pokeml.visualisation.gen_bst_plot import get_bst_plot, get_median_bst_plot
from pokeml.utils.utils_commands import CliUI

app = typer.Typer()
console = Console()

ui = CliUI()


@app.command("general_bst", help='Obtain the basic bst distribution in general and by generations')
def general_bst(
    input_path: str = "datasets/pkdx_min.csv"
):
    """
    Run the full acquire_full_pkdx pipeline and display summary EDA.
    """

    console.print('')
    ui.rule("PokéML General BST distribution")
    data_description = describe_data(input_path)
    max_min_overall, max_min_regs, max_min_legs = bst_dist(input_path)

    # BASIC PKDX table
    console.print()
    ui.info(f"[bold white]Pokédex Description[/bold white]")
    table_describe = df_to_table(data_description, show_index=True)
    console.print(table_describe, justify='center')
    console.print()

    # REGULAR and LEGENDARY table
    table_regs = df_to_table(max_min_regs, hide_columns=['extreme', 'generation'])

    # LEGENDARY table
    table_legs = df_to_table(max_min_legs, hide_columns=['extreme', 'generation'])

    # DISPLAY
    ui.info(f"[bold white]Max/Min BST for Regular/Legendary in each generation[/bold white]")
    console.print(Columns([table_regs, table_legs]), justify='center')
    console.print()

    # BST_DIST plot
    over_dist = {interval_bst(load_data(input_path), 170 + i, 20)
                 [0]: interval_bst(load_data(input_path), 170 + i, 20)[1] for i in range(0, 560, 20)}
    get_bst_plot(over_dist)

    # MEDIAN BY GEN plot
    get_median_bst_plot(input_path)

    ui.success("Plots complete")

    ui.panel(
        "Histogram BST general: [bold]plots/eda/total_stats_interval.png[/bold]\n"
        "Histogram BST per generation: [bold]plots/eda/median_bst_interval_per_gen.png[/bold]",
        title="[bold red]Plots created[/bold red]",
    )
    console.print("")


@app.command('bst_vs_stage', help='For each pkmn stage, display how each stage in each generation deviates from overall median')
def bst_dist_stage(
    input_path: str = "datasets/pkdx_min.csv"
):
    df = pd.read_csv(input_path)
    conf_stage_cat = {
        "single": (["single"], "regular"),
        "s1c2": (["s1c2"], "regular"),
        "s2c2": (["s2c2"], "regular"),
        "s1c3": (["s1c3"], "regular"),
        "s2c3": (["s2c3"], "regular"),
        "s3c3": (["s3c3"], "regular"),
        "legends": (None, "legendary"),
    }

    console.print()
    ui.rule("PokéML BST vs stage")
    ui.info(f"[bold white]Splitting Pkdx by stage and rarity[/bold white]")

    mean_stage_cat = stats_by_stage(df, conf_stage_cat)
    baseline = compute_baseline(df)
    get_bst_vs_stage_plot(mean_stage_cat, baseline)

    ui.success("Plots complete")

    ui.panel(
        "Histograms BST vs stage: [bold]plots/eda/bst_vs_stage.png[/bold]",
        title="[bold red]Plots created[/bold red]",
    )
    console.print("")
