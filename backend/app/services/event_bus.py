from __future__ import annotations

import heapq
import itertools
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from threading import Lock
from typing import Any

EVENT_WORKLOAD_UPDATE = "workload_update"
EVENT_METRIC_UPDATE = "metric_update"
EVENT_SCALING_DECISION = "scaling_decision"

_VALID_EVENTS = {EVENT_WORKLOAD_UPDATE, EVENT_METRIC_UPDATE, EVENT_SCALING_DECISION}

@dataclass(order=True)
class _HeapItem:
    timestamp: float
    seq: int
    event: dict = field(compare=False)

class EventBus:
    def __init__(self, history_limit: int = 500):
        self._heap: list[_HeapItem] = []
        self._seq = itertools.count()
        self._lock = Lock()
        self._history_limit = history_limit
        self._history: dict[int, deque] = defaultdict(
            lambda: deque(maxlen=self._history_limit)
        )

    def publish(
        self,
        event_type: str,
        org_id: int,
        payload: dict[str, Any] | None = None,
        *,
        timestamp: float | None = None,
    ) -> None:
         if event_type not in _VALID_EVENTS:
           raise ValueError(f"Unknown event_type: {event_type!r}")
        ts = timestamp if timestamp is not None else time.time()
        event = {
            "type": event_type,
            "org_id": org_id,
            "timestamp": ts,
            "payload": payload or {},
        }
        item = _HeapItem(timestamp=ts, seq=next(self._seq), event=event)
        with self._lock:
            heapq.heappush(self._heap, item)
            self._history[org_id].append(event)

    def drain_due(self, until_timestamp: float | None = None) -> list[dict]:
       cutoff = until_timestamp if until_timestamp is not None else time.time()
        drained: list[dict] = []
        with self._lock:
            while self._heap and self._heap[0].timestamp <= cutoff:
                drained.append(heapq.heappop(self._heap).event)
        return drained

    def recent(self, org_id: int, limit: int = 50) -> list[dict]:
        with self._lock:
            items = list(self._history.get(org_id, ()))
        return items[-limit:]
    def reset(self) -> None:
        with self._lock:
            self._heap.clear()
            self._history.clear()

event_bus = EventBus()
