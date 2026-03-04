"""Data update coordinator for Zonspaarpot 2.0."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ZonspaarpotApiClient, ZonspaarpotApiError
from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)


@dataclass
class ZonspaarpotData:
    """Container for latest API payloads."""

    info: dict[str, Any]
    config: dict[str, Any]
    actual: dict[str, Any]


class ZonspaarpotDataUpdateCoordinator(DataUpdateCoordinator[ZonspaarpotData]):
    """Coordinator for polling Zonspaarpot API."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: ZonspaarpotApiClient,
        update_interval: timedelta,
    ) -> None:
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.api = api

    async def _async_update_data(self) -> ZonspaarpotData:
        """Fetch data from API."""
        try:
            info = await self.api.async_get_info()
            config = await self.api.async_get_config()
            actual = await self.api.async_get_actual()
        except ZonspaarpotApiError as err:
            raise UpdateFailed(str(err)) from err

        return ZonspaarpotData(info=info, config=config, actual=actual)
