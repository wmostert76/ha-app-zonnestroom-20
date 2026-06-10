"""Data update coordinator for Zonnestroom 2.0."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import issue_registry as ir
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ZonnestroomApiClient, ZonnestroomApiError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclass
class ZonnestroomData:
    """Container for latest API payloads."""

    info: dict[str, Any]
    config: dict[str, Any]
    actual: dict[str, Any]


class ZonnestroomDataUpdateCoordinator(DataUpdateCoordinator[ZonnestroomData]):
    """Coordinator for polling Zonnestroom API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: ZonnestroomApiClient,
        update_interval: timedelta,
    ) -> None:
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.api = api

    async def _async_update_data(self) -> ZonnestroomData:
        """Fetch data from API."""
        try:
            info = await self.api.async_get_info()
            config = await self.api.async_get_config()
            config = await self._async_sync_homewizard_p1_ip(config)
            actual = await self.api.async_get_actual()
        except ZonnestroomApiError as err:
            ir.async_create_issue(
                self.hass,
                DOMAIN,
                "cannot_connect",
                is_fixable=False,
                severity=ir.IssueSeverity.ERROR,
                translation_key="cannot_connect",
                translation_placeholders={"host": self.api.host},
            )
            raise UpdateFailed(str(err)) from err

        ir.async_delete_issue(self.hass, DOMAIN, "cannot_connect")
        return ZonnestroomData(info=info, config=config, actual=actual)

    async def _async_sync_homewizard_p1_ip(self, config: dict[str, Any]) -> dict[str, Any]:
        """Keep the Zonnestroom P1 IP in sync with Home Assistant's HomeWizard P1 entry."""
        p1_ip = self._find_homewizard_p1_ip()
        if p1_ip is None:
            return config

        configured_ip = config.get("p1_meter", {}).get("ipaddress")
        if configured_ip == p1_ip:
            return config

        _LOGGER.info(
            "Updating Zonnestroom P1 IP from %s to HomeWizard P1 IP %s",
            configured_ip,
            p1_ip,
        )
        await self.api.async_save_p1_ip_config(p1_ip)
        return await self.api.async_get_config()

    def _find_homewizard_p1_ip(self) -> str | None:
        """Return the IP address from the HomeWizard P1 config entry if present."""
        for entry in self.hass.config_entries.async_entries("homewizard"):
            if not _is_homewizard_p1_entry(entry):
                continue

            ip_address = entry.data.get("ip_address")
            if isinstance(ip_address, str) and ip_address:
                return ip_address

        return None


def _is_homewizard_p1_entry(entry: ConfigEntry) -> bool:
    """Check whether a HomeWizard config entry is the P1 meter."""
    unique_id = str(entry.unique_id or "")
    return entry.title == "P1 Meter" or unique_id.startswith("HWE-P1_")
