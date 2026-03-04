"""Sensor platform for Zonspaarpot 2.0."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ZonspaarpotRuntimeData
from .const import DOMAIN
from .entity import ZonspaarpotEntity


@dataclass(frozen=True, kw_only=True)
class ZonspaarpotSensorDescription(SensorEntityDescription):
    """Zonspaarpot sensor description."""

    value_path: tuple[str, ...]


SENSORS: tuple[ZonspaarpotSensorDescription, ...] = (
    ZonspaarpotSensorDescription(
        key="home_consumption",
        name="Huisverbruik",
        translation_key="home_consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class="measurement",
        value_path=("actual", "actual", "home_consumption"),
    ),
    ZonspaarpotSensorDescription(
        key="additional_consumption",
        name="Extra verbruik",
        translation_key="additional_consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class="measurement",
        value_path=("actual", "actual", "additional_consumption"),
    ),
    ZonspaarpotSensorDescription(
        key="mode",
        name="Actieve modus",
        translation_key="mode",
        value_path=("actual", "actual", "mode"),
    ),
    ZonspaarpotSensorDescription(
        key="homewizard_consumption",
        name="HomeWizard verbruik",
        translation_key="homewizard_consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class="measurement",
        value_path=("actual", "homewizard_pib", "consumption"),
    ),
    ZonspaarpotSensorDescription(
        key="homewizard_charge_percentage",
        name="HomeWizard laadpercentage",
        translation_key="homewizard_charge_percentage",
        native_unit_of_measurement="%",
        device_class=SensorDeviceClass.BATTERY,
        state_class="measurement",
        value_path=("actual", "homewizard_pib", "charge_percentage"),
    ),
    ZonspaarpotSensorDescription(
        key="p1_status",
        name="P1 status",
        translation_key="p1_status",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_path=("config", "p1_meter", "status"),
    ),
    ZonspaarpotSensorDescription(
        key="p1_type",
        name="P1 type",
        translation_key="p1_type",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_path=("config", "p1_meter", "type"),
    ),
    ZonspaarpotSensorDescription(
        key="p1_ipaddress",
        name="P1 IP-adres",
        translation_key="p1_ipaddress",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_path=("config", "p1_meter", "ipaddress"),
    ),
    ZonspaarpotSensorDescription(
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
    """Set up Zonspaarpot sensors."""
    runtime_data: ZonspaarpotRuntimeData = entry.runtime_data
    async_add_entities([ZonspaarpotSensor(runtime_data, description) for description in SENSORS])


class ZonspaarpotSensor(ZonspaarpotEntity, SensorEntity):
    """Representation of a Zonspaarpot sensor."""

    entity_description: ZonspaarpotSensorDescription

    def __init__(self, runtime_data: ZonspaarpotRuntimeData, description: ZonspaarpotSensorDescription) -> None:
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
