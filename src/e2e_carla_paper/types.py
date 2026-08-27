"""Shared data contracts used at module boundaries."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class AgentOutput:
    """Output from the frozen E2E agent before arbitration."""

    control: Any
    predicted_trajectory: Any | None
    inference_time_ms: float
    action_age_ms: float
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MonitorOutput:
    """Safety-monitor decision and the observable evidence behind it."""

    trigger: bool
    risk_score: float
    signals: Mapping[str, float]
    reason: str = ""


@dataclass(frozen=True)
class RunOutcome:
    """Minimal outcome required to compare paired branches."""

    safe: bool
    route_completed: bool
    collision: bool = False
    lane_departure: bool = False
    minimum_ttlc_s: float | None = None

