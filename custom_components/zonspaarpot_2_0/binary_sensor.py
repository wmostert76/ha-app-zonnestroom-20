"""Binary sensor platform for Zonspaarpot 2.0."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ZonspaarpotRuntimeData
from .const import DOMAIN
from .entity import ZonspaarpotEntity


@dataclass(frozen=True, kw_only=True)
class ZonspaarpotBinarySensorDescription(BinarySensorEntityDescription):
    """Description for Zonspaarpot binary sensors."""

    top_key: str
    nested_key: str


BINARY_SENSORS: tuple[ZonspaarpotBinarySensorDescription, ...] = (
    ZonspaarpotBinarySensorDescription(
        key="cooling",
        name="Koeling actief",
        translation_key="cooling",
        top_key="actual",
        nested_key="cooling",
    ),
    ZonspaarpotBinarySensorDescription(
        key="homewizard_connected",
        name="HomeWizard verbonden",
        translation_key="homewizard_connected",
        entity_category=EntityCategory.DIAGNOSTIC,
        top_key="homewizard_pib",
        nested_key="connected",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Zonspaarpot binary sensors."""
    runtime_data: ZonspaarpotRuntimeData = entry.runtime_data
    async_add_entities([ZonspaarpotBinarySensor(runtime_data, description) for description in BINARY_SENSORS])


class ZonspaarpotBinarySensor(ZonspaarpotEntity, BinarySensorEntity):
    """Zonspaarpot binary sensor."""

    entity_description: ZonspaarpotBinarySensorDescription

    def __init__(self, runtime_data: ZonspaarpotRuntimeData, description: ZonspaarpotBinarySensorDescription) -> None:
        super().__init__(runtime_data)
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{self._host}_{description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if binary sensor is on."""
        if self.entity_description.top_key == "actual":
            data = self.coordinator.data.actual.get("actual", {})
        else:
            data = self.coordinator.data.actual.get("homewizard_pib", {})
        return bool(data.get(self.entity_description.nested_key))
