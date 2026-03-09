"""Constants for Zonnestroom 2.0."""

from datetime import timedelta

DOMAIN = "zonnestroom"
NAME = "Zonnestroom 2.0"

CONF_HOST = "host"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_HOST = "192.168.180.109"
DEFAULT_SCAN_INTERVAL = 10
DEFAULT_TIMEOUT = 10

UPDATE_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)

MODE_OPTIMIZING = "Optimizing"
MODE_MAXIMUM_LOAD = "Maximum load"
MODE_API_MODE = "API mode"
