"""Operational labels for takeover justification."""

from __future__ import annotations

from enum import Enum

from e2e_carla_paper.types import RunOutcome


class InterventionLabel(str, Enum):
    NECESSARY_EFFECTIVE = "NECESSARY_EFFECTIVE"
    UNNECESSARY = "UNNECESSARY"
    INEFFECTIVE = "INEFFECTIVE"
    HARMFUL = "HARMFUL"


def classify_intervention(
    e2e_continue: RunOutcome,
    forced_fallback: RunOutcome,
) -> InterventionLabel:
    """Classify a paired event from binary branch safety outcomes.

    This truth table is intentionally minimal. The paper must separately freeze
    the exact definition of `safe` using collision, lane departure and TTLC.
    """

    if not e2e_continue.safe and forced_fallback.safe:
        return InterventionLabel.NECESSARY_EFFECTIVE
    if e2e_continue.safe and forced_fallback.safe:
        return InterventionLabel.UNNECESSARY
    if not e2e_continue.safe and not forced_fallback.safe:
        return InterventionLabel.INEFFECTIVE
    return InterventionLabel.HARMFUL

