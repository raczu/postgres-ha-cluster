from pgload.sql.queries.common.queries import (
    DROP_DATABASE,
)
from pgload.sql.queries.smr.queries import (
    CREATE_DATABASE,
    GET_RANDOM_STORE_TOTAL_SALES,
    INSERT_TEST_DATA,
    REGISTER_PURCHASE_FOR_RANDOM_PRODUCT,
)
from pgload.sql.query import Queries, Query

__all__ = ["SMRQueries"]


class SMRQueries(Queries):
    __root__: list[Query] = [
        DROP_DATABASE,
        CREATE_DATABASE,
        INSERT_TEST_DATA,
        GET_RANDOM_STORE_TOTAL_SALES,
        REGISTER_PURCHASE_FOR_RANDOM_PRODUCT,
    ]
