"""Config flow for Zonnestroom 2.0."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ZonnestroomApiClient, ZonnestroomApiConnectionError, ZonnestroomApiError
from .const import CONF_HOST, CONF_SCAN_INTERVAL, DEFAULT_HOST, DEFAULT_SCAN_INTERVAL, DOMAIN, NAME


def _schema(host: str, scan_interval: int) -> vol.Schema:
    """Return the host and scan interval schema."""
    return vol.Schema(
        {
            vol.Required(CONF_HOST, default=host): str,
            vol.Required(CONF_SCAN_INTERVAL, default=scan_interval): vol.All(
                vol.Coerce(int), vol.Range(min=2, max=300)
            ),
        }
    )


class ZonnestroomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zonnestroom 2.0."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            data, errors = await self._validate_user_input(user_input)
            if not errors:
                host = data[CONF_HOST]
                unique_id = f"{DOMAIN}_{host}"
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=NAME, data=data)

        return self.async_show_form(
            step_id="user",
            data_schema=_schema(DEFAULT_HOST, DEFAULT_SCAN_INTERVAL),
            errors=errors,
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        """Reconfigure an existing entry."""
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}
        current_scan_interval = int(
            entry.options.get(
                CONF_SCAN_INTERVAL,
                entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            )
        )

        if user_input is not None:
            data, errors = await self._validate_user_input(user_input)
            if not errors:
                return self.async_update_reload_and_abort(
                    entry,
                    data_updates=data,
                    options_updates={CONF_SCAN_INTERVAL: data[CONF_SCAN_INTERVAL]},
                    title=NAME,
                    reason="reconfigure_successful",
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_schema(entry.data.get(CONF_HOST, DEFAULT_HOST), current_scan_interval),
            errors=errors,
        )

    async def _validate_user_input(
        self,
        user_input: dict[str, Any],
    ) -> tuple[dict[str, Any], dict[str, str]]:
        """Validate user input and return normalized data."""
        errors: dict[str, str] = {}
        host = user_input[CONF_HOST].strip()
        scan_interval = int(user_input[CONF_SCAN_INTERVAL])

        session = async_get_clientsession(self.hass)
        api = ZonnestroomApiClient(session, host)
        try:
            await api.async_get_info()
        except ZonnestroomApiConnectionError:
            errors["base"] = "cannot_connect"
        except ZonnestroomApiError:
            errors["base"] = "invalid_api"
        except Exception:  # noqa: BLE001
            errors["base"] = "unknown"

        return {CONF_HOST: host, CONF_SCAN_INTERVAL: scan_interval}, errors

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get options flow."""
        return ZonnestroomOptionsFlow(config_entry)


class ZonnestroomOptionsFlow(config_entries.OptionsFlow):
    """Handle Zonnestroom options."""

    def __init__(self, config_entry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = int(
            self._config_entry.options.get(
                CONF_SCAN_INTERVAL,
                self._config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            )
        )
        schema = vol.Schema(
            {
                vol.Required(CONF_SCAN_INTERVAL, default=current): vol.All(
                    vol.Coerce(int), vol.Range(min=2, max=300)
                ),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
