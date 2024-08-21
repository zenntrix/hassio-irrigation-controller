# custom_components/irrigation_control/switch.py

import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    name = config_entry.data["name"]
    irrigation_zone_switch_entity_id = config_entry.data["irrigation_zone_switch_entity_id"]
    irrigation_pump_switch_entity_id = config_entry.data["irrigation_pump_switch_entity_id"]
    water_consumption_entity_id = config_entry.data["water_consumption_entity_id"]
    volume_required = config_entry.data["volume_required"]

    async_add_entities([IrrigationControlSwitch(name, irrigation_zone_switch_entity_id, irrigation_pump_switch_entity_id, water_consumption_entity_id, volume_required)])

class IrrigationControlSwitch(SwitchEntity):
    def __init__(self, name, irrigation_zone_switch_entity_id, irrigation_pump_switch_entity_id, water_consumption_entity_id, volume_required):
        self._name = name
        self._irrigation_zone_switch_entity_id = irrigation_zone_switch_entity_id
        self._irrigation_pump_switch_entity_id = irrigation_pump_switch_entity_id
        self._water_consumption_entity_id = water_consumption_entity_id
        self._volume_required = volume_required
        self._state = False
        self._unique_id = f"irrigation_control_{irrigation_zone_switch_entity_id}"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._unique_id)},
            "name": self._name,
            "manufacturer": "Custom",
            "model": "Irrigation Control",
            "sw_version": "1.0",
        }

    async def async_turn_on(self, **kwargs):
        self._state = True
        await self.hass.services.async_call('switch', 'turn_on', {'entity_id': self._irrigation_zone_switch_entity_id})
        await self.hass.services.async_call('light', 'turn_on', {'entity_id': self._irrigation_pump_switch_entity_id})
        _LOGGER.info("Irrigation zone turned on")

    async def async_turn_off(self, **kwargs):
        self._state = False
        await self.hass.services.async_call('light', 'turn_off', {'entity_id': self._irrigation_pump_switch_entity_id})
        await self.hass.services.async_call('switch', 'turn_off', {'entity_id': self._irrigation_zone_switch_entity_id})
        _LOGGER.info("Irrigation zone turned off")

    async def async_update(self):
        water_consumption = float(self.hass.states.get(self._water_consumption_entity_id).state)
        if self._state and water_consumption >= self._volume_required:
            await self.async_turn_off()
