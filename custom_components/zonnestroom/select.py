"""Select platform for Zonnestroom 2.0."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ZonnestroomRuntimeData
from .const import DOMAIN, MODE_OPTIONS
from .entity import ZonnestroomEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up mode select."""
    runtime_data: ZonnestroomRuntimeData = entry.runtime_data
    async_add_entities([ZonnestroomModeSelect(runtime_data)])


class ZonnestroomModeSelect(ZonnestroomEntity, SelectEntity):
    """Select entity for mode changes."""

    _attr_name = "Modus kiezen"
    _attr_options = MODE_OPTIONS
    _attr_translation_key = "mode_select"

    def __init__(self, runtime_data: ZonnestroomRuntimeData) -> None:
        super().__init__(runtime_data)
        self._attr_unique_id = f"{DOMAIN}_{self._host}_mode_select"

    @property
    def current_option(self) -> str | None:
        """Return the selected mode."""
        return self.coordinator.data.actual.get("actual", {}).get("mode")

    async def async_select_option(self, option: str) -> None:
        """Select a mode."""
        await self._runtime_data.api.async_set_mode(option)
        await self.coordinator.async_request_refresh()
