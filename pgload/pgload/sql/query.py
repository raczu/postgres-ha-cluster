from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Callable

import psycopg2

from pgload.metrics import QUERY_COUNTER, QUERY_ERROR_COUNTER, QUERY_LATENCY_HISTOGRAM
from pgload.sql.utils import pgaddr


class QueryType(StrEnum):
    READ = "READ"
    WRITE = "WRITE"
    MIXED = "MIXED"


@dataclass
class Query:
    callable: Callable[..., Any]
    type: QueryType
    tags: list[str] | None = None

    def __call__(self, conn: Any, metrics: bool = True, **kwargs: Any) -> Any:
        """
        Call the query with the given connection and arguments.

        Args:
            conn: psycopg2 connection to database.
            metrics: Whether to collect metrics for the query execution.
            **kwargs: Additional arguments to pass to the query.

        Returns:
            Any result from the query execution based on the callable.
        """
        if metrics:
            qtype = self.type.lower()
            ipaddr = pgaddr(conn)
            try:
                QUERY_COUNTER.labels(qtype, ipaddr).inc()
                with QUERY_LATENCY_HISTOGRAM.labels(qtype, ipaddr).time():
                    result = self.callable(conn, **kwargs)
                return result
            except psycopg2.DatabaseError as exc:
                QUERY_ERROR_COUNTER.labels(qtype, ipaddr).inc()
                raise exc
        else:
            return self.callable(conn, **kwargs)


@dataclass
class ReadQuery(Query):
    type: QueryType = QueryType.READ


@dataclass
class WriteQuery(Query):
    type: QueryType = QueryType.WRITE


@dataclass
class MixedQuery(Query):
    type: QueryType = QueryType.MIXED


class Queries:
    __root__: list[Query] = []

    def all(self) -> list[Query]:
        return self.__root__

    def filter(self, type: QueryType, tags: str | list[str] | None = None) -> list[Query]:
        if tags is not None and not isinstance(tags, list):
            tags = [tags]
        return [
            query
            for query in self.__root__
            if query.type == type and (tags is None or all(tag in query.tags for tag in tags))
        ]
