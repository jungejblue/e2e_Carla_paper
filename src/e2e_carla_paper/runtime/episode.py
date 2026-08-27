"""Episode lifecycle and paired-run reset boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EpisodeSpec:
    scenario_id: str
    map_name: str
    route_id: str
    seed: int
    vehicle_blueprint: str = "vehicle.lincoln.mkz_2020"


class EpisodeRunner:
    """Own actors and reset the world between paired branches."""

    def __init__(self, client: Any, world: Any) -> None:
        self.client = client
        self.world = world
        self.actors: list[Any] = []

    def reset(self, spec: EpisodeSpec) -> None:
        """Reload the target world and recreate actors from `spec`."""

        raise NotImplementedError("Implement after the Town01 spawn/route smoke test.")

    def close(self) -> None:
        for actor in reversed(self.actors):
            actor.destroy()
        self.actors.clear()

