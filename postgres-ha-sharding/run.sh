#!/bin/bash

cat << EOF > /opt/patroni/patroni.yml
scope: postgres
name: ${PG_PATRONI_NAME}
restapi:
  listen: ${PG_PATRONI_RESTAPI_LISTEN}
  connect_address: ${PG_PATRONI_RESTAPI_CONNECT_ADDRESS}
etcd3:
  host: ${PG_PATRONI_ETCD3_HOST}
citus:
  group: ${PG_PATRONI_CITUS_GROUP}
  database: ${PG_PATRONI_CITUS_DATABASE}
bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      use_slots: true
      parameters: {max_connections: 256, shared_buffers: 256MB}
  initdb:
    - encoding: UTF8
    - data-checksums
  pg_hba:
    - host replication replicator 0.0.0.0/0 md5
    - host all all 0.0.0.0/0 md5
postgresql:
  listen: ${PG_PATRONI_POSTGRESQL_LISTEN}
  connect_address: ${PG_PATRONI_POSTGRESQL_CONNECT_ADDRESS}
  data_dir: /var/lib/postgresql/data/pgdata
  authentication:
    replication:
      username: replicator
      password: replicator
    superuser:
      username: ${POSTGRESQL_USERNAME}
      password: ${POSTGRESQL_PASSWORD}
EOF

patroni /opt/patroni/patroni.yml