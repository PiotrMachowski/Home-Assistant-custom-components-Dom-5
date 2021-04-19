import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions
from homeassistant.core import HomeAssistant

from .const import *
from .connector import test_connection

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_URL): str,
    vol.Required(CONF_USERNAME): str,
    vol.Required(CONF_PASSWORD): str
})


async def validate_input(hass: HomeAssistant, data: dict):
    if len(data.get(CONF_URL)) < 3:
        raise InvalidUrl

    url = data.get(CONF_URL)
    username = data.get(CONF_USERNAME)
    password = data.get(CONF_PASSWORD)

    try:
        result = await hass.async_add_executor_job(test_connection, url, username, password)
        if not result:
            raise InvalidCredentials
    except:
        raise InvalidUrl


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)
                title = f"{user_input.get(CONF_USERNAME)} ({user_input.get(CONF_URL)})"
                return self.async_create_entry(title=title, data=user_input)
            except InvalidCredentials:
                errors[CONF_PASSWORD] = "invalid_auth"
            except InvalidUrl:
                errors[CONF_URL] = "cannot_connect"

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)


class InvalidCredentials(exceptions.HomeAssistantError):
    pass


class InvalidUrl(exceptions.HomeAssistantError):
    pass
