"""Info Commands Module

Handles legacy system information commands for backward compatibility.
"""

import json
import sys
from typing import Dict, Any, Optional

from syinfo.device_info import DeviceInfo
from syinfo.network_info import NetworkInfo
from syinfo.sys_info import SysInfo


class InfoCommands:
    """Legacy system information commands."""
    
    @staticmethod
    def handle_device_info(disable_print: bool = False, return_json: bool = False) -> Dict[str, Any]:
        """Handle device information command."""
        try:
            info = DeviceInfo.get_all()
            
            if not disable_print:
                DeviceInfo.print(info)
            
            if return_json:
                print(json.dumps(info))
            
            return {"success": True, "data": info}
        except Exception as e:
            error_msg = f"Failed to get device info: {e}"
            if not disable_print:
                print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def handle_network_info(
        search_period: int = 10,
        search_device_vendor_too: bool = True,
        disable_print: bool = False,
        return_json: bool = False
    ) -> Dict[str, Any]:
        """Handle network information command."""
        try:
            info = NetworkInfo.get_all(
                search_period=search_period,
                search_device_vendor_too=search_device_vendor_too
            )
            
            if not disable_print:
                NetworkInfo.print(info)
            
            if return_json:
                print(json.dumps(info))
            
            return {"success": True, "data": info}
        except Exception as e:
            error_msg = f"Failed to get network info: {e}"
            if not disable_print:
                print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def handle_system_info(
        search_period: int = 10,
        search_device_vendor_too: bool = True,
        disable_print: bool = False,
        return_json: bool = False
    ) -> Dict[str, Any]:
        """Handle system information command."""
        try:
            info = SysInfo.get_all(
                search_period=search_period,
                search_device_vendor_too=search_device_vendor_too
            )
            
            if not disable_print:
                SysInfo.print(info)
            
            if return_json:
                print(json.dumps(info))
            
            return {"success": True, "data": info}
        except Exception as e:
            error_msg = f"Failed to get system info: {e}"
            if not disable_print:
                print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg} 