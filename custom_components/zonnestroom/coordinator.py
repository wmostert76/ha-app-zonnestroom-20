"""Data update coordinator for Zonnestroom 2.0."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
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
            actual = await self.api.async_get_actual()
        except ZonnestroomApiError as err:
            raise UpdateFailed(str(err)) from err

        return ZonnestroomData(info=info, config=config, actual=actual)
