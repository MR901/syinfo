"""SyInfo CLI - Simplified Command Line Interface

Simple CLI commands without over-engineered command structure.
"""

import json
from typing import Any, Dict

from .core.device_info import DeviceInfo
from .core.sys_info import SysInfo, print_brief_sys_info
from .exceptions import SyInfoException


def handle_info_command(info_type: str, output_json: bool = False) -> Dict[str, Any]:
    """Handle info commands.

    Args:
        info_type: Type of info ('system', 'device', 'network', 'brief')
        output_json: Whether to output as JSON

    Returns:
        Dictionary with command results
    """
    try:
        if info_type == "brief":
            if not output_json:
                print_brief_sys_info()
            return {"success": True, "message": "Brief info displayed"}

        elif info_type == "device":
            info = DeviceInfo.get_all()
            if not output_json:
                DeviceInfo.print(info)
            else:
                print(json.dumps(info, indent=2, default=str))
            return {"success": True, "data": info}

        elif info_type == "system":
            info = SysInfo.get_all()
            if not output_json:
                SysInfo.print(info)
            else:
                print(json.dumps(info, indent=2, default=str))
            return {"success": True, "data": info}

        elif info_type == "network":
            try:
                from .core.network_info import NetworkInfo

                network_info = NetworkInfo()
                info = network_info.get_all()
                if not output_json:
                    NetworkInfo.print(info)
                else:
                    print(json.dumps(info, indent=2, default=str))
                return {"success": True, "data": info}
            except ImportError:
                print(
                    "Network features not available. Install with: pip install syinfo[network]",
                )
                return {"success": False, "error": "Network features not available"}
        else:
            print(f"Unknown info type: {info_type}")
            print("Available types: system, device, network, brief")
            return {"success": False, "error": f"Unknown info type: {info_type}"}

    except SyInfoException as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"success": False, "error": str(e)}


def handle_export_command(
    format_type: str = "json", output_file: str = None,
) -> Dict[str, Any]:
    """Handle export command.

    Args:
        format_type: Export format ('json', 'yaml', 'csv')
        output_file: Optional output file path

    Returns:
        Dictionary with command results
    """
    try:
        # Import the main API export function
        from . import export_system_info

        result = export_system_info(format_type, output_file)

        if output_file:
            print(f"System information exported to {output_file}")
        else:
            print(result)

        return {"success": True, "exported_to": output_file}

    except Exception as e:
        print(f"Export failed: {e}")
        return {"success": False, "error": str(e)}


def show_help():
    """Show help information."""
    help_text = """
SyInfo - System Information Library

Usage: syinfo <command> [options]

Commands:
  info <type>     Show system information
    - system      Complete system + network info
    - device      Hardware/device information only  
    - network     Network information only
    - brief       Brief system summary

  export          Export system info
    --format      Format (json/yaml/csv) [default: json]
    --output      Output file path [optional]

Options:
  --json          Output as JSON
  --help, -h      Show this help

Examples:
  syinfo info system
  syinfo info device --json
  syinfo export --format yaml --output system.yaml
"""
    print(help_text)


__all__ = ["handle_info_command", "handle_export_command", "show_help"]
