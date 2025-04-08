#!/bin/bash
set -e

PGPASSWORD="$POSTGRESQL_PASSWORD" psql -v ON_ERROR_STOP=1 -U "$POSTGRESQL_USERNAME" -d ecommerce <<-EOSQL
  ALTER ROLE "$POSTGRESQL_USERNAME" SET search_path TO ecommerce, public;
EOSQL
