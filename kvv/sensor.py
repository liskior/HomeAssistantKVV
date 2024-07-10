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
                    vol.Required('name_origin', default='Karlsruhe, Hauptfriedhof'): str,
                    vol.Required('name_destination', default='Karlsruhe Karl-Wilhelm-Platz'): str,
                    vol.Required('nameInfo_origin', default='7000402'): str,
                    vol.Required('nameInfo_destination', default='7000401'): str
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


def fetch_departures(name_origin, name_destination, nameInfo_origin, nameInfo_destination):
    REQUEST_PARAMS['name_origin'] = name_origin
    REQUEST_PARAMS['name_destination'] = name_destination
    REQUEST_PARAMS['nameInfo_origin'] = nameInfo_origin
    REQUEST_PARAMS['nameInfo_destination'] = nameInfo_destination
    r = requests.get(url=REQUEST_URL, params=REQUEST_PARAMS)
    # _LOGGER.error(r)
    data = r.json()
    trips = data['trips']
    print(trips)
    departures = []
    for trip in trips:
        d = {}
        d['number'] = trip['legs'][0]['mode']['number']
        if (not d['number']):
            continue
        try:
            d['dateTime'] = trip['legs'][0]['stopSeq'][0]['ref']['depDateTime']
            print(d['dateTime'])
            # d['realDateTime'] = {trip['realDateTime']['hour'], trip['realDateTime']['minute']}
            d['delay'] = trip['legs'][0]['stopSeq'][0]['ref']['depDelay']
        except:
            print(trip)
        d['destination'] = trip['legs'][0]['mode']['destination']
        departures.append(d)
        if len(departures) == 10:
            break
    return departures


class KvvSensor(SensorEntity):
    departures = []

    def __init__(self, hass: HomeAssistant, info) -> None:
        print(info)
        self.hass: HomeAssistant = hass
        self.sensor_name = "kvv_sensor"
        self.name_origin = info.get('name_origin')
        self.name_destination = info.get('name_destination')
        self.nameInfo_origin = info.get('nameInfo_origin')
        self.nameInfo_destination = info.get('nameInfo_destination')

    @property
    def name(self) -> str:
        return self.sensor_name

    @property
    def unique_id(self) -> str:
        return f"{self.sensor_name}_{self.name_origin}_{self.name_destination}"

    @property
    def state(self) -> str:
        return self.name_origin + f" - {self.name_destination}"

    @property
    def extra_state_attributes(self):
        return {
            "departures": [str(departure) for departure in self.departures or []]
        }

    def update(self):
        self.departures = fetch_departures(self.name_origin, self.name_destination, self.nameInfo_origin,
                                           self.nameInfo_destination)

