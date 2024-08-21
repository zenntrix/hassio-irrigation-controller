# custom_components/irrigation_control/__init__.py

DOMAIN = "irrigation_control"

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "switch")
    )
    return True

async def async_unload_entry(hass, entry):
    await hass.config_entries.async_forward_entry_unload(entry, "switch")
    return True

async def async_update_options(hass, entry):
    hass.config_entries.async_update_entry(entry, options=entry.options)
    return True

