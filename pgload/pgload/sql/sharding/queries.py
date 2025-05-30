from pgload.sql.query import ReadQuery, WriteQuery
from pgload.sql.sharding.callables import (
    drop_database,
    get_random_product,
    get_random_purchase,
    get_random_store,
    init_database,
    insert_test_data,
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
