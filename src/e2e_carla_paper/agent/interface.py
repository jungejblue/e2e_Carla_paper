"""Model-independent driving-agent interface."""

from __future__ import annotations

from typing import Any, Protocol

from e2e_carla_paper.types import AgentOutput


class DrivingAgent(Protocol):
    def reset(self, scenario_context: Any) -> None: ...

    def run_step(self, observation: Any, timestamp_s: float) -> AgentOutput: ...

