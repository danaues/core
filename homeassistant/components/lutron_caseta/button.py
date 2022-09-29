"""Support for Lutron keypad buttons."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import LutronCasetaDevice
from .const import DOMAIN as CASETA_DOMAIN
from .models import LutronCasetaData


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Lutron keypad buttons."""
    data: LutronCasetaData = hass.data[CASETA_DOMAIN][config_entry.entry_id]
    bridge = data.bridge
    bridge_device = data.bridge_device
    button_devices = bridge.get_buttons()
    non_caseta_button_devices: dict[str, dict] = {}

    for button_device_id in button_devices:
        if "device_name" in button_devices[button_device_id]:
            non_caseta_button_devices.setdefault(
                str(button_device_id),
                button_devices[button_device_id],
            )

    async_add_entities(
        LutronCasetaButton(button_devices[button_device_id], bridge, bridge_device)
        for button_device_id in non_caseta_button_devices
    )


class LutronCasetaButton(LutronCasetaDevice, ButtonEntity):
    """Representation of a Lutron keypad button."""

    async def async_press(self) -> None:
        """Send a button press event."""
        await self._smartbridge.tap_button(self.device_id)

    @property
    def serial(self):
        """Buttons shouldn't have serial numbers, Return None."""
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {"device_id": self.device_id}
