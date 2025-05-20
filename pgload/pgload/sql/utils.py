from contextlib import contextmanager
from typing import Any, Generator
from urllib.parse import urlparse

import psycopg2


@contextmanager
def pgconnection(dsn: str, **kwargs: Any) -> Generator:
    """Context manager for psycopg2 connection.

    Args:
        dsn: DSN (URI format) for the database connection.
        **kwargs: Additional arguments to pass to the connection.
    """
    parsed = urlparse(dsn)
    params = {
        "dbname": parsed.path[1:] if parsed.path else None,
        "user": parsed.username,
        "password": parsed.password,
        "host": parsed.hostname,
        "port": parsed.port,
    }
    params.update(kwargs)
    conn = psycopg2.connect(**params)
    try:
        yield conn
    finally:
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
            conn.rollback()
            raise exc
