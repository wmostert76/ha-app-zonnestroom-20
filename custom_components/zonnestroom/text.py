"""Text platform for Zonnestroom 2.0."""

from __future__ import annotations

from ipaddress import ip_address

from homeassistant.components.text import TextEntity, TextMode
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ZonnestroomRuntimeData
from .api import ZonnestroomApiClient, ZonnestroomApiError
from .const import CONF_HOST, DOMAIN
from .entity import ZonnestroomEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up editable host text field."""
    runtime_data: ZonnestroomRuntimeData = entry.runtime_data
    async_add_entities([ZonnestroomHostText(hass, entry, runtime_data)])


class ZonnestroomHostText(ZonnestroomEntity, TextEntity):
    """Editable IP address for the Zonnestroom API host."""

    _attr_name = "IP-adres"
    _attr_mode = TextMode.TEXT
    _attr_native_max = 45
    _attr_pattern = r"^[0-9a-fA-F:.]+$"
    _attr_translation_key = "host"

    def __init__(self, hass: HomeAssistant, entry, runtime_data: ZonnestroomRuntimeData) -> None:
        super().__init__(runtime_data)
        self._hass = hass
        self._entry = entry
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_host"

    @property
    def native_value(self) -> str:
        """Return the active API host."""
        return self._runtime_data.host

    async def async_set_value(self, value: str) -> None:
        """Update the API host immediately and persist it in the config entry."""
        new_host = value.strip()
        try:
            ip_address(new_host)
        except ValueError as err:
            raise HomeAssistantError("Voer een geldig IP-adres in.") from err

        if new_host == self._runtime_data.host:
            return

        session = async_get_clientsession(self._hass)
        new_api = ZonnestroomApiClient(session=session, host=new_host)
        try:
            await new_api.async_get_info()
        except ZonnestroomApiError as err:
            raise HomeAssistantError(f"Kan geen verbinding maken met {new_host}.") from err

        self._runtime_data.host = new_host
        self._runtime_data.api = new_api
        self._runtime_data.coordinator.api = new_api

        data = dict(self._entry.data)
        data[CONF_HOST] = new_host
        self._hass.config_entries.async_update_entry(
            self._entry,
            data=data,
        )

        await self._runtime_data.coordinator.async_request_refresh()
        self.async_write_ha_state()
