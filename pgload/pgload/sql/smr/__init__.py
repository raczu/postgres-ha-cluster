from pgload.sql.query import Queries, Query
from pgload.sql.smr.queries import (
    CREATE_DATABASE,
    DROP_DATABASE,
    GET_PRODUCTS_WITH_HIGH_PURCHASES_AND_LOW_STOCK_RANDOMLY,
    GET_RANDOM_PRODUCT,
    GET_RANDOM_PURCHASE,
    GET_RANDOM_STORE,
    INSERT_TEST_DATA,
    REGISTER_PURCHASE_FOR_RANDOM_PRODUCT,
)

__all__ = ["SMRQueries"]


class SMRQueries(Queries):
    __root__: list[Query] = [
        DROP_DATABASE,
        CREATE_DATABASE,
        INSERT_TEST_DATA,
        GET_RANDOM_STORE,
        GET_RANDOM_PRODUCT,
        GET_RANDOM_PURCHASE,
        GET_PRODUCTS_WITH_HIGH_PURCHASES_AND_LOW_STOCK_RANDOMLY,
        REGISTER_PURCHASE_FOR_RANDOM_PRODUCT,
    ]
