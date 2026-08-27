"""Thin adapter around the external CARLA Garage TransFuser++ agent."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from e2e_carla_paper.types import AgentOutput


class TransFuserPPAdapter:
    def __init__(self, garage_root: Path, checkpoint: Path) -> None:
        self.garage_root = garage_root
        self.checkpoint = checkpoint
        self._agent: Any | None = None

    def reset(self, scenario_context: Any) -> None:
        if self._agent is None:
            raise RuntimeError("Connect the CARLA Garage sensor agent before running an episode.")

    def run_step(self, observation: Any, timestamp_s: float) -> AgentOutput:
        raise NotImplementedError(
            "Map the CARLA Garage sensor_agent output to AgentOutput without modifying weights."
        )

