import logging
import voluptuous as vol
from typing import Any, Dict
from homeassistant.core import callback
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow, ConfigEntry

from .tencentcloud_api import Modules, DefaultModel
from .tencentcloud_api import TencentCloudAsrAPi
from . import SecretIdKey, SecretKeyKey, ModelKey
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: Dict[str, str] = {}
        if user_input:
            try:
                secretId = user_input.get(SecretIdKey)
                secretKey = user_input.get(SecretKeyKey)
                TencentCloudAsrAPi(secretId, secretKey)
            except Exception as err:
                errors["base"] = str(err)
                _LOGGER.error("check secret failed:%s", err)

            if not errors:
                return self.async_create_entry(title=DOMAIN, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(SecretIdKey): str,
                    vol.Required(SecretKeyKey): str,
                    vol.Required(ModelKey, default=DefaultModel): vol.In(Modules.keys()),
                },
            ),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        return TencentCloudAsrOptionFlow(config_entry)


class TencentCloudAsrOptionFlow(OptionsFlow):
    def __init__(self, config_entry: ConfigEntry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        if not user_input:
            user_input = {**self._config_entry.data, **self._config_entry.options}
        else:
            return self.async_create_entry(title=DOMAIN, data=user_input)
        model = user_input.get(ModelKey, DefaultModel)
        config_schema = vol.Schema({
            vol.Optional(ModelKey, default=model): vol.In(Modules.keys()),
        })
        return self.async_show_form(step_id="user", data_schema=config_schema, errors={})
