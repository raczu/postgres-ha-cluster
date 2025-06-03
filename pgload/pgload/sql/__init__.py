from enum import StrEnum

from pgload.sql.queries.sharding import ShardingQueries
from pgload.sql.queries.smr import SMRQueries
from pgload.sql.query import Queries, Query, QueryType
from pgload.sql.utils import pgconnection
from pgload.sql.worker import SQLWorker, SQLWorkerManager

__all__ = [
    "pgconnection",
    "Query",
    "Queries",
    "QueryType",
    "ClusterMode",
    "SMRQueries",
    "ShardingQueries",
    "QUERIES_BASED_ON_CLUSTER_MODE",
    "SQLWorker",
    "SQLWorkerManager",
]


class ClusterMode(StrEnum):
    SHARDING = "sharding"
    REPLICATION = "replication"


QUERIES_BASED_ON_CLUSTER_MODE = {
    ClusterMode.SHARDING: ShardingQueries(),
    ClusterMode.REPLICATION: SMRQueries(),
}
