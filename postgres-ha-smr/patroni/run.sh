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

cat << EOF > /opt/patroni/init-db.sh
echo "Sleeping for 10 seconds to allow Patroni to start..."
sleep 10

until HTTP_CODE="\$(curl -s -o /dev/null -w "%{http_code}" 'http://${PG_PATRONI_RESTAPI_LISTEN}/primary')"; do
  echo "Waiting for Patroni REST API to be available..."
  sleep 1
done

if [ "\$HTTP_CODE" -eq 200 ]; then
    DEFAULT_CONN_STR="dbname=postgres user=${POSTGRESQL_USERNAME} password=${POSTGRESQL_PASSWORD} host=localhost port=5432"
    until psql "\$DEFAULT_CONN_STR" -c "SELECT 1;" >/dev/null 2>&1; do
      echo "Waiting for PostgreSQL to be ready..."
      sleep 1
    done

    CONN_STR="dbname=${POSTGRESQL_DATABASE} user=${POSTGRESQL_USERNAME} password=${POSTGRESQL_PASSWORD} host=localhost port=5432"
    if psql "\$CONN_STR" -c "SELECT 1;" >/dev/null 2>&1; then
      echo "Database ${POSTGRESQL_DATABASE} already exists."
      exit 0
    fi
    psql "\$DEFAULT_CONN_STR" -c "CREATE DATABASE ${POSTGRESQL_DATABASE};"
    echo "Database ${POSTGRESQL_DATABASE} created successfully."
  fi
EOF

chmod +x /opt/patroni/init-db.sh
/opt/patroni/init-db.sh &
patroni /opt/patroni/patroni.yml
