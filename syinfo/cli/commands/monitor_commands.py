"""Monitor Commands Module

Handles system monitoring commands.
"""

import json
import sys
from typing import Dict, Any, Optional

try:
    from syinfo.monitoring.core import SystemMonitor
    from syinfo.monitoring.utils import MonitoringConfig
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False


class MonitorCommands:
    """System monitoring commands."""
    
    @staticmethod
    def start_monitoring(
        config_path: Optional[str] = None,
        output_dir: Optional[str] = None,
        interval: int = 60,
        duration: Optional[int] = None,
        format: str = 'csv'
    ) -> Dict[str, Any]:
        """Start system monitoring."""
        if not MONITORING_AVAILABLE:
            return {
                "success": False,
                "error": "Monitoring features not available. Install required dependencies."
            }
        
        try:
            config = MonitoringConfig(config_path) if config_path else None
            monitor = SystemMonitor(
                config_path=config_path,
                output_dir=output_dir
            )
            
            if monitor.start_monitoring(interval=interval, duration=duration):
                return {
                    "success": True,
                    "message": f"Monitoring started successfully (interval: {interval}s)",
                    "details": {
                        "interval": interval,
                        "duration": duration,
                        "output_dir": output_dir,
                        "format": format
                    }
                }
            else:
                return {"success": False, "error": "Failed to start monitoring"}
                
        except Exception as e:
            return {"success": False, "error": f"Monitoring error: {e}"}
    
    @staticmethod
    def stop_monitoring() -> Dict[str, Any]:
        """Stop system monitoring."""
        if not MONITORING_AVAILABLE:
            return {
                "success": False,
                "error": "Monitoring features not available. Install required dependencies."
            }
        
        try:
            monitor = SystemMonitor()
            if monitor.stop_monitoring():
                return {"success": True, "message": "Monitoring stopped successfully"}
            else:
                return {"success": False, "error": "Failed to stop monitoring"}
                
        except Exception as e:
            return {"success": False, "error": f"Monitoring error: {e}"}
    
    @staticmethod
    def get_status() -> Dict[str, Any]:
        """Get current monitoring status."""
        if not MONITORING_AVAILABLE:
            return {
                "success": False,
                "error": "Monitoring features not available. Install required dependencies."
            }
        
        try:
            monitor = SystemMonitor()
            stats = monitor.get_current_stats()
            
            if stats:
                return {
                    "success": True,
                    "data": stats,
                    "message": "Current system status retrieved successfully"
                }
            else:
                return {"success": False, "error": "Unable to get system status"}
                
        except Exception as e:
            return {"success": False, "error": f"Status error: {e}"}
    
    @staticmethod
    def collect_data(
        output_dir: Optional[str] = None,
        format: str = 'csv',
        include_processes: bool = True,
        include_logs: bool = False
    ) -> Dict[str, Any]:
        """Collect one-time system data."""
        if not MONITORING_AVAILABLE:
            return {
                "success": False,
                "error": "Monitoring features not available. Install required dependencies."
            }
        
        try:
            monitor = SystemMonitor(output_dir=output_dir)
            data = monitor.collect_snapshot(
                include_processes=include_processes,
                include_logs=include_logs
            )
            
            if data:
                return {
                    "success": True,
                    "data": data,
                    "message": "Data collection completed successfully"
                }
            else:
                return {"success": False, "error": "Failed to collect data"}
                
        except Exception as e:
            return {"success": False, "error": f"Data collection error: {e}"} 