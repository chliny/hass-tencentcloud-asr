import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from typing import Any, Dict
import aiohttp
import logging
from tencentcloud_api import Modules

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def validate_path(path: str) -> None:

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(path) as response:
                _LOGGER.info(f'response.status {response.status}')
                if response.status != 200:
                    raise ValueError
                await response.text()
    except Exception as e:
        _LOGGER.error('validate_path', e)
        raise ValueError


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: Dict[str, str] = {}
        if user_input:
            return self.async_create_entry(title=DOMAIN, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("secretid"): str,
                    vol.Required("secretkey"): str,
                    vol.Optional("model", default="16k_zh"): vol.In(Modules.keys()),
                },
            ),
            errors=errors
        )
