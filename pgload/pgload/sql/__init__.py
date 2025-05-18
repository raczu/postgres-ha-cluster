from contextlib import contextmanager
from enum import StrEnum
from typing import Any, Generator
from urllib.parse import urlparse

import psycopg2

from pgload.sql.queries import (
    CREATE_CITUS_SHARDING_DATABASE,
    CREATE_SMR_DATABASE,
    DROP_DATABASE,
    INSERT_TEST_DATA_FOR_SHARDING,
    INSERT_TEST_DATA_FOR_SMR,
)
from pgload.sql.query import Queries, Query, QueryType

__all__ = [
    "pgconnection",
    "Query",
    "Queries",
    "QueryType",
    "ClusterMode",
    "SMRQueries",
    "ShardingQueries",
    "QUERIES_BASED_ON_CLUSTER_MODE",
]


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
    except psycopg2.DatabaseError as exc:
        conn.rollback()
        raise exc
    else:
        conn.commit()
    finally:
        conn.close()


class ClusterMode(StrEnum):
    SHARDING = "sharding"
    REPLICATION = "replication"


class SMRQueries(Queries):
    __root__: list[Query] = [
        DROP_DATABASE,
        CREATE_SMR_DATABASE,
        INSERT_TEST_DATA_FOR_SMR,
    ]


class ShardingQueries(Queries):
    __root__: list[Query] = [
        DROP_DATABASE,
        CREATE_CITUS_SHARDING_DATABASE,
        INSERT_TEST_DATA_FOR_SHARDING,
    ]


QUERIES_BASED_ON_CLUSTER_MODE = {
    ClusterMode.SHARDING: ShardingQueries(),
    ClusterMode.REPLICATION: SMRQueries(),
}
