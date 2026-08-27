"""CARLA client creation and synchronous-mode configuration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CarlaRuntimeConfig:
    host: str = "localhost"
    port: int = 2000
    timeout_seconds: float = 20.0
    fixed_delta_seconds: float = 0.05
    traffic_manager_port: int = 8000
    traffic_manager_seed: int = 2026


def connect(config: CarlaRuntimeConfig) -> tuple[Any, Any]:
    """Connect to CARLA and return `(client, world)`.

    CARLA is imported lazily because its Python API is supplied externally.
    """

    import carla  # type: ignore[import-not-found]

    client = carla.Client(config.host, config.port)
    client.set_timeout(config.timeout_seconds)
    return client, client.get_world()


def enable_synchronous_mode(client: Any, world: Any, config: CarlaRuntimeConfig) -> None:
    """Apply the deterministic runtime settings shared by all paired runs."""

    settings = world.get_settings()
    settings.synchronous_mode = True
    settings.fixed_delta_seconds = config.fixed_delta_seconds
    world.apply_settings(settings)

    traffic_manager = client.get_trafficmanager(config.traffic_manager_port)
    traffic_manager.set_synchronous_mode(True)
    traffic_manager.set_random_device_seed(config.traffic_manager_seed)

