from enum import StrEnum

from pgload.sql.queries import (
    CREATE_CITUS_SHARDING_DATABASE,
    CREATE_NEW_STORE,
    CREATE_SMR_DATABASE,
    DROP_DATABASE,
    GET_PRODUCTS_WITH_HIGH_PURCHASE_AND_LOW_STOCK,
    GET_TOP_5_STORES_BY_TOTAL_PURCHASE_VALUE,
    INSERT_TEST_DATA_FOR_SHARDING,
    INSERT_TEST_DATA_FOR_SMR,
    REGISTER_PURCHASE_FOR_RANDOM_PRODUCT,
    UPDATE_RANDOM_PRODUCT_QUANTITY,
)
from pgload.sql.query import Queries, Query, QueryType
from pgload.sql.utils import pgconnection
from pgload.sql.worker import SQLWorker

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
]


class ClusterMode(StrEnum):
    SHARDING = "sharding"
    REPLICATION = "replication"


class SMRQueries(Queries):
    __root__: list[Query] = [
        DROP_DATABASE,
        CREATE_SMR_DATABASE,
        INSERT_TEST_DATA_FOR_SMR,
        GET_TOP_5_STORES_BY_TOTAL_PURCHASE_VALUE,
        GET_PRODUCTS_WITH_HIGH_PURCHASE_AND_LOW_STOCK,
        CREATE_NEW_STORE,
        UPDATE_RANDOM_PRODUCT_QUANTITY,
        REGISTER_PURCHASE_FOR_RANDOM_PRODUCT,
    ]


class ShardingQueries(Queries):
    __root__: list[Query] = [
        DROP_DATABASE,
        CREATE_CITUS_SHARDING_DATABASE,
        INSERT_TEST_DATA_FOR_SHARDING,
        GET_TOP_5_STORES_BY_TOTAL_PURCHASE_VALUE,
        GET_PRODUCTS_WITH_HIGH_PURCHASE_AND_LOW_STOCK,
        CREATE_NEW_STORE,
        UPDATE_RANDOM_PRODUCT_QUANTITY,
        REGISTER_PURCHASE_FOR_RANDOM_PRODUCT,
    ]


QUERIES_BASED_ON_CLUSTER_MODE = {
    ClusterMode.SHARDING: ShardingQueries(),
    ClusterMode.REPLICATION: SMRQueries(),
}
