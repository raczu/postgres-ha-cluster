from pgload.sql.queries.common.callables import (
    drop_database,
    get_random_product,
    get_random_purchase,
    get_random_store,
    get_random_store_products,
)
from pgload.sql.query import ReadQuery, WriteQuery

DROP_DATABASE = WriteQuery(callable=drop_database, tags=["database", "drop"])

GET_RANDOM_PRODUCT = ReadQuery(
    callable=get_random_product,
    tags=["benchmark"],
)

GET_RANDOM_PURCHASE = ReadQuery(
    callable=get_random_purchase,
    tags=["benchmark"],
)

GET_RANDOM_STORE = ReadQuery(
    callable=get_random_store,
    tags=["benchmark"],
)

GET_RANDOM_STORE_PRODUCTS = ReadQuery(
    callable=get_random_store_products,
    tags=["benchmark"],
)
