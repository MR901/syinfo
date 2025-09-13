"""SyInfo - System Information Library

A simple, well-designed Python library for gathering system information including
hardware specifications, network configuration, and optional monitoring.

Features:
- Hardware Information: CPU, memory, disk, GPU details
- Network Information: Interfaces, connectivity, device discovery
- Software Information: OS details, kernel info, Python environment
- Optional Monitoring: Simple performance monitoring
- Export Capabilities: JSON, CSV, YAML formats
- CLI Tools: Simple command-line interface

Examples:
    Basic system information:
    >>> import syinfo
    >>> info = syinfo.get_system_info()
    >>> print(f"OS: {info['system_name']}, CPU: {info['cpu_model']}")

    Hardware details:
    >>> hardware = syinfo.get_hardware_info()
    >>> print(f"CPU: {hardware['cpu']['model']}")
    >>> print(f"Memory: {hardware['memory']['total']}")

    Network discovery:
    >>> devices = syinfo.discover_network_devices()
    >>> print(f"Found {len(devices)} devices on network")

    Print detailed tree structure:
    >>> complete_info = syinfo.get_complete_info()
    >>> syinfo.print_system_tree(complete_info)
"""

import logging
import sys
from typing import Any, Dict, List, Optional

# Version information
from ._version import __author__, __email__, __license__, __version__, __version_info__

# Configure logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Simplified exception imports
# Import core functionality
from .core.device_info import DeviceInfo
from .core.sys_info import SysInfo, print_brief_sys_info
from .core.utils import Execute, HumanReadable
from .exceptions import (
    ConfigurationError,
    DataCollectionError,
    NetworkError,
    SyInfoException,
    SystemAccessError,
    ValidationError,
)

# Try to import network features
try:
    from .core.network_info import NetworkInfo
    from .core.search_network import search_devices_on_network

    _NETWORK_AVAILABLE = True
except ImportError:
    _NETWORK_AVAILABLE = False

    # Create dummy functions
    def search_devices_on_network(*args, **kwargs):
        raise SyInfoException(
            "Network features not available. Install required dependencies.",
        )


def get_system_info() -> Dict[str, Any]:
    """Get comprehensive system information with simplified access.

    Returns:
        Dictionary containing system information with easy access keys

    Examples:
        >>> info = get_system_info()
        >>> print(f"System: {info['system_name']}")
        >>> print(f"CPU: {info['cpu_model']}")
        >>> print(f"Memory: {info['total_memory']}")
    """
    # Get complete system information
    complete_info = get_complete_info()

    # Create simplified access dictionary
    simplified = {
        # System identification
        "hostname": complete_info.get("dev_info", {}).get("static_hostname", "unknown"),
        "system_name": complete_info.get("dev_info", {})
        .get("operating_system", {})
        .get("full_name", "unknown"),
        "kernel_version": complete_info.get("dev_info", {})
        .get("operating_system", {})
        .get("kernel", "unknown"),
        "architecture": complete_info.get("dev_info", {})
        .get("operating_system", {})
        .get("architecture", "unknown"),
        "python_version": complete_info.get("dev_info", {}).get(
            "python_version", "unknown",
        ),
        # Hardware information
        "cpu_model": complete_info.get("cpu_info", {})
        .get("design", {})
        .get("model name", "unknown"),
        "cpu_cores_physical": complete_info.get("cpu_info", {})
        .get("cores", {})
        .get("physical", 0),
        "cpu_cores_logical": complete_info.get("cpu_info", {})
        .get("cores", {})
        .get("total", 0),
        "cpu_usage_percent": complete_info.get("cpu_info", {})
        .get("percentage_used", {})
        .get("total", 0),
        # Memory information
        "total_memory": complete_info.get("memory_info", {})
        .get("virtual", {})
        .get("readable", {})
        .get("total", "0 B"),
        "available_memory": complete_info.get("memory_info", {})
        .get("virtual", {})
        .get("readable", {})
        .get("available", "0 B"),
        "memory_usage_percent": complete_info.get("memory_info", {})
        .get("virtual", {})
        .get("percent", 0),
        # Time information
        "boot_time": complete_info.get("time", {})
        .get("boot_time", {})
        .get("readable", "unknown"),
        "uptime": complete_info.get("time", {})
        .get("uptime", {})
        .get("readable", "unknown"),
        # Network information (if available)
        "network_info": complete_info.get("network_info", {}),
        "mac_address": complete_info.get("dev_info", {}).get("mac_address", "unknown"),
        # Raw complete information for advanced users
        "_complete_info": complete_info,
    }

    return simplified


