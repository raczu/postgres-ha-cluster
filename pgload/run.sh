#!/bin/bash
set -e

PGLOAD_WRITE_DSN="${PGLOAD_WRITE_DSN:-$PGLOAD_READ_DSN}"
PGLOAD_HEALTH_CHECK_TIMEOUT="${PGLOAD_HEALTH_CHECK_TIMEOUT:-120}"
echo "pgload env variables:"
env | grep PGLOAD

COUNTER=0
until pgload health check --dsn "${PGLOAD_NODES_DSN}" > /tmp/pgload-healthcheck; do
  if [ "$COUNTER" -gt "$PGLOAD_HEALTH_CHECK_TIMEOUT" ]; then
    echo "Health check timed out after ${PGLOAD_HEALTH_CHECK_TIMEOUT} seconds."
    cat /tmp/pgload-healthcheck
    exit 1
  fi
  echo "Waiting for all nodes to be healthy..."
  sleep 1
  COUNTER=$((COUNTER + 1))
done
cat /tmp/pgload-healthcheck

pgload init database \
  --mode "${PGLOAD_MODE:-"replication"}" \
  --write-dsn "${PGLOAD_WRITE_DSN}" \
  --force \
  --with-test-data \
  --scale "${PGLOAD_SCALE:-1}" \
  --seed "${PGLOAD_SEED:-$RANDOM}"

echo "Letting the database settle (sleeping for 10 seconds)..."
sleep 10

pgload benchmark run \
  --mode "${PGLOAD_MODE:-"replication"}" \
  --write-dsn "${PGLOAD_WRITE_DSN}" \
  --read-dsn "${PGLOAD_READ_DSN}" \
  --clients "${PGLOAD_CLIENTS:-10}" \
  --write-clients "${PGLOAD_WRITE_CLIENTS:-0}"
