import logging
from datetime import timedelta
from typing import Any, Callable, Dict, Optional

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import StateType

from .connector import Dom5Connector
from .const import *

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_URL): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})


def messages_state_extractor(connector: Dom5Connector) -> Optional[int]:
    return connector.data.messages_number


def messages_attributes_extractor(connector: Dom5Connector) -> dict:
    return {
        "titles": connector.data.last_messages_titles
    }


def last_message_state_extractor(connector: Dom5Connector) -> Optional[str]:
    return connector.data.last_message_title


def last_message_attributes_extractor(connector: Dom5Connector) -> dict:
    return {
        "title": connector.data.last_message_title,
        "body": connector.data.last_message_body,
        "date": connector.data.last_message_date,
        "id": connector.data.last_message_id
    }


def announcements_state_extractor(connector: Dom5Connector) -> Optional[int]:
    return connector.data.announcements_number


def announcements_attributes_extractor(connector: Dom5Connector) -> dict:
    return {
        "titles": connector.data.last_announcements_titles
    }


def last_announcement_state_extractor(connector: Dom5Connector) -> Optional[str]:
    return connector.data.last_announcement_title


def last_announcement_attributes_extractor(connector: Dom5Connector) -> dict:
    return {
        "title": connector.data.last_announcement_title,
        "body": connector.data.last_announcement_body,
        "date": connector.data.last_announcement_date,
        "id": connector.data.last_announcement_id
    }


def finances_state_extractor(connector: Dom5Connector) -> float:
    return connector.data.balance


def finances_attributes_extractor(connector: Dom5Connector) -> dict:
    return {
        "arrear": connector.data.arrear,
        "overpayment": connector.data.overpayment
    }


SENSOR_TYPES = {
    "messages": [" ", messages_state_extractor, messages_attributes_extractor],
    "last_message": [None, last_message_state_extractor, last_message_attributes_extractor],
    "announcements": [" ", announcements_state_extractor, announcements_attributes_extractor],
    "last_announcement": [None, last_announcement_state_extractor, last_announcement_attributes_extractor],
    "finances": ["zł", finances_state_extractor, finances_attributes_extractor]
}


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    name = config.get(CONF_NAME)
    url = config.get(CONF_URL)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    connector = Dom5Connector(url, username, password)
    if not hass.async_add_executor_job(connector.test_connection):
        raise Exception('Invalid configuration')
    await hass.async_add_executor_job(connector.update)
    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(Dom5Sensor(name, connector, sensor_type))
    async_add_entities(entities, True)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_devices: Callable):
    connector = hass.data[DOMAIN][config_entry.entry_id]
    devices = []
    await hass.async_add_executor_job(connector.update)
    for sensor_type in SENSOR_TYPES:
        devices.append(Dom5ConfigFlowSensor(DEFAULT_NAME, connector, sensor_type))
    async_add_devices(devices)


class Dom5Sensor(Entity):
    def __init__(self, name: str, connector: Dom5Connector, sensor_type: str):
        self._name = name
        self._connector = connector
        self._sensor_type = sensor_type

    @property
    def name(self):
        return f'{self._name} {self._sensor_type} - {self._connector.username}'

    @property
    def icon(self):
        return "mdi:home-city"

    @property
    def unit_of_measurement(self) -> Optional[str]:
        return SENSOR_TYPES[self._sensor_type][0]

    @property
    def state(self) -> StateType:
        return SENSOR_TYPES[self._sensor_type][1](self._connector)

    @property
    def extra_state_attributes(self) -> Optional[Dict[str, Any]]:
        return SENSOR_TYPES[self._sensor_type][2](self._connector)

    def update(self):
        self._connector.update()

    @property
    def unique_id(self):
        return f"{DOMAIN}-yaml-{self._name}-{self._connector.url}-{self._connector.username}-{self._sensor_type}"


class Dom5ConfigFlowSensor(Dom5Sensor):
    def __init__(self, name: str, connector: Dom5Connector, sensor_type: str):
        super().__init__(name, connector, sensor_type)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._connector.url, self._connector.username)},
            "name": f"{self._connector.url}: {self._connector.username}",
            "manufacturer": "Sacer",
            "via_device": None,
        }

    @property
    def unique_id(self):
        return f"{DOMAIN}-{self._connector.url}-{self._connector.username}-{self._sensor_type}"

