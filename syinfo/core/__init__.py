"""Core module for SyInfo.

This module provides the core functionality for system information gathering,
including device information, system information, and utility functions.
"""

# Import core classes and functions
from .device_info import DeviceInfo
from .sys_info import SysInfo, print_brief_sys_info
from .utils import Execute, HumanReadable, create_highlighted_heading

# Exceptions are now imported from parent package

# Try to import network info if available
try:
    from .network_info import NetworkInfo

    NETWORK_AVAILABLE = True
except ImportError:
    NETWORK_AVAILABLE = False

    # Create dummy class for compatibility
    class NetworkInfo:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "Network features not available. Install required dependencies.",
            )


__all__ = [
    # Core classes
    "DeviceInfo",
    "SysInfo",
    "NetworkInfo",
    # Utility classes
    "HumanReadable",
    "Execute",
    # Utility functions
    "create_highlighted_heading",
    "print_brief_sys_info",
    # Feature flag
    "NETWORK_AVAILABLE",
]
