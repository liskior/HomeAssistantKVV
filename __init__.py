"""The kvv integration."""
from __future__ import annotations
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .const import SCAN_INTERVAL

def setup(hass: HomeAssistant, config: ConfigType):
    return True

