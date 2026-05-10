"""Shared entity logic for Zonnestroom 2.0."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import ZonnestroomRuntimeData
from .const import DOMAIN, NAME


class ZonnestroomEntity(CoordinatorEntity):
    """Base entity for Zonnestroom 2.0."""

    _attr_has_entity_name = True

    def __init__(self, runtime_data: ZonnestroomRuntimeData) -> None:
        super().__init__(runtime_data.coordinator)
        self._runtime_data = runtime_data
        self._entry_id = runtime_data.entry_id

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": NAME,
            "manufacturer": "Zonnestroom",
            "model": self.coordinator.data.info.get("product_type", "Unknown"),
            "sw_version": self.coordinator.data.info.get("api_version"),
            "configuration_url": f"http://{self._runtime_data.host}",
        }
