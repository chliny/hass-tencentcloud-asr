import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from typing import Any, Dict
import logging
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
                    vol.Optional(ModelKey, default=DefaultModel): vol.In(Modules.keys()),
                },
            ),
            errors=errors
        )
