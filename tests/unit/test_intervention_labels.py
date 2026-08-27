from e2e_carla_paper.evaluation.intervention_labels import (
    InterventionLabel,
    classify_intervention,
)
from e2e_carla_paper.types import RunOutcome


def outcome(safe: bool) -> RunOutcome:
    return RunOutcome(safe=safe, route_completed=safe)


def test_necessary_effective() -> None:
    assert classify_intervention(outcome(False), outcome(True)) is (
        InterventionLabel.NECESSARY_EFFECTIVE
    )


def test_unnecessary() -> None:
    assert classify_intervention(outcome(True), outcome(True)) is InterventionLabel.UNNECESSARY


def test_ineffective() -> None:
    assert classify_intervention(outcome(False), outcome(False)) is InterventionLabel.INEFFECTIVE


def test_harmful() -> None:
    assert classify_intervention(outcome(True), outcome(False)) is InterventionLabel.HARMFUL

