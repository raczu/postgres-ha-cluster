import random

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from pgload.sql import (
    QUERIES_BASED_ON_CLUSTER_MODE,
    ClusterMode,
    QueryType,
    pgconnection,
)

app = typer.Typer(help="Database initialization commands for pgload.")

MODE: ClusterMode = typer.Option(
    ClusterMode.REPLICATION,
    "--mode",
    help="Cluster mode for the database, either SMR or sharding with Citus.",
)
WRITE_DSN: str = typer.Option(
    ..., "--write-dsn", help="Write connection string (URI format) for the database."
)
FORCE: bool = typer.Option(False, "--force", help="Drop existing database and create a new one.")
WITH_TEST_DATA: bool = typer.Option(
    False, "--with-test-data", help="Include test data in the database initialization."
)
SCALE: int = typer.Option(1, "--scale", help="Scale factor for the test data size.")
SEED: int | None = typer.Option(None, "--seed", help="Seed for the fake data generator.")


@app.command(help="Initialize the database with or without test data.")
def database(
    dsn: str = WRITE_DSN,
    mode: ClusterMode = MODE,
    force: bool = FORCE,
    with_test_data: bool = WITH_TEST_DATA,
    scale: int = SCALE,
    seed: int | None = SEED,
) -> None:
    seed = random.randint(0, 2**32 - 1) if seed is None else seed
    queries = QUERIES_BASED_ON_CLUSTER_MODE[mode]

    with pgconnection(dsn) as conn:
        if force:
            queries.filter(type=QueryType.WRITE, tags=["database", "drop"])[0](
                conn=conn, metrics=False
            )
        queries.filter(type=QueryType.WRITE, tags=["database", "init"])[0](conn=conn, metrics=False)
        if with_test_data:
            typer.secho(
                "Including test data in the database. This may take a while.",
                fg=typer.colors.YELLOW,
            )
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="Generating and inserting test data...", total=None)
                queries.filter(type=QueryType.WRITE, tags=["fulfill", "testdata"])[0](
                    conn=conn, metrics=False, scale=scale, seed=seed
                )
            typer.echo(
                f"Included test data in database with scale factor: "
                f"{typer.style(scale, fg=typer.colors.BLUE)} "
                f"and seed: {typer.style(seed, fg=typer.colors.BLUE)}."
            )
    typer.secho("Successfully initialized the database.", fg=typer.colors.GREEN)
