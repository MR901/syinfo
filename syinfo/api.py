"""High-level SyInfo API class.

Encapsulates the top-level helper functions as methods to provide an OO entry
point while keeping the package root clean and import-fast.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .core.device_info import DeviceInfo
from .core.system_info import SystemInfo, print_brief_sys_info
from .core.utils import HumanReadable
from .exceptions import (
    ConfigurationError,
    DataCollectionError,
    NetworkError,
    SyInfoException,
    SystemAccessError,
    ValidationError,
)


class SyInfoAPI:
    """Object-oriented facade for SyInfo's top-level features."""

    # ---------- Core collection ----------
    def get_complete_info(
        self, include_network: bool = False, network_scan_time: int = 5
    ) -> Dict[str, Any]:
        if include_network:
            try:
                return SystemInfo.get_all(
                    search_period=network_scan_time, search_device_vendor_too=True
                )
            except Exception as e:
                raise DataCollectionError("Failed to collect system + network info", e)
        return DeviceInfo.get_all()

    def get_system_info(self) -> Dict[str, Any]:
        complete_info = self.get_complete_info()
        simplified = {
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
                "python_version", "unknown"
            ),
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
            "boot_time": complete_info.get("time", {})
            .get("boot_time", {})
            .get("readable", "unknown"),
            "uptime": complete_info.get("time", {})
            .get("uptime", {})
            .get("readable", "unknown"),
            "network_info": complete_info.get("network_info", {}),
            "mac_address": complete_info.get("dev_info", {}).get("mac_address", "unknown"),
            "_complete_info": complete_info,
        }
        return simplified

    def get_hardware_info(self) -> Dict[str, Any]:
        info = DeviceInfo.get_all()
        return {
            "cpu": {
                "model": info.get("cpu_info", {}).get("design", {}).get("model name", "unknown"),
                "cores_physical": info.get("cpu_info", {}).get("cores", {}).get("physical", 0),
                "cores_logical": info.get("cpu_info", {}).get("cores", {}).get("total", 0),
                "usage_percent": info.get("cpu_info", {}).get("percentage_used", {}).get("total", 0),
                "frequency_mhz": info.get("cpu_info", {}).get("frequency_Mhz", {}),
                "design": info.get("cpu_info", {}).get("design", {}),
            },
            "memory": {
                "total_bytes": info.get("memory_info", {}).get("virtual", {}).get("in_bytes", {}).get("total", 0),
                "available_bytes": info.get("memory_info", {}).get("virtual", {}).get("in_bytes", {}).get("available", 0),
                "total": info.get("memory_info", {}).get("virtual", {}).get("readable", {}).get("total", "0 B"),
                "available": info.get("memory_info", {}).get("virtual", {}).get("readable", {}).get("available", "0 B"),
                "usage_percent": info.get("memory_info", {}).get("virtual", {}).get("percent", 0),
                "swap": info.get("memory_info", {}).get("swap", {}),
                "design": info.get("memory_info", {}).get("design", {}),
            },
            "gpu": info.get("gpu_info", {}),
            "disk": info.get("disk_info", {}),
            "device_manufacturer": info.get("dev_info", {}).get("device", {}),
        }

    # ---------- Network ----------
    def get_network_info(self, scan_devices: bool = False, scan_timeout: int = 10) -> Dict[str, Any]:
        from .core.network_info import NetworkInfo  # local import (optional dep)
        from .exceptions import SyInfoException

        network_collector = NetworkInfo()
        info = network_collector.get_all(
            search_period=scan_timeout if scan_devices else 0,
            search_device_vendor_too=scan_devices,
        )
        return info.get("network_info", {})

    def discover_network_devices(self, timeout: int = 10, include_vendor_info: bool = True) -> List[Dict[str, Any]]:
        try:
            from .core.search_network import search_devices_on_network
        except ImportError as e:
            raise SyInfoException("Network features not available. Install required dependencies.") from e

        try:
            return search_devices_on_network(time=timeout)
        except Exception as e:
            raise DataCollectionError(f"Failed to discover network devices: {e!s}")

    # ---------- Display & export ----------
    def print_system_tree(self, info: Optional[Dict[str, Any]] = None) -> None:
        if info is None:
            info = self.get_complete_info()
        if "network_info" in info:
            SystemInfo.print(info, return_msg=False)
        else:
            DeviceInfo.print(info, return_msg=False)

    def print_brief_info(self) -> None:
        print_brief_sys_info()

    def export_system_info(
        self, format: str = "json", output_file: Optional[str] = None, include_sensitive: bool = False
    ) -> str:
        info = self.get_system_info()
        if not include_sensitive:
            for key in ["mac_address"]:
                info.pop(key, None)

        if format.lower() == "json":
            import json

            result = json.dumps(info, indent=2, default=str)
        elif format.lower() == "yaml":
            import yaml

            yaml_safe_info: Dict[str, Any] = {}
            for key, value in info.items():
                if isinstance(value, dict):
                    yaml_safe_info[key] = str(value) if key.startswith("_") else value
                else:
                    yaml_safe_info[key] = value if isinstance(value, (str, int, float, bool)) else str(value)
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

    # ---------- Monitoring ----------
    def create_system_monitor(self, interval: int = 60, **kwargs):
        from .resource_monitor.system_monitor import SystemMonitor

        return SystemMonitor(interval=interval, **kwargs)

    # ---------- Feature status ----------
    def get_available_features(self) -> Dict[str, bool]:
        try:
            import importlib

            _has_network = importlib.util.find_spec("syinfo.core.network_info") is not None
        except Exception:
            _has_network = False

        return {
            "core": True,
            "network": _has_network,
            "monitoring": True,
        }

    def print_feature_status(self) -> None:
        features = self.get_available_features()
        print("SyInfo Feature Status:")
        print("-" * 30)
        for feature, available in features.items():
            status = "✓ Available" if available else "✗ Not Available"
            print(f"{feature.capitalize():<15} {status}")


__all__ = ["SyInfoAPI"]


