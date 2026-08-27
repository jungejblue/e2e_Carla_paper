"""State machine that selects E2E or fallback control."""

from __future__ import annotations

from enum import Enum, auto
from typing import Any

from e2e_carla_paper.types import MonitorOutput


class ControlMode(Enum):
    E2E = auto()
    FALLBACK = auto()


class TakeoverManager:
    def __init__(self) -> None:
        self.mode = ControlMode.E2E

    def reset(self) -> None:
        self.mode = ControlMode.E2E

    def select_control(
        self,
        e2e_control: Any,
        fallback_control: Any,
        monitor: MonitorOutput,
        force_fallback: bool = False,
    ) -> Any:
        if force_fallback or monitor.trigger:
            self.mode = ControlMode.FALLBACK
        return fallback_control if self.mode is ControlMode.FALLBACK else e2e_control

