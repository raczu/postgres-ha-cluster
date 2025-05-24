#!/bin/bash

PGLOAD_WRITE_DSN="${PGLOAD_WRITE_DSN:-PGLOAD_RED_DSN}"

until pgload health check --dsn "${PGLOAD_WRITE_DSN} ${PGLOAD_READ_DSN}" > /dev/null; do
  echo "Waiting for all nodes to be healthy..."
  sleep 1
done

pgload init benchmark \
  --mode "${PGLOAD_MODE:-"replication"}" \
  --write-dsn "${PGLOAD_WRITE_DSN}" \
  --force \
  --with-test-data \
  --scale "${PGLOAD_SCALE:-1}" \
  --seed "${PGLOAD_SEED:-RANDOM}" \

pgload benchmark run \
  --mode "${PGLOAD_MODE:-"replication"}" \
  --write-dsn "${PGLOAD_WRITE_DSN:-PGLOAD_READ_DSN}" \
  --read-dsn "${PGLOAD_READ_DSN}" \
  --clients "${PGLOAD_CLIENTS:-10}" \
  --write-clients "${PGLOAD_WRITE_CLIENTS:-0}" \