def get_complete_info(
    include_network: bool = False, network_scan_time: int = 5,
) -> Dict[str, Any]:
    """Get complete system information in original detailed format.

    Args:
        include_network: Whether to include network information
        network_scan_time: Time in seconds to spend scanning network

    Returns:
        Complete system information dictionary in original format

    Examples:
        >>> complete = get_complete_info()
        >>> print_system_tree(complete)  # Print in tree format
    """
    if include_network and _NETWORK_AVAILABLE:
        return SysInfo.get_all(
            search_period=network_scan_time, search_device_vendor_too=True,
        )
    else:
        return DeviceInfo.get_all()


def get_hardware_info() -> Dict[str, Any]:
    """Get detailed hardware information only.

    Returns:
        Dictionary containing hardware details

    Examples:
        >>> hw = get_hardware_info()
        >>> print(f"CPU: {hw['cpu']['model']}")
        >>> print(f"RAM: {hw['memory']['total']}")
    """
    info = DeviceInfo.get_all()

    return {
        "cpu": {
            "model": info.get("cpu_info", {})
            .get("design", {})
            .get("model name", "unknown"),
            "cores_physical": info.get("cpu_info", {})
            .get("cores", {})
            .get("physical", 0),
            "cores_logical": info.get("cpu_info", {}).get("cores", {}).get("total", 0),
            "usage_percent": info.get("cpu_info", {})
            .get("percentage_used", {})
            .get("total", 0),
            "frequency_mhz": info.get("cpu_info", {}).get("frequency_Mhz", {}),
            "design": info.get("cpu_info", {}).get("design", {}),
        },
        "memory": {
            "total_bytes": info.get("memory_info", {})
            .get("virtual", {})
            .get("in_bytes", {})
            .get("total", 0),
            "available_bytes": info.get("memory_info", {})
            .get("virtual", {})
            .get("in_bytes", {})
            .get("available", 0),
            "total": info.get("memory_info", {})
            .get("virtual", {})
            .get("readable", {})
            .get("total", "0 B"),
            "available": info.get("memory_info", {})
            .get("virtual", {})
            .get("readable", {})
            .get("available", "0 B"),
            "usage_percent": info.get("memory_info", {})
            .get("virtual", {})
            .get("percent", 0),
            "swap": info.get("memory_info", {}).get("swap", {}),
            "design": info.get("memory_info", {}).get("design", {}),
        },
        "gpu": info.get("gpu_info", {}),
        "disk": info.get("disk_info", {}),
        "device_manufacturer": info.get("dev_info", {}).get("device", {}),
    }


def get_network_info(
    scan_devices: bool = False, scan_timeout: int = 10,
) -> Dict[str, Any]:
    """Get network information and optionally scan for devices.

    Args:
        scan_devices: Whether to scan for devices on the network
        scan_timeout: Timeout for device scanning in seconds

    Returns:
        Dictionary containing network information

    Examples:
        >>> net = get_network_info(scan_devices=True)
        >>> print(f"Connected devices: {len(net.get('devices_on_network', []))}")
    """
    if not _NETWORK_AVAILABLE:
        raise SyInfoException(
            "Network features not available. Install required dependencies.",
        )

    network_collector = NetworkInfo()
    info = network_collector.get_all(
        search_period=scan_timeout if scan_devices else 0,
        search_device_vendor_too=scan_devices,
    )

    return info.get("network_info", {})


def discover_network_devices(
    timeout: int = 10, include_vendor_info: bool = True,
) -> List[Dict[str, Any]]:
    """Discover devices on the local network.

    Args:
        timeout: Scan timeout in seconds
        include_vendor_info: Whether to include vendor information

    Returns:
        List of discovered devices

    Examples:
        >>> devices = discover_network_devices(timeout=5)
        >>> for device in devices:
        ...     print(f"Device: {device['ip']} - {device.get('hostname', 'Unknown')}")
    """
    if not _NETWORK_AVAILABLE:
        raise SyInfoException(
            "Network features not available. Install required dependencies.",
        )

    try:
        return search_devices_on_network(time=timeout)
    except Exception as e:
        raise DataCollectionError(f"Failed to discover network devices: {e!s}")


def print_system_tree(info: Optional[Dict[str, Any]] = None) -> None:
    """Print system information in the original detailed tree format.

    Args:
        info: System information dictionary. If None, will collect current info.

    Examples:
        >>> print_system_tree()  # Print current system info
        >>> info = get_complete_info()
        >>> print_system_tree(info)  # Print specific info
    """
    if info is None:
        info = get_complete_info()

    if "network_info" in info:
        # Print complete system + network info
        SysInfo.print(info, return_msg=False)
    else:
        # Print device info only
        DeviceInfo.print(info, return_msg=False)


