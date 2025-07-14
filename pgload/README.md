# pgload

`pgload` is a custom benchmarking tool designed to evaluate the performance of PostgreSQL high availability (HA) setups.
It simulates database workloads, collects metrics about query performance and expose them to via an HTTP endpoint,
making them available for scraping by Prometheus.

## Usage

`pgload` is intended to be run as a Docker container within the same network as your PostgreSQL HA cluster.
However, it can also be run locally to benchmark independent PostgreSQL instances.

```bash
pgload health check [OPTIONS]

--dsn DSN
    (required) Comma or space-separated list of PostgreSQL connection strings to check health.
--display
    Display the health check results in a table (default: true)
```

```bash
pgload init database [OPTIONS]

--write-dsn DSN
    (required) PostgreSQL connection string for write operations.
--mode MODE
    Cluster mode: 'replication' or 'sharding' (default: replication).
--force
    Drop and recreate the database (default: false).
--with-test-data
    Populate with test data (default: false).
--scale N
    Scale factor for test data (default: 1).
--seed N
    Seed for test data generator (default: random).
```

```bash
pgload benchmark run [OPTIONS]

--mode MODE
    Cluster mode: 'replication' or 'sharding' (default: replication).
--write-dsn DSN
    Connection string for write operations.
--read-dsn DSN
    Connection string for read operations.
--clients N
    Number of concurrent clients (default: 10).
--write-clients N
    Number of concurrent clients for write operations (rest will be read, default: 0).
--duration N
    Duration of the benchmark in seconds (default: infinite).
--metrics-port N
    Port for Prometheus metrics server (default: 8080).
```