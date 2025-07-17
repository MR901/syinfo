"""Info API Module

Provides programmatic access to legacy system information functionality.
"""

from typing import Dict, Any, Optional
import json

try:
    from syinfo.device_info import DeviceInfo
    from syinfo.network_info import NetworkInfo
    from syinfo.sys_info import SysInfo
    INFO_AVAILABLE = True
except ImportError:
    INFO_AVAILABLE = False


class InfoAPI:
    """API for system information operations."""
    
    def __init__(self):
        """Initialize info API."""
        self.info_available = INFO_AVAILABLE
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get device information."""
        if not INFO_AVAILABLE:
            return {
                "success": False,
                "error": "Device info features not available"
            }
        
        try:
            info = DeviceInfo.get_all()
            return {
                "success": True,
                "data": info,
                "message": "Device information retrieved successfully"
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_network_info(
        self,
        search_period: int = 10,
        search_device_vendor_too: bool = True
    ) -> Dict[str, Any]:
        """Get network information."""
        if not INFO_AVAILABLE:
            return {
                "success": False,
                "error": "Network info features not available"
            }
        
        try:
            info = NetworkInfo.get_all(
                search_period=search_period,
                search_device_vendor_too=search_device_vendor_too
            )
            return {
                "success": True,
                "data": info,
                "message": "Network information retrieved successfully"
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_system_info(
        self,
        search_period: int = 10,
        search_device_vendor_too: bool = True
    ) -> Dict[str, Any]:
        """Get combined system information."""
        if not INFO_AVAILABLE:
            return {
                "success": False,
                "error": "System info features not available"
            }
        
        try:
            info = SysInfo.get_all(
                search_period=search_period,
                search_device_vendor_too=search_device_vendor_too
            )
            return {
                "success": True,
                "data": info,
                "message": "System information retrieved successfully"
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_all_info(
        self,
        search_period: int = 10,
        search_device_vendor_too: bool = True
    ) -> Dict[str, Any]:
        """Get all available system information."""
        if not INFO_AVAILABLE:
            return {
                "success": False,
                "error": "System info features not available"
            }
        
        try:
            device_info = DeviceInfo.get_all()
            network_info = NetworkInfo.get_all(
                search_period=search_period,
                search_device_vendor_too=search_device_vendor_too
            )
            system_info = SysInfo.get_all(
                search_period=search_period,
                search_device_vendor_too=search_device_vendor_too
            )
            
            all_info = {
                "device": device_info,
                "network": network_info,
                "system": system_info,
                "metadata": {
                    "search_period": search_period,
                    "search_device_vendor_too": search_device_vendor_too
                }
            }
            
            return {
                "success": True,
                "data": all_info,
                "message": "All system information retrieved successfully"
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def print_device_info(self) -> Dict[str, Any]:
        """Print device information to console."""
        if not INFO_AVAILABLE:
            return {
                "success": False,
                "error": "Device info features not available"
            }
        
        try:
            info = DeviceInfo.get_all()
            DeviceInfo.print(info)
            return {
                "success": True,
                "message": "Device information printed successfully"
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def print_network_info(
        self,
        search_period: int = 10,
        search_device_vendor_too: bool = True
    ) -> Dict[str, Any]:
        """Print network information to console."""
        if not INFO_AVAILABLE:
            return {
                "success": False,
                "error": "Network info features not available"
            }
        
        try:
            info = NetworkInfo.get_all(
                search_period=search_period,
                search_device_vendor_too=search_device_vendor_too
            )
            NetworkInfo.print(info)
            return {
                "success": True,
                "message": "Network information printed successfully"
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def print_system_info(
        self,
        search_period: int = 10,
        search_device_vendor_too: bool = True
    ) -> Dict[str, Any]:
        """Print system information to console."""
        if not INFO_AVAILABLE:
            return {
                "success": False,
                "error": "System info features not available"
            }
        
        try:
            info = SysInfo.get_all(
                search_period=search_period,
                search_device_vendor_too=search_device_vendor_too
            )
            SysInfo.print(info)
            return {
                "success": True,
                "message": "System information printed successfully"
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)} 