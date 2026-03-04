"""Shared entity logic for Zonspaarpot 2.0."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import ZonspaarpotRuntimeData


class ZonspaarpotEntity(CoordinatorEntity):
    """Base entity for Zonspaarpot 2.0."""

    _attr_has_entity_name = True

    def __init__(self, runtime_data: ZonspaarpotRuntimeData) -> None:
        super().__init__(runtime_data.coordinator)
        self._runtime_data = runtime_data
        self._host = runtime_data.host
        self._attr_device_info = {
            "identifiers": {("zonspaarpot_2_0", self._host)},
            "name": "Zonspaarpot 2.0",
            "manufacturer": "Zonspaarpot",
            "model": runtime_data.coordinator.data.info.get("product_type", "Unknown"),
            "sw_version": runtime_data.coordinator.data.info.get("api_version"),
            "configuration_url": f"http://{self._host}",
        }
