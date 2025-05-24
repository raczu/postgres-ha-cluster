import typer

from pgload.commands.benchmark import app as benchmark_app
from pgload.commands.health import app as health_app
from pgload.commands.initialize import app as initialize_app

app = typer.Typer()
app.add_typer(initialize_app, name="init")
app.add_typer(benchmark_app, name="benchmark")
app.add_typer(health_app, name="health")


if __name__ == "__main__":
    app()
