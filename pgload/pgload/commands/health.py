import re
from urllib.parse import urlparse

import psycopg2
import typer
from rich.console import Console
from rich.table import Table

from pgload.sql.utils import pgconnection, pgtransaction

app = typer.Typer(help="Database health check commands for pgload.")

DSN: str = typer.Option(..., "--dsn", help="Database connection strings to check health.")
DISPLAY: bool = typer.Option(True, "--display", help="Display the health check results in a table.")


class Node:
    def __init__(self, dsn: str) -> None:
        parsed = urlparse(dsn)
        if not parsed.hostname or not parsed.scheme.startswith("postgres"):
            raise ValueError(f"Invalid DSN: {dsn}")
        self.dsn = dsn
        self.address = (
            f"{parsed.hostname}:{parsed.port}" if parsed.port else f"{parsed.hostname}:5432"
        )
        self.healthy = False


@app.command(help="Check the health of the database(s).")
def check(dsn: str = DSN, display: bool = DISPLAY) -> None:
    nodes = [Node(dsn=d.strip()) for d in re.split(r"[ ,]+", dsn) if d.strip()]
    if not nodes:
        raise typer.BadParameter("At least one DSN must be provided.")

    for node in nodes:
        try:
            with pgconnection(node.dsn) as conn:
                with pgtransaction(conn) as tx:
                    tx.execute("SELECT 1;")
                    node.healthy = True
        except psycopg2.DatabaseError:
            pass

    if display:
        table = Table()
        table.add_column("Node", justify="left")
        table.add_column("Health", justify="left")
        for node in nodes:
            color = typer.colors.GREEN if node.healthy else typer.colors.RED
            status = "healthy" if node.healthy else "unhealthy"
            table.add_row(f"[{typer.colors.BLUE}]{node.address}", f"[{color}]{status}")
        console = Console()
        console.print(table)

    if not all(node.healthy for node in nodes):
        typer.secho("Some nodes are unhealthy.", fg=typer.colors.RED)
        raise typer.Exit(1)
    typer.secho("All nodes are healthy.", fg=typer.colors.GREEN)
