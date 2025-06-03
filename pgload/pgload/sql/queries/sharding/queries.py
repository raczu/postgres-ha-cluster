from pgload.sql.queries.sharding.callables import (
    get_random_store_purchases,
    get_random_store_total_sales,
    init_database,
    insert_test_data,
)
from pgload.sql.query import ReadQuery, WriteQuery

CREATE_DATABASE = WriteQuery(callable=init_database, tags=["database", "init"])

INSERT_TEST_DATA = WriteQuery(callable=insert_test_data, tags=["fulfill", "testdata"])

GET_RANDOM_STORE_PURCHASES = ReadQuery(callable=get_random_store_purchases, tags=["benchmark"])

GET_RANDOM_STORE_TOTAL_SALES = ReadQuery(callable=get_random_store_total_sales, tags=["benchmark"])
