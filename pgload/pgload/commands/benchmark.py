import typer

app = typer.Typer(help="Benchmarking commands for pgload.")

WRITE_DSN: str = typer.Option(
    ..., "--write-dsn", help="Write connection string for the database."
)
READ_DSN: str = typer.Option(
    ..., "--read-dsn", help="Read connection string for the database."
)
CLIENTS: int = typer.Option(10, "--clients", help="Number of concurrent clients.")
DURATION: int = typer.Option(
    60, "--duration", help="Duration of the benchmark in seconds."
)


@app.command(help="Run a benchmark on the database.")
def run() -> None: ...
