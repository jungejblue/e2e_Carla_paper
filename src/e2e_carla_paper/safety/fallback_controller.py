"""Fixed reference lane-recovery controller."""

from __future__ import annotations

from typing import Any


class LaneRecoveryController:
    """Reference controller; it is not trained or tuned per test scenario."""

    def reset(self) -> None:
        pass

    def run_step(self, vehicle_state: Any, centerline: Any) -> Any:
        raise NotImplementedError("Implement after choosing the final tracking controller.")

