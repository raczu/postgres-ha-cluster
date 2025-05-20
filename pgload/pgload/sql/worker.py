import random
import threading
import time

import psycopg2
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    stop_when_event_set,
    wait_exponential,
)

from pgload.sql.utils import pgconnection
from pgload.sql.query import Query


class SQLWorker(threading.Thread):
    def __init__(
        self, dsn: str, queries: list[Query], stop_event: threading.Event
    ) -> None:
        super().__init__()
        self._dsn: str = dsn
        self._queries: list[Query] = queries
        self._stop_event: threading.Event = stop_event

    def run(self) -> None:
        r = Retrying(
            stop=stop_after_attempt(5) | stop_when_event_set(self._stop_event),
            wait=wait_exponential(multiplier=1, min=1, max=10),
            retry=retry_if_exception_type(psycopg2.OperationalError),
            reraise=True,
        )
        for attempt in r:
            with attempt:
                while not self._stop_event.is_set():
                    with pgconnection(self._dsn) as conn:
                        query = random.choice(self._queries)
                        _ = query(conn)
                        time.sleep(random.uniform(0.5, 2.0))
