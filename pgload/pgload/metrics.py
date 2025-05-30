from prometheus_client import Counter, Gauge, Histogram

QUERY_ERROR_COUNTER = Counter(
    "pgload_query_error_total",
    "Total number of errors encountered during execution",
    ["type", "node"],
)

QUERY_COUNTER = Counter("pgload_query_total", "Total number of queries executed", ["type", "node"])

QUERY_LATENCY_HISTOGRAM = Histogram(
    "pgload_query_latency_seconds",
    "Latency of queries in seconds",
    ["type", "node"],
    buckets=[0.1, 0.25, 0.5, 1, 2, 5],
)
