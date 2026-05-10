"""Number platform for Zonnestroom 2.0."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.const import EntityCategory, UnitOfPower, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ZonnestroomRuntimeData
from .const import DOMAIN
from .entity import ZonnestroomEntity


@dataclass(frozen=True, kw_only=True)
class ZonnestroomLoadNumberDescription(NumberEntityDescription):
    """Description for editable load configuration values."""

    load_key: str
    payload_key: str
    fallback: int


LOAD_NUMBERS: tuple[ZonnestroomLoadNumberDescription, ...] = (
    ZonnestroomLoadNumberDescription(
        key="setload",
        name="Setload (watt)",
        translation_key="setload",
        load_key="maxwatt",
        payload_key="watt",
        fallback=0,
        native_min_value=0,
        native_max_value=2300,
        native_step=1,
        native_unit_of_measurement=UnitOfPower.WATT,
        mode="box",
    ),
    ZonnestroomLoadNumberDescription(
        key="wait_after_update",
        name="Wacht na update",
        translation_key="wait_after_update",
        load_key="waitafterupdate",
        payload_key="wait_after_update",
        fallback=1,
        native_min_value=0,
        native_max_value=300,
        native_step=1,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.CONFIG,
        mode="box",
    ),
    ZonnestroomLoadNumberDescription(
        key="awake",
        name="Awake",
        translation_key="awake",
        load_key="awake",
        payload_key="awake",
        fallback=30,
        native_min_value=0,
        native_max_value=3600,
        native_step=1,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.CONFIG,
        mode="box",
    ),
    ZonnestroomLoadNumberDescription(
        key="sleep",
        name="Sleep",
        translation_key="sleep",
        load_key="sleep",
        payload_key="sleep",
        fallback=0,
        native_min_value=0,
        native_max_value=3600,
        native_step=1,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.CONFIG,
        mode="box",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up load configuration numbers."""
    runtime_data: ZonnestroomRuntimeData = entry.runtime_data
    async_add_entities([ZonnestroomLoadNumber(runtime_data, description) for description in LOAD_NUMBERS])


class ZonnestroomLoadNumber(ZonnestroomEntity, NumberEntity):
    """Number entity for load configuration."""

    entity_description: ZonnestroomLoadNumberDescription

    def __init__(
        self,
        runtime_data: ZonnestroomRuntimeData,
        description: ZonnestroomLoadNumberDescription,
    ) -> None:
        super().__init__(runtime_data)
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{runtime_data.entry_id}_{description.key}"

    @property
    def native_value(self) -> float | None:
        """Return configured load value."""
        value = self.coordinator.data.config.get("load", {}).get(self.entity_description.load_key)
        if value is None:
            return None
        return float(value)

    async def async_set_native_value(self, value: float) -> None:
        """Persist new load configuration."""
        config_load = self.coordinator.data.config.get("load", {})
        payload = {
            "watt": int(config_load.get("maxwatt", 0)),
            "wait_after_update": int(config_load.get("waitafterupdate", 1)),
            "awake": int(config_load.get("awake", 30)),
            "sleep": int(config_load.get("sleep", 0)),
        }
        payload[self.entity_description.payload_key] = int(round(value))

        await self._runtime_data.api.async_save_load_config(
            watt=payload["watt"],
            wait_after_update=payload["wait_after_update"],
            awake=payload["awake"],
            sleep=payload["sleep"],
        )
        await self.coordinator.async_request_refresh()
