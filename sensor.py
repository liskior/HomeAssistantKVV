from __future__ import annotations
import logging

import requests

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import PLATFORM_SCHEMA
import voluptuous as vol

from .const import DOMAIN
from .const import SCAN_INTERVAL
from .const import REQUEST_URL, REQUEST_PARAMS

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional('info'):
        [
            {
                vol.Required('stop_name', default='Durlacher Tor'): str,
                vol.Optional('direction_name', default=None): str
            }
        ]
    }
)


async def async_setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        add_entities: AddEntitiesCallback,
        _: DiscoveryInfoType | None = None,
) -> None:
    if 'info' in config:
        for departure in config['info']:
            add_entities([KvvSensor(hass, departure)])


def fetch_departures(stop_name, direction_name):
    REQUEST_PARAMS['name_dm'] = stop_name
    r = requests.get(url=REQUEST_URL, params=REQUEST_PARAMS)
    data = r.json()
    departureList = data['departureList']
    departures = []
    for departure in departureList:
        d = {}
        d['number'] = departure['servingLine']['number']
        d['product'] = departure['servingLine']['name']
        d['dateTime'] = str(departure['dateTime']['hour']) + ":" + str(departure['dateTime']['minute'])
        try:
            d['realDateTime'] = str(departure['realDateTime']['hour']) + ":" + str(departure['realDateTime']['minute'])
            d['delay'] = departure['servingLine']['delay']
        except:
            d['delay'] = 0
        d['direction'] = departure['servingLine']['direction']
        if not direction_name or d['direction'] == direction_name:
            departures.append(d)
        if len(departures) == 10:
            break
    return departures


class KvvSensor(SensorEntity):
    departures = []

    def __init__(self, hass: HomeAssistant, info) -> None:
        self.hass: HomeAssistant = hass
        self.sensor_name = "kvv_sensor"
        self.stop_name = info.get('stop_name')
        self.direction_name = None#info.get('direction_name') //TODO

    @property
    def name(self) -> str:
        return self.sensor_name

    @property
    def unique_id(self) -> str:
        return f"{self.sensor_name}_{self.stop_name}"

    @property
    def state(self) -> str:
        return self.stop_name

    @property
    def extra_state_attributes(self):
        return {
            "departures": [str(departure) for departure in self.departures or []]
        }

    def update(self):
        self.departures = fetch_departures(self.stop_name, self.direction_name)
