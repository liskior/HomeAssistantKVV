"""Constants for the kvv integration."""

from datetime import timedelta

DOMAIN = "kvv"
SCAN_INTERVAL = timedelta(seconds=20)

REQUEST_URL = "https://projekte.kvv-efa.de/sl3-alone/XSLT_DM_REQUEST"
REQUEST_PARAMS = {'outputFormat': 'JSON',
              'coordOutputFormat': 'WGS84[dd.ddddd]',
              'depType': 'stopEvents',
              'locationServerActive': 1,
              'mode': 'direct',
              'type_dm': 'stop',
              'useOnlyStops': 1,
              'useRealtime': 1}




