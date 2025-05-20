from prometheus_client import Counter, Histogram

QUERY_ERROR_COUNTER = Counter(
    "pgload_query_error_total",
    "Total number of errors encountered during execution",
    ["type"],
)

QUERY_COUNTER = Counter(
    "pgload_query_total", "Total number of queries executed", ["type"]
)

QUERY_DURATION = Histogram(
    "pgload_query_duration_seconds",
    "Duration of query execution in seconds",
    ["type"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 5],
)
