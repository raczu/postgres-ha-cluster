import io
import itertools
from contextlib import contextmanager
from dataclasses import astuple
from typing import Any, Generator, Iterator
from urllib.parse import urlparse

import psycopg2


@contextmanager
def pgconnection(dsn: str, timeout: int = 5, **kwargs: Any) -> Generator:
    """Context manager for psycopg2 connection.

    Args:
        dsn: DSN (URI format) for the database connection.
        timeout: Connection timeout in seconds.
        **kwargs: Additional arguments to pass to the connection.
    """
    parsed = urlparse(dsn)
    if not parsed.hostname or not parsed.scheme.startswith("postgres"):
        raise ValueError(f"Invalid DSN: {dsn}")
    params = {
        "dbname": parsed.path[1:] if parsed.path else None,
        "user": parsed.username,
        "password": parsed.password,
        "host": parsed.hostname,
        "port": parsed.port,
        "connect_timeout": timeout,
    }
    params.update(kwargs)
    conn = None
    try:
        conn = psycopg2.connect(**params)
        yield conn
    finally:
        if conn:
            conn.close()


@contextmanager
def pgtransaction(conn: Any) -> Generator:
    """Context manager for psycopg2 transaction.

    Args:
        conn: psycopg2 connection to database.
    """
    with conn.cursor() as cur:
        try:
            yield cur
            conn.commit()
        except psycopg2.DatabaseError as exc:
            if not conn.closed:
                conn.rollback()
            raise exc


def pgaddr(conn: Any) -> str:
    """
    Get the address of the node from the connection.
    """
    with pgtransaction(conn) as tx:
        tx.execute("SELECT inet_server_addr() AS address")
        return tx.fetchone()[0]


def write2buffer(rows: list[Any]) -> io.StringIO:
    buf = io.StringIO()
    buf.writelines("\t".join(map(str, astuple(row))) + "\n" for row in rows)
    buf.seek(0)
    return buf


def batchify(iterable: list[Any], size: int) -> Iterator[list[Any]]:
    iterator = iter(iterable)
    return iter(lambda: list(itertools.islice(iterator, size)), [])
