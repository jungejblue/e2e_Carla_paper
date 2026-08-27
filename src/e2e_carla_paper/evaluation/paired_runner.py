"""Orchestrate the e2e-continue and forced-fallback paired branches."""

from __future__ import annotations

from dataclasses import dataclass

from e2e_carla_paper.types import RunOutcome


@dataclass(frozen=True)
class PairedOutcome:
    candidate_event_id: str
    e2e_continue: RunOutcome
    forced_fallback: RunOutcome
    pre_intervention_consistent: bool


class PairedRunner:
    def run(self, candidate_event_id: str) -> PairedOutcome:
        raise NotImplementedError(
            "Implement deterministic reruns and pre-intervention consistency checks."
        )

