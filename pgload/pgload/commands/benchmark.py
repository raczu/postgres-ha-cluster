import signal
import threading
import time

import typer
from prometheus_client import start_http_server

from pgload.commands.health import check
from pgload.sql import (
    QUERIES_BASED_ON_CLUSTER_MODE,
    ClusterMode,
    QueryType,
    SQLWorkerManager,
)

app = typer.Typer(help="Benchmarking commands for pgload.")

MODE: ClusterMode = typer.Option(
    ClusterMode.REPLICATION,
    "--mode",
    help="Cluster mode for the database, either SMR or sharding with Citus.",
)
WRITE_DSN: str | None = typer.Option(
    None, "--write-dsn", help="Write connection string for the database."
)
READ_DSN: str | None = typer.Option(
    None, "--read-dsn", help="Read connection string for the database."
)
CLIENTS: int = typer.Option(10, "--clients", help="Number of concurrent clients.")
WRITE_CLIENTS: int = typer.Option(
    0,
    "--write-clients",
    help="Number of concurrent clients for write operations (rest will be read).",
)
DURATION: int | None = typer.Option(
    None,
    "--duration",
    help="Duration of the benchmark in seconds or None for infinite.",
)
METRICS_SERVER_PORT: int = typer.Option(
    8080,
    "--metrics-port",
    help="Port for the Prometheus metrics server.",
)


@app.command(help="Run a benchmark on the database.")
def run(
    mode: ClusterMode = MODE,
    write_dsn: str | None = WRITE_DSN,
    read_dsn: str | None = READ_DSN,
    clients: int = CLIENTS,
    write_clients: int = WRITE_CLIENTS,
    duration: int | None = DURATION,
    metrics_port: int = METRICS_SERVER_PORT,
) -> None:
    if not (write_dsn or read_dsn):
        typer.BadParameter("At least one of --write-dsn or --read-dsn must be provided.")
    if write_clients > clients:
        raise typer.BadParameter("Number of write clients cannot exceed total number of clients.")

    check(",".join(dsn for dsn in (write_dsn, read_dsn) if dsn), display=False)
    stop_event = threading.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda signum, frame: stop_event.set())
    start_http_server(metrics_port)

    queries = QUERIES_BASED_ON_CLUSTER_MODE[mode]
    manager = SQLWorkerManager(stop_event=stop_event)
    if write_dsn:
        manager.add(
            dsn=write_dsn,
            queries=queries.filter(type=QueryType.WRITE, tags=["benchmark"])
            + queries.filter(type=QueryType.MIXED, tags=["benchmark"]),
            num=write_clients,
        )

    if read_dsn:
        manager.add(
            dsn=write_dsn,
            queries=queries.filter(type=QueryType.WRITE, tags=["benchmark"]),
            num=write_clients,
        )

    typer.secho(
        f"Starting benchmark ("
        f"duration: {f'{duration}s' if duration is not None else 'inf'}, "
        f"clients: {clients}"
        f")...",
        fg=typer.colors.YELLOW,
    )
    manager.start()

    start = time.time()
    while not stop_event.is_set():
        if duration and (time.time() - start) >= duration:
            stop_event.set()
            break

        if not manager.all_alive():
            typer.secho("One or more workers have stopped unexpectedly.", fg=typer.colors.RED)
            typer.secho("Stopping benchmark...", fg=typer.colors.YELLOW)
            stop_event.set()
        time.sleep(0.1)

    manager.stop()
    typer.secho("Benchmark completed.", fg=typer.colors.GREEN)
