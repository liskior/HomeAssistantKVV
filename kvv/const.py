"""Constants for the kvv integration."""

from datetime import datetime, timedelta

DOMAIN = "kvv"
SCAN_INTERVAL = timedelta(seconds=20)

REQUEST_URL = "https://projekte.kvv-efa.de/sl3-alone/XSLT_TRIP_REQUEST2"
REQUEST_PARAMS = {
              'outputFormat': 'JSON',
              'coordOutputFormat': 'WGS84[dd.ddddd]',
              'type_origin': 'stop',
              'type_destination': 'stop',
              'useRealtime': 1,
              'routeType': 'LEASTWALKING'
            }





