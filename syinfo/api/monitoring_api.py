"""Monitoring API Module

Provides programmatic access to system monitoring functionality.
"""

from typing import Dict, Any, Optional, List
import json
import os

try:
    from syinfo.monitoring.core import SystemMonitor
    from syinfo.monitoring.utils import MonitoringConfig
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False


class MonitoringAPI:
    """API for system monitoring operations."""
    
    def __init__(self, config_path: Optional[str] = None, output_dir: Optional[str] = None):
        """Initialize monitoring API."""
        self.config_path = config_path
        self.output_dir = output_dir
        self.monitor = None
        
        if MONITORING_AVAILABLE:
            self.monitor = SystemMonitor(config_path=config_path, output_dir=output_dir)
    
    def start_monitoring(
        self,
        interval: int = 60,
        duration: Optional[int] = None,
        include_processes: bool = True,
        include_logs: bool = False
    ) -> Dict[str, Any]:
        """Start system monitoring."""
        if not MONITORING_AVAILABLE:
            return {
                "success": False,
                "error": "Monitoring features not available"
            }
        
        try:
            if self.monitor.start_monitoring(
                interval=interval,
                duration=duration,
                include_processes=include_processes,
                include_logs=include_logs
            ):
                return {
                    "success": True,
                    "message": "Monitoring started successfully",
                    "details": {
                        "interval": interval,
                        "duration": duration,
                        "include_processes": include_processes,
                        "include_logs": include_logs
                    }
                }
            else:
                return {"success": False, "error": "Failed to start monitoring"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def stop_monitoring(self) -> Dict[str, Any]:
        """Stop system monitoring."""
        if not MONITORING_AVAILABLE:
            return {
                "success": False,
                "error": "Monitoring features not available"
            }
        
        try:
            if self.monitor.stop_monitoring():
                return {"success": True, "message": "Monitoring stopped successfully"}
            else:
                return {"success": False, "error": "Failed to stop monitoring"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_current_stats(self) -> Dict[str, Any]:
        """Get current system statistics."""
        if not MONITORING_AVAILABLE:
            return {
                "success": False,
                "error": "Monitoring features not available"
            }
        
        try:
            stats = self.monitor.get_current_stats()
            if stats:
                return {
                    "success": True,
                    "data": stats,
                    "message": "Current stats retrieved successfully"
                }
            else:
                return {"success": False, "error": "Unable to get current stats"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def collect_snapshot(
        self,
        include_processes: bool = True,
        include_logs: bool = False,
        output_format: str = 'json'
    ) -> Dict[str, Any]:
        """Collect a single system snapshot."""
        if not MONITORING_AVAILABLE:
            return {
                "success": False,
                "error": "Monitoring features not available"
            }
        
        try:
            data = self.monitor.collect_snapshot(
                include_processes=include_processes,
                include_logs=include_logs
            )
            
            if data:
                if output_format == 'json':
                    return {
                        "success": True,
                        "data": data,
                        "message": "Snapshot collected successfully"
                    }
                else:
                    # Convert to other formats if needed
                    return {
                        "success": True,
                        "data": data,
                        "message": "Snapshot collected successfully"
                    }
            else:
                return {"success": False, "error": "Failed to collect snapshot"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get monitoring service status."""
        if not MONITORING_AVAILABLE:
            return {
                "success": False,
                "error": "Monitoring features not available"
            }
        
        try:
            status = self.monitor.get_status()
            return {
                "success": True,
                "data": status,
                "message": "Status retrieved successfully"
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_data_files(self, data_dir: Optional[str] = None) -> Dict[str, Any]:
        """Get list of collected data files."""
        if not MONITORING_AVAILABLE:
            return {
                "success": False,
                "error": "Monitoring features not available"
            }
        
        try:
            directory = data_dir or self.output_dir or "./monitoring_data"
            
            if not os.path.exists(directory):
                return {
                    "success": True,
                    "data": [],
                    "message": "No data directory found"
                }
            
            files = []
            for file in os.listdir(directory):
                if file.endswith(('.csv', '.json')):
                    file_path = os.path.join(directory, file)
                    files.append({
                        "name": file,
                        "path": file_path,
                        "size": os.path.getsize(file_path),
                        "modified": os.path.getmtime(file_path)
                    })
            
            return {
                "success": True,
                "data": files,
                "message": f"Found {len(files)} data files"
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)} 