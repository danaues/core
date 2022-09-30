"""Support for Lutron Caseta Occupancy/Vacancy Sensors."""
from pylutron_caseta import OCCUPANCY_GROUP_OCCUPIED

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN as CASETA_DOMAIN, LutronCasetaDevice
from .models import LutronCasetaData


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Lutron Caseta binary_sensor platform.

    Adds occupancy groups from the Caseta bridge associated with the
    config_entry as binary_sensor entities.
    """
    data: LutronCasetaData = hass.data[CASETA_DOMAIN][config_entry.entry_id]
    bridge = data.bridge
    bridge_device = data.bridge_device
    occupancy_groups = bridge.occupancy_groups
    async_add_entities(
        LutronOccupancySensor(occupancy_group, bridge, bridge_device)
        for occupancy_group in occupancy_groups.values()
    )


class LutronOccupancySensor(LutronCasetaDevice, BinarySensorEntity):
    """Representation of a Lutron occupancy group."""

    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY

    @property
    def is_on(self):
        """Return the brightness of the light."""
        return self._device["status"] == OCCUPANCY_GROUP_OCCUPIED

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        self._smartbridge.add_occupancy_subscriber(
            self.device_id, self.async_write_ha_state
        )

    @property
    def device_id(self):
        """Return the device ID used for calling pylutron_caseta."""
        return self._device["occupancy_group_id"]

    @property
    def unique_id(self):
        """Return a unique identifier."""
        return f"occupancygroup_{self._bridge_unique_id}_{self.device_id}"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {"device_id": self.device_id}
