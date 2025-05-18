from pgload.sql.callables import (
    drop_database,
    init_citus_sharding_database,
    init_smr_database,
    insert_test_data_for_sharding,
    insert_test_data_for_smr,
)
from pgload.sql.query import WriteQuery

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
