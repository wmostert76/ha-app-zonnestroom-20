"""Sensor platform for Zonnestroom 2.0."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ZonnestroomRuntimeData
from .const import DOMAIN
from .entity import ZonnestroomEntity


@dataclass(frozen=True, kw_only=True)
class ZonnestroomSensorDescription(SensorEntityDescription):
    """Zonnestroom sensor description."""

    value_path: tuple[str, ...]


SENSORS: tuple[ZonnestroomSensorDescription, ...] = (
    ZonnestroomSensorDescription(
        key="home_consumption",
        name="Huisverbruik",
        translation_key="home_consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class="measurement",
        value_path=("actual", "actual", "home_consumption"),
    ),
    ZonnestroomSensorDescription(
        key="additional_consumption",
        name="Extra verbruik",
        translation_key="additional_consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class="measurement",
        value_path=("actual", "actual", "additional_consumption"),
    ),
    ZonnestroomSensorDescription(
        key="mode",
        name="Actieve modus",
        translation_key="mode",
        value_path=("actual", "actual", "mode"),
    ),
    ZonnestroomSensorDescription(
        key="homewizard_consumption",
        name="HomeWizard verbruik",
        translation_key="homewizard_consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class="measurement",
        value_path=("actual", "homewizard_pib", "consumption"),
    ),
    ZonnestroomSensorDescription(
        key="homewizard_charge_percentage",
        name="HomeWizard laadpercentage",
        translation_key="homewizard_charge_percentage",
        native_unit_of_measurement="%",
        device_class=SensorDeviceClass.BATTERY,
        state_class="measurement",
        value_path=("actual", "homewizard_pib", "charge_percentage"),
    ),
    ZonnestroomSensorDescription(
        key="p1_status",
        name="P1 status",
        translation_key="p1_status",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_path=("config", "p1_meter", "status"),
    ),
    ZonnestroomSensorDescription(
        key="p1_type",
        name="P1 type",
        translation_key="p1_type",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_path=("config", "p1_meter", "type"),
    ),
    ZonnestroomSensorDescription(
        key="p1_ipaddress",
        name="P1 IP-adres",
        translation_key="p1_ipaddress",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_path=("config", "p1_meter", "ipaddress"),
    ),
    ZonnestroomSensorDescription(
        key="api_version",
        name="API versie",
        translation_key="api_version",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_path=("info", "api_version"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Zonnestroom sensors."""
    runtime_data: ZonnestroomRuntimeData = entry.runtime_data
    async_add_entities([ZonnestroomSensor(runtime_data, description) for description in SENSORS])


class ZonnestroomSensor(ZonnestroomEntity, SensorEntity):
    """Representation of a Zonnestroom sensor."""

    entity_description: ZonnestroomSensorDescription

    def __init__(self, runtime_data: ZonnestroomRuntimeData, description: ZonnestroomSensorDescription) -> None:
        super().__init__(runtime_data)
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{self._host}_{description.key}"

    @property
    def native_value(self) -> Any:
        """Return sensor value."""
        data = self.coordinator.data
        value: Any = getattr(data, self.entity_description.value_path[0])
        for key in self.entity_description.value_path[1:]:
            if not isinstance(value, dict):
                return None
            value = value.get(key)
        return value
