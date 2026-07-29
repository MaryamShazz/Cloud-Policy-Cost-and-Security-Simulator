from __future__ import annotations

import heapq
import itertools
import math
from collections import deque
from dataclasses import dataclass, field

import numpy as np

EV_REQUEST_ARRIVAL = "REQUEST_ARRIVAL"
EV_SERVICE_COMPLETE = "SERVICE_COMPLETE"
EV_CONTROL_EVAL = "CONTROL_EVAL"


@dataclass(order=True)
class SimEvent:
  sim_time: float
    seq: int
    event_type: str = field(compare=False)
    payload: dict = field(compare=False, default_factory=dict)


@dataclass
class VMQueueState:
  queue_ms: float = 0.0
    sim_time: float = 0.0
     cumulative_dropped: int = 0
    dropped_in_last_tick: int = 0
    latency_history: deque = field(default_factory=lambda: deque(maxlen=200))
   last_mean_service_time_ms: float = 5.0
    last_sample_service_time_ms: float = 5.0


class VMDESSimulator:
      MAX_QUEUE_MS = 5_000.0   

    def __init__(self, vm_instance_id: str) -> None:
        self.instance_id = vm_instance_id
        self.state = VMQueueState()
        self._heap: list[SimEvent] = []
        self._seq = itertools.count()
  def _push(
        self,
        sim_time: float,
        event_type: str,
        payload: dict | None = None,
    ) -> None:
        ev = SimEvent(
            sim_time=sim_time,
            seq=next(self._seq),
            event_type=event_type,
            payload=payload or {},
        )
        heapq.heappush(self._heap, ev)

    def step(
        self,
        dt_seconds: float,
        rps: float,
        mean_service_time_ms: float,
        sample_service_time_ms: float,
        vcpu: int,
    ) -> dict:
     
        t_start = self.state.sim_time
        t_end = t_start + dt_seconds

        processing_rate = float(vcpu) * (1_000.0 / max(0.1, mean_service_time_ms))
        drain_capacity_ms = processing_rate * dt_seconds
     incoming_work_ms = rps * dt_seconds * sample_service_time_ms

        self._push(t_start, EV_SERVICE_COMPLETE, {"drain_capacity_ms": drain_capacity_ms})
        self._push(t_start, EV_REQUEST_ARRIVAL, {"incoming_work_ms": incoming_work_ms})
        latency_ms = sample_service_time_ms 
        dropped_this_tick = 0
  while self._heap and self._heap[0].sim_time <= t_end:
            ev = heapq.heappop(self._heap)
            self.state.sim_time = ev.sim_time

            if ev.event_type == EV_SERVICE_COMPLETE:
                self.state.queue_ms = max(
                    0.0, self.state.queue_ms - ev.payload["drain_capacity_ms"]
                )

            elif ev.event_type == EV_REQUEST_ARRIVAL:
                queue_delay_ms = self.state.queue_ms / max(1.0, processing_rate)
                latency_ms = sample_service_time_ms + queue_delay_ms
     new_queue = self.state.queue_ms + ev.payload["incoming_work_ms"]
               if new_queue > self.MAX_QUEUE_MS:
                    overflow_ms = new_queue - self.MAX_QUEUE_MS
                    dropped_this_tick = int(
                        overflow_ms / max(0.1, sample_service_time_ms)
                    )
                    new_queue = self.MAX_QUEUE_MS

                self.state.queue_ms = new_queue

        self.state.sim_time = t_end

self.state.dropped_in_last_tick = dropped_this_tick
        self.state.cumulative_dropped += dropped_this_tick

       self.state.last_mean_service_time_ms = mean_service_time_ms
        self.state.last_sample_service_time_ms = sample_service_time_ms

        self.state.latency_history.append(latency_ms)
        if len(self.state.latency_history) >= 5:
            p95_latency_ms = float(np.percentile(list(self.state.latency_history), 95))
        else:
             p95_latency_ms = latency_ms * 1.5

       final_queue_delay_ms = self.state.queue_ms / max(1.0, processing_rate)

        return {
            "queue_ms": round(self.state.queue_ms, 2),
            "latency_ms": round(latency_ms, 2),
            "p95_latency_ms": round(p95_latency_ms, 2),
            "queue_delay_ms": round(final_queue_delay_ms, 2),
            "dropped": dropped_this_tick,
           "mean_service_time_ms": round(mean_service_time_ms, 3),
            "sample_service_time_ms": round(sample_service_time_ms, 3),
            "avg_service_time_ms": round(mean_service_time_ms, 3),  # legacy alias
            "processing_rate_ms_per_s": round(processing_rate, 2),
        }

    def reset(self) -> None:
        self.state = VMQueueState()
        self._heap.clear()
def compute_backlog_per_instance(
    queue_total_ms: float,
    avg_service_time_ms: float,
    num_instances: int,
) -> float:
  
    backlog_requests = queue_total_ms / max(0.1, avg_service_time_ms)
    return backlog_requests / max(1, num_instances)


def compute_target_bpi(latency_slo_ms: float, avg_service_time_ms: float) -> float:
   return latency_slo_ms / max(0.1, avg_service_time_ms)

def compute_desired_capacity(
    queue_total_ms: float,
    avg_service_time_ms: float,
    target_bpi: float,
) -> int:
  backlog_requests = queue_total_ms / max(0.1, avg_service_time_ms)
    return max(1, math.ceil(backlog_requests / max(0.001, target_bpi)))
