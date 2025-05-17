import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .tencentcloud_api import DefaultModel

DOMAIN = "tencentcloud_asr"

PLATFORMS = (Platform.STT,)
_LOGGER = logging.getLogger(__name__)

# const key
SecretIdKey = "secretid"
SecretKeyKey = "secretkey"
ModelKey = "model"


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    if not config_entry.update_listeners:
        config_entry.add_update_listener(async_update_options)
    config_data = {**config_entry.data, **config_entry.options}
    model = config_data.get(ModelKey, DefaultModel)
    hass.data[ModelKey] = model
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True


async def async_update_options(hass: HomeAssistant, config_entry: ConfigEntry):
    config_data = {**config_entry.data, **config_entry.options}
    model = config_data.get(ModelKey, DefaultModel)
    _LOGGER.debug("update model:%s", model)
    hass.data[ModelKey] = model


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