def print_brief_info() -> None:
    """Print a brief system summary for quick diagnostics."""
    print_brief_sys_info()


def export_system_info(
    format: str = "json",
    output_file: Optional[str] = None,
    include_sensitive: bool = False,
) -> str:
    """Export system information in various formats.

    Args:
        format: Export format ("json", "yaml", "csv")
        output_file: Optional output file path
        include_sensitive: Whether to include sensitive information

    Returns:
        Exported data as string (also written to file if specified)

    Examples:
        >>> json_data = export_system_info("json")
        >>> export_system_info("yaml", "system_info.yaml")
    """
    info = get_system_info()

    # Remove sensitive information if requested
    if not include_sensitive:
        sensitive_keys = ["mac_address"]
        for key in sensitive_keys:
            info.pop(key, None)

    if format.lower() == "json":
        import json

        result = json.dumps(info, indent=2, default=str)
    elif format.lower() == "yaml":
        import yaml

        # Convert complex objects to strings for YAML serialization
        yaml_safe_info = {}
        for key, value in info.items():
            if isinstance(value, dict):
                yaml_safe_info[key] = str(value) if key.startswith("_") else value
            else:
                yaml_safe_info[key] = (
                    str(value)
                    if not isinstance(value, (str, int, float, bool))
                    else value
                )
        result = yaml.dump(yaml_safe_info, default_flow_style=False)
    elif format.lower() == "csv":
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Property", "Value"])
        for key, value in info.items():
            if not isinstance(value, dict) and not key.startswith("_"):
                writer.writerow([key, str(value)])
        result = output.getvalue()
    else:
        raise ValidationError(f"Unsupported export format: {format}")

    if output_file:
        with open(output_file, "w") as f:
            f.write(result)

    return result


def create_simple_monitor(interval: int = 60):
    """Create a simple system monitor.

    Args:
        interval: Monitoring interval in seconds

    Returns:
        SimpleMonitor instance for basic monitoring

    Examples:
        >>> monitor = syinfo.create_simple_monitor(interval=30)
        >>> monitor.start(duration=300)  # Monitor for 5 minutes
        >>> results = monitor.stop()
        >>> print(f"Average CPU: {results['summary']['cpu_avg']:.1f}%")
    """
    from .simple_monitoring import create_simple_monitor as _create_monitor

    return _create_monitor(interval=interval)


def get_available_features() -> Dict[str, bool]:
    """Get information about available features.

    Returns:
        Dictionary mapping feature names to availability status

    Examples:
        >>> features = get_available_features()
        >>> if features['network']:
        ...     devices = discover_network_devices()
    """
    return {
        "core": True,  # Always available
        "network": _NETWORK_AVAILABLE,
        "monitoring": True,  # Simple monitoring always available
    }


def print_feature_status() -> None:
    """Print the status of all features."""
    features = get_available_features()

    print("SyInfo Feature Status:")
    print("-" * 30)

    for feature, available in features.items():
        status = "✓ Available" if available else "✗ Not Available"
        print(f"{feature.capitalize():<15} {status}")

    if not all(features.values()):
        print()
        print("To install missing features:")
        if not features["network"]:
            print("  pip install syinfo[network]")
        print("  pip install syinfo[full]  # Install everything")


# Module exports
__all__ = [
    # Version information
    "__version__",
    "__version_info__",
    "__author__",
    "__email__",
    "__license__",
    # High-level functions
    "get_system_info",
    "get_complete_info",
    "get_hardware_info",
    "get_network_info",
    "discover_network_devices",
    "print_system_tree",
    "print_brief_info",
    "export_system_info",
    "create_simple_monitor",
    # Feature management
    "get_available_features",
    "print_feature_status",
    # Core classes (for advanced usage)
    "DeviceInfo",
    "SysInfo",
    "HumanReadable",
    "Execute",
    # Exceptions
    "SyInfoException",
    "ConfigurationError",
    "DataCollectionError",
    "NetworkError",
    "SystemAccessError",
    "ValidationError",
    # Legacy compatibility
    "print_brief_sys_info",
]

# Module initialization (debug only)
if __debug__:
    import os

    if os.environ.get("SYINFO_DEBUG"):
        available_features = [k for k, v in get_available_features().items() if v]
