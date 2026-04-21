from rich.console import Console
from rich.panel import Panel

console = Console()


class CliUI:
    def rule(self, title: str):
        console.rule(f"[bold red]{title}[/bold red]", style='white')

    def info(self, msg: str):
        console.print(f"[white]•[/white] {msg}")

    def success(self, msg: str):
        console.print(f"[green]✔[/green] {msg}")

    def warning(self, msg: str):
        console.print(f"[yellow]⚠[/yellow] {msg}")

    def panel(self, msg: str, title: str = "Info"):
        console.print(Panel(msg, title=title, border_style="white"))


class PkdxUI:
    def header(self, title: str):
        console.print()
        console.rule(f"[bold red]{title}[/bold red]", style="white")

    def phase(self, title: str):
        console.rule(f"[bold red]{title}[/bold red]", style="white")

    def info(self, msg: str):
        console.print(f"[white]•[/white] {msg}")

    def item(self, msg: str):
        console.print(f"  [white]{msg}[/white]")

    def success(self, msg: str):
        console.print(f"[green]✔[/green] {msg}")

    def warning(self, msg: str):
        console.print(f"[yellow]⚠[/yellow] {msg}")

    def error(self, msg: str):
        console.print(f"[red]✘[/red] {msg}")

    def summary(self, title: str, body: str):
        console.print(Panel(body, title=title, border_style="white"))
