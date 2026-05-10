"""Diagnostics support for Zonnestroom 2.0."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import ZonnestroomRuntimeData
from .const import CONF_HOST, DOMAIN

TO_REDACT = {CONF_HOST}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,  # noqa: ARG001
    entry: ConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    runtime_data: ZonnestroomRuntimeData = entry.runtime_data
    coordinator = runtime_data.coordinator

    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "last_update_success": coordinator.last_update_success,
        "data": {
            "info": coordinator.data.info,
            "config": async_redact_data(coordinator.data.config, TO_REDACT),
            "actual": coordinator.data.actual,
        },
        "host_matches_runtime": entry.data.get(CONF_HOST) == runtime_data.host,
        "domain": DOMAIN,
    }
