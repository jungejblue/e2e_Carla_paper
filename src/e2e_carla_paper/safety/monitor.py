"""Observable-risk monitor used to nominate takeover candidate events."""

from __future__ import annotations

from typing import Mapping

from e2e_carla_paper.types import MonitorOutput


class SafetyMonitor:
    def __init__(self, threshold: float) -> None:
        self.threshold = threshold

    def evaluate(self, signals: Mapping[str, float]) -> MonitorOutput:
        """Compute a risk score after the monitor definition is finalized."""

        raise NotImplementedError("Freeze signals and calibration procedure before implementation.")

