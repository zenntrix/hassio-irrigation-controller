# custom_components/irrigation_control/config_flow.py

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import selector
from .const import DOMAIN

@callback
def configured_instances(hass):
    return [entry.data.get("name") for entry in hass.config_entries.async_entries(DOMAIN)]

class IrrigationControlConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name", description="Name of the irrigation zone"): str,
                vol.Required("irrigation_zone_switch_entity_id", description="Select the switch entity for the irrigation zone"): selector({
                    "entity": {"domain": "switch"}
                }),
                vol.Required("irrigation_pump_switch_entity_id", description="Select the switch which controls the irrigation pump"): selector({
                    "entity": {"domain": "light"}
                }),
                vol.Required("water_consumption_entity_id", description="Select the sensor entity for water consumption"): selector({
                    "entity": {"domain": "sensor"}
                }),
                vol.Required("volume_required", description="Volume of water required to turn off the irrigation (in liters)"): vol.Coerce(float),
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return IrrigationControlOptionsFlowHandler(config_entry)

class IrrigationControlOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("name", default=self.config_entry.data.get("name")): str,
                vol.Required("irrigation_zone_switch_entity_id", default=self.config_entry.data.get("irrigation_zone_switch_entity_id")): selector({
                    "entity": {"domain": "switch"}
                }),
                vol.Required("irrigation_pump_switch_entity_id",default=self.config_entry.data.get("irrigation_pump_switch_entity_id"), description="Select the switch which controls the irrigation pump"): selector({
                    "entity": {"domain": "light"}
                }),
                vol.Required("water_consumption_entity_id", default=self.config_entry.data.get("water_consumption_entity_id")): selector({
                    "entity": {"domain": "sensor"}
                }),
                vol.Required("volume_required", default=self.config_entry.data.get("volume_required")): vol.Coerce(float),
            })
        )

