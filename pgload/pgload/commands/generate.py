import typer

HOST: str = typer.Option("localhost", "-h", "--host", help="Database server hostname.")
PORT: int = typer.Option(5432, "-p", "--port", help="Database server port.")
CLIENTS: int = typer.Option(1, "-c", "--clients", help="Number of clients simulating the load.")


def generate(
    host: str = HOST,
    port: int = PORT,
    clients: int = CLIENTS,
) -> None:
    print("This is the generate command of pgload")
