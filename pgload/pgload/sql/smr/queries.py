from pgload.sql.query import ReadQuery, WriteQuery
from pgload.sql.smr.callables import (
    drop_database,
    get_products_with_high_purchases_and_low_stock_randomly,
    get_random_product,
    get_random_purchase,
    get_random_store,
    init_database,
    insert_test_data,
    register_purchase_for_random_product,
)

DROP_DATABASE = WriteQuery(callable=drop_database, tags=["database", "drop"])
CREATE_DATABASE = WriteQuery(callable=init_database, tags=["database", "init"])
INSERT_TEST_DATA = WriteQuery(callable=insert_test_data, tags=["fulfill", "testdata"])
GET_RANDOM_STORE = ReadQuery(
    callable=get_random_store,
    tags=["benchmark"],
)
GET_RANDOM_PRODUCT = ReadQuery(
    callable=get_random_product,
    tags=["benchmark"],
)
GET_RANDOM_PURCHASE = ReadQuery(
    callable=get_random_purchase,
    tags=["benchmark"],
)
GET_PRODUCTS_WITH_HIGH_PURCHASES_AND_LOW_STOCK_RANDOMLY = ReadQuery(
    callable=get_products_with_high_purchases_and_low_stock_randomly,
    tags=["benchmark"],
)
REGISTER_PURCHASE_FOR_RANDOM_PRODUCT = WriteQuery(
    callable=register_purchase_for_random_product,
    tags=["benchmark"],
)
