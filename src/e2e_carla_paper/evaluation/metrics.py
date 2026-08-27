"""Metric containers for intervention and closed-loop driving performance."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InterventionMetrics:
    precision: float
    recall: float
    ineffective_rate: float
    harmful_rate: float
    e2e_control_authority: float

