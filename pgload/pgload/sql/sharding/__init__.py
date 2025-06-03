from pgload.sql.query import Queries, Query
from pgload.sql.sharding.queries import (
    CREATE_DATABASE,
    DROP_DATABASE,
    GET_RANDOM_PRODUCT,
    GET_RANDOM_PURCHASE,
    GET_RANDOM_STORE,
    INSERT_TEST_DATA,
)

__all__ = ["ShardingQueries"]


class ShardingQueries(Queries):
    __root__: list[Query] = [
        DROP_DATABASE,
        CREATE_DATABASE,
        INSERT_TEST_DATA,
        GET_RANDOM_STORE,
        GET_RANDOM_PRODUCT,
        GET_RANDOM_PURCHASE,
    ]
