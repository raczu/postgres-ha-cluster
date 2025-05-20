from pgload.sql.callables import (
    create_new_store,
    drop_database,
    get_products_with_high_purchase_and_low_stock,
    get_top_5_stores_by_total_purchase_value,
    init_citus_sharding_database,
    init_smr_database,
    insert_test_data_for_sharding,
    insert_test_data_for_smr,
    register_purchase_for_random_product,
    update_random_product_quantity,
)
from pgload.sql.query import MixedQuery, ReadQuery, WriteQuery

DROP_DATABASE = WriteQuery(callable=drop_database, tags=["database", "drop"])

CREATE_SMR_DATABASE = WriteQuery(callable=init_smr_database, tags=["database", "init"])

CREATE_CITUS_SHARDING_DATABASE = WriteQuery(
    callable=init_citus_sharding_database, tags=["database", "init"]
)

INSERT_TEST_DATA_FOR_SMR = WriteQuery(
    callable=insert_test_data_for_smr, tags=["fulfill", "testdata"]
)

INSERT_TEST_DATA_FOR_SHARDING = WriteQuery(
    callable=insert_test_data_for_sharding, tags=["fulfill", "testdata"]
)

GET_TOP_5_STORES_BY_TOTAL_PURCHASE_VALUE = ReadQuery(
    callable=get_top_5_stores_by_total_purchase_value,
    tags=["benchmark"],
)

GET_PRODUCTS_WITH_HIGH_PURCHASE_AND_LOW_STOCK = ReadQuery(
    callable=get_products_with_high_purchase_and_low_stock,
    tags=["benchmark"],
)

CREATE_NEW_STORE = WriteQuery(
    callable=create_new_store,
    tags=["benchmark"],
)

UPDATE_RANDOM_PRODUCT_QUANTITY = MixedQuery(
    callable=update_random_product_quantity,
    tags=["benchmark"],
)

REGISTER_PURCHASE_FOR_RANDOM_PRODUCT = MixedQuery(
    callable=register_purchase_for_random_product,
    tags=["benchmark"],
)
