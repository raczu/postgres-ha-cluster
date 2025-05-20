#!/bin/bash

cat << EOF > /opt/patroni/patroni.yml
scope: postgres
name: ${PG_PATRONI_NAME}
restapi:
  listen: ${PG_PATRONI_RESTAPI_LISTEN}
  connect_address: ${PG_PATRONI_RESTAPI_CONNECT_ADDRESS}
etcd3:
  host: ${PG_PATRONI_ETCD3_HOST}
bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      use_slots: true
  initdb:
    - encoding: UTF8
    - data-checksums
  pg_hba:
    - host replication replicator 0.0.0.0/0 md5
    - host all all 0.0.0.0/0 md5
  post_init: /opt/patroni/init-db.sh
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

cat << EOF > /opt/patroni/init-db.sh
#!/bin/bash
set -e

psql -d "\$1" -c "CREATE DATABASE ${POSTGRESQL_DATABASE};"
EOF

chmod +x /opt/patroni/init-db.sh
patroni /opt/patroni/patroni.yml