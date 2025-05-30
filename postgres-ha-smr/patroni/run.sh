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
    CONN_STR="dbname=postgres user=${POSTGRESQL_USERNAME} password=${POSTGRESQL_PASSWORD} host=localhost port=5432"
    until psql "\$CONN_STR" -c "CREATE DATABASE ${POSTGRESQL_DATABASE};"; do
      echo "Waiting for database creation..."
      sleep 1
    done
    echo "Database ${POSTGRESQL_DATABASE} created successfully."
  fi
EOF

chmod +x /opt/patroni/init-db.sh
/opt/patroni/init-db.sh &
patroni /opt/patroni/patroni.yml
