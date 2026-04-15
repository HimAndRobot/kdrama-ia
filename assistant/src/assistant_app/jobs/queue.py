from __future__ import annotations

import queue
import threading
import time
from typing import Callable


class JobQueue:
    def __init__(self) -> None:
        self._queue: "queue.Queue[Callable[[], None]]" = queue.Queue()
        self._pending = 0
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def submit(self, fn: Callable[[], None]) -> None:
        with self._lock:
            self._pending += 1
        self._queue.put(fn)

    def wait_for_idle(self, timeout_s: float) -> bool:
        deadline = time.time() + max(0.0, timeout_s)
        while time.time() < deadline:
            with self._lock:
                if self._pending == 0:
                    return True
            time.sleep(0.02)
        with self._lock:
            return self._pending == 0

    def _worker(self) -> None:
        while True:
            fn = self._queue.get()
            try:
                fn()
            except Exception:
                pass
            finally:
                with self._lock:
                    self._pending = max(0, self._pending - 1)
                self._queue.task_done()
