"""Deterministic FIFO action delay applied after E2E inference."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class TimedAction(Generic[T]):
    generated_at_s: float
    action: T


class ActionDelayBuffer(Generic[T]):
    def __init__(self, delay_ms: float) -> None:
        if delay_ms < 0:
            raise ValueError("delay_ms must be non-negative")
        self.delay_s = delay_ms / 1000.0
        self._queue: deque[TimedAction[T]] = deque()

    def reset(self) -> None:
        self._queue.clear()

    def push(self, action: T, generated_at_s: float) -> None:
        self._queue.append(TimedAction(generated_at_s, action))

    def pop_ready(self, now_s: float) -> TimedAction[T] | None:
        """Return the newest action whose configured delay has elapsed."""

        ready: TimedAction[T] | None = None
        while self._queue and now_s - self._queue[0].generated_at_s >= self.delay_s:
            ready = self._queue.popleft()
        return ready

