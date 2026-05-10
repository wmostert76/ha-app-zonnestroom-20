"""The Zonnestroom 2.0 integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.typing import ConfigType

from .api import ZonnestroomApiClient
from .const import CONF_HOST, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN
from .coordinator import ZonnestroomDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SELECT,
    Platform.NUMBER,
    Platform.TEXT,
    Platform.BUTTON,
]


@dataclass
class ZonnestroomRuntimeData:
    """Runtime data for a config entry."""

    api: ZonnestroomApiClient
    coordinator: ZonnestroomDataUpdateCoordinator
    host: str
    entry_id: str


_UNIQUE_ID_MIGRATIONS: tuple[tuple[Platform, str, str], ...] = (
    (Platform.SENSOR, "home_consumption", "home_consumption"),
    (Platform.SENSOR, "additional_consumption", "additional_consumption"),
    (Platform.SENSOR, "mode", "mode"),
    (Platform.SENSOR, "homewizard_consumption", "homewizard_consumption"),
    (Platform.SENSOR, "homewizard_charge_percentage", "homewizard_charge_percentage"),
    (Platform.SENSOR, "p1_status", "p1_status"),
    (Platform.SENSOR, "p1_type", "p1_type"),
    (Platform.SENSOR, "p1_ipaddress", "p1_ipaddress"),
    (Platform.SENSOR, "api_version", "api_version"),
    (Platform.BINARY_SENSOR, "cooling", "cooling"),
    (Platform.BINARY_SENSOR, "homewizard_connected", "homewizard_connected"),
    (Platform.SELECT, "mode_select", "mode_select"),
    (Platform.NUMBER, "setload", "setload"),
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:  # noqa: ARG001
    """Set up the integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    """Set up Zonnestroom from a config entry."""
    host = entry.data[CONF_HOST]
    scan_interval = int(entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)))

    _migrate_unique_ids(hass, entry.entry_id, host)

    session = async_get_clientsession(hass)
    api = ZonnestroomApiClient(session=session, host=host)
    coordinator = ZonnestroomDataUpdateCoordinator(
        hass=hass,
        api=api,
        update_interval=timedelta(seconds=scan_interval),
    )
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = ZonnestroomRuntimeData(
        api=api,
        coordinator=coordinator,
        host=host,
        entry_id=entry.entry_id,
    )
    hass.data[DOMAIN][entry.entry_id] = entry.runtime_data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


def _migrate_unique_ids(hass: HomeAssistant, entry_id: str, host: str) -> None:
    """Migrate IP-based entity unique IDs to config-entry-based IDs."""
    entity_registry = er.async_get(hass)

    for platform, old_key, new_key in _UNIQUE_ID_MIGRATIONS:
        old_unique_id = f"{DOMAIN}_{host}_{old_key}"
        new_unique_id = f"{DOMAIN}_{entry_id}_{new_key}"

        if entity_registry.async_get_entity_id(platform.value, DOMAIN, new_unique_id):
            continue

        entity_id = entity_registry.async_get_entity_id(platform.value, DOMAIN, old_unique_id)
        if entity_id is None:
            continue

        try:
            entity_registry.async_update_entity(entity_id, new_unique_id=new_unique_id)
        except ValueError:
            _LOGGER.debug("Could not migrate unique ID for %s", entity_id, exc_info=True)


async def async_unload_entry(hass: HomeAssistant, entry) -> bool:
    """Unload config entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
