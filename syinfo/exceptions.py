"""SyInfo Exceptions - Simplified

Essential exceptions for the SyInfo library without over-engineering.
"""


class SyInfoException(Exception):
    """Base exception for all SyInfo errors."""

    pass


class DataCollectionError(SyInfoException):
    """Raised when data collection fails."""

    pass


class NetworkError(SyInfoException):
    """Raised when network operations fail."""

    pass


class SystemAccessError(SyInfoException):
    """Raised when system access is denied or insufficient privileges."""

    pass


class ValidationError(SyInfoException):
    """Raised when input validation fails."""

    pass


class ConfigurationError(SyInfoException):
    """Raised when configuration is invalid."""

    pass


__all__ = [
    "SyInfoException",
    "DataCollectionError",
    "NetworkError",
    "SystemAccessError",
    "ValidationError",
    "ConfigurationError",
]
