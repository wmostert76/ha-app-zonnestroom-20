"""Binary sensor platform for Zonnestroom 2.0."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import ZonnestroomRuntimeData
from .const import DOMAIN
from .entity import ZonnestroomEntity


@dataclass(frozen=True, kw_only=True)
class ZonnestroomBinarySensorDescription(BinarySensorEntityDescription):
    """Description for Zonnestroom binary sensors."""

    top_key: str
    nested_key: str


BINARY_SENSORS: tuple[ZonnestroomBinarySensorDescription, ...] = (
    ZonnestroomBinarySensorDescription(
        key="cooling",
        name="Koeling actief",
        translation_key="cooling",
        top_key="actual",
        nested_key="cooling",
    ),
    ZonnestroomBinarySensorDescription(
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
    """Set up Zonnestroom binary sensors."""
    runtime_data: ZonnestroomRuntimeData = entry.runtime_data
    async_add_entities([ZonnestroomBinarySensor(runtime_data, description) for description in BINARY_SENSORS])


class ZonnestroomBinarySensor(ZonnestroomEntity, BinarySensorEntity):
    """Zonnestroom binary sensor."""

    entity_description: ZonnestroomBinarySensorDescription

    def __init__(self, runtime_data: ZonnestroomRuntimeData, description: ZonnestroomBinarySensorDescription) -> None:
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
