"""Button platform for Zonnestroom 2.0."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ZonnestroomRuntimeData
from .const import DOMAIN
from .entity import ZonnestroomEntity


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Zonnestroom buttons."""
    runtime_data: ZonnestroomRuntimeData = entry.runtime_data
    async_add_entities([ZonnestroomRefreshButton(runtime_data)])


class ZonnestroomRefreshButton(ZonnestroomEntity, ButtonEntity):
    """Button that requests an immediate coordinator refresh."""

    _attr_name = "Ververs"
    _attr_translation_key = "force_refresh"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, runtime_data: ZonnestroomRuntimeData) -> None:
        super().__init__(runtime_data)
        self._attr_unique_id = f"{DOMAIN}_{runtime_data.entry_id}_force_refresh"

    async def async_press(self) -> None:
        """Refresh data immediately."""
        await self.coordinator.async_request_refresh()
