"""Constants used throughout the SyInfo package."""

from typing import Final

# Display constants for missing or unavailable data
UNKNOWN: Final[str] = "unknown"
NEED_SUDO: Final[str] = "sudo needed"

# Default configuration values
DEFAULT_MONITORING_INTERVAL: Final[int] = 60
DEFAULT_SEARCH_PERIOD: Final[int] = 10
DEFAULT_MAX_PROCESSES: Final[int] = 10
DEFAULT_LOG_LEVEL: Final[str] = "INFO"

# File size limits (in bytes)
MAX_LOG_FILE_SIZE: Final[int] = 10 * 1024 * 1024  # 10MB
MAX_DATA_FILE_SIZE: Final[int] = 100 * 1024 * 1024  # 100MB

# Time constants (in seconds)
DAY_IN_SECONDS: Final[int] = 24 * 3600
HOUR_IN_SECONDS: Final[int] = 3600
MINUTE_IN_SECONDS: Final[int] = 60

# Size conversion constants
BYTES_IN_KB: Final[int] = 1024
BYTES_IN_MB: Final[int] = 1024 * 1024
BYTES_IN_GB: Final[int] = 1024 * 1024 * 1024
BYTES_IN_TB: Final[int] = 1024 * 1024 * 1024 * 1024
