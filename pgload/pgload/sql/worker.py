import itertools
import threading
import time

import psycopg2
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_delay,
    stop_when_event_set,
    wait_fixed,
)

from pgload.sql.query import Query
from pgload.sql.utils import pgconnection


class SQLWorker(threading.Thread):
    def __init__(self, dsn: str, queries: list[Query], stop_event: threading.Event) -> None:
        super().__init__()
        self._dsn: str = dsn
        self._queries: itertools.cycle[Query] = itertools.cycle(queries)
        self._stop_event: threading.Event = stop_event

    def run(self) -> None:
        while not self._stop_event.is_set():
            query = next(self._queries)
            r = Retrying(
                stop=stop_when_event_set(self._stop_event),
                wait=wait_fixed(0.2),
                retry=retry_if_exception_type(psycopg2.DatabaseError),
                reraise=True,
            )
            for attempt in r:
                with attempt:
                    with pgconnection(self._dsn) as conn:
                        _ = query(conn)
            time.sleep(0.2)


class SQLWorkerManager:
    def __init__(self, stop_event: threading.Event) -> None:
        self._stop_event: threading.Event = stop_event
        self._workers: list[SQLWorker] = []

    def add(self, dsn: str, queries: list[Query], num: int) -> None:
        self._workers.extend(
            SQLWorker(dsn=dsn, queries=queries, stop_event=self._stop_event) for _ in range(num)
        )

    def start(self) -> None:
        for worker in self._workers:
            worker.start()

    def stop(self) -> None:
        for worker in self._workers:
            worker.join()

    def all_alive(self) -> bool:
        return all(worker.is_alive() for worker in self._workers)
