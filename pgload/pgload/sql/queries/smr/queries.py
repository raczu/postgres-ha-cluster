from pgload.sql.queries.smr.callables import (
    get_products_with_high_purchases_and_low_stock_randomly,
    get_random_store_purchases,
    get_random_store_total_sales,
    init_database,
    insert_test_data,
    register_purchase_for_random_product,
    update_random_product_quantity,
)
from pgload.sql.query import ReadQuery, WriteQuery

CREATE_DATABASE = WriteQuery(callable=init_database, tags=["database", "init"])

INSERT_TEST_DATA = WriteQuery(callable=insert_test_data, tags=["fulfill", "testdata"])

GET_PRODUCTS_WITH_HIGH_PURCHASES_AND_LOW_STOCK_RANDOMLY = ReadQuery(
    callable=get_products_with_high_purchases_and_low_stock_randomly,
    tags=["benchmark"],
)

REGISTER_PURCHASE_FOR_RANDOM_PRODUCT = WriteQuery(
    callable=register_purchase_for_random_product,
    tags=["benchmark"],
)

UPDATE_RANDOM_PRODUCT_QUANTITY = WriteQuery(
    callable=update_random_product_quantity,
    tags=["benchmark", "update"],
)

GET_RANDOM_STORE_PURCHASES = ReadQuery(
    callable=get_random_store_purchases,
    tags=["benchmark"],
)

GET_RANDOM_STORE_TOTAL_SALES = ReadQuery(
    callable=get_random_store_total_sales,
    tags=["benchmark"],
)
