from pgload.sql.queries.common.queries import (
    DROP_DATABASE,
    GET_RANDOM_STORE_PRODUCTS,
)
from pgload.sql.queries.sharding.queries import (
    CREATE_DATABASE,
    GET_RANDOM_STORE_PURCHASES,
    GET_RANDOM_STORE_TOTAL_SALES,
    INSERT_TEST_DATA,
)
from pgload.sql.query import Queries, Query

__all__ = ["ShardingQueries"]


class ShardingQueries(Queries):
    __root__: list[Query] = [
        DROP_DATABASE,
        CREATE_DATABASE,
        INSERT_TEST_DATA,
        GET_RANDOM_STORE_PRODUCTS,
        GET_RANDOM_STORE_PURCHASES,
        GET_RANDOM_STORE_TOTAL_SALES,
    ]
