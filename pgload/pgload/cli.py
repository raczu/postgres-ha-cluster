import typer
import importlib.metadata

from pgload.commands.generate import generate

app = typer.Typer()
app.command(
    name="generate",
    help="Generate a load for postgres high availability cluster.",
)(generate)


@app.command(help="Show the version of pgload.")
def version() -> None:
    typer.echo(f"pgload {importlib.metadata.version("pgload")}")


if __name__ == "__main__":
    app()
