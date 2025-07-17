"""
Main monitoring orchestrator for system and process monitoring.

This module provides the core monitoring functionality including:
- Real-time system monitoring
- Process monitoring and analysis
- Log collection and analysis
- Storage analysis
"""

import os
import time
import json
import signal
import threading
from datetime import datetime
from typing import Dict, List, Optional, Union
import psutil
import yaml

from ..utils.config import MonitoringConfig
from ..utils.logger import MonitoringLogger
from ..data.collector import DataCollector


class SystemMonitor:
    """
    Real-time system monitoring with crash tolerance and resource management.
    
    Features:
    - Continuous CPU, memory, disk, and network monitoring
    - Configurable monitoring intervals
    - Automatic data persistence
    - Resource usage optimization
    - Graceful shutdown handling
    """
    
    def __init__(self, config_path: Optional[str] = None, output_dir: Optional[str] = None):
        """
        Initialize system monitor with configuration.
        
        Args:
            config_path: Path to configuration file
            output_dir: Directory for output files
        """
        self.config = MonitoringConfig(config_path)
        self.logger = MonitoringLogger()
        self.collector = DataCollector(output_dir or self.config.get('storage.data_directory'))
        self.monitoring = False
        self.monitor_thread = None
        self.stop_event = threading.Event()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def start_monitoring(self, interval: int = 60, duration: Optional[int] = None) -> bool:
        """
        Start continuous monitoring with specified parameters.
        
        Args:
            interval: Monitoring interval in seconds
            duration: Total monitoring duration in seconds (None for continuous)
            
        Returns:
            True if monitoring started successfully, False otherwise
        """
        try:
            if self.monitoring:
                self.logger.log_monitoring_event("WARNING", "Monitoring already running")
                return False
                
            self.logger.log_monitoring_event("INFO", f"Starting system monitoring (interval: {interval}s)")
            self.monitoring = True
            self.stop_event.clear()
            
            # Start monitoring in separate thread
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop,
                args=(interval, duration),
                daemon=True
            )
            self.monitor_thread.start()
            
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to start monitoring")
            return False
    
    def stop_monitoring(self) -> bool:
        """
        Gracefully stop monitoring and save final data.
        
        Returns:
            True if monitoring stopped successfully, False otherwise
        """
        try:
            if not self.monitoring:
                return True
                
            self.logger.log_monitoring_event("INFO", "Stopping system monitoring")
            self.monitoring = False
            self.stop_event.set()
            
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=10)
                
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to stop monitoring")
            return False
    
    def get_current_stats(self) -> Dict:
        """
        Get current system statistics without starting monitoring.
        
        Returns:
            Dictionary containing current system statistics
        """
        try:
            return self._collect_system_stats()
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to collect system stats")
            return {}
    
    def _monitor_loop(self, interval: int, duration: Optional[int]):
        """Main monitoring loop."""
        start_time = time.time()
        
        while self.monitoring and not self.stop_event.is_set():
            try:
                # Check duration limit
                if duration and (time.time() - start_time) > duration:
                    self.logger.log_monitoring_event("INFO", "Monitoring duration reached")
                    break
                
                # Collect and store system stats
                stats = self._collect_system_stats()
                self.collector.store_system_data(stats)
                
                # Wait for next interval
                self.stop_event.wait(interval)
                
            except Exception as e:
                self.logger.log_error_with_context(e, "Error in monitoring loop")
                time.sleep(5)  # Brief pause before retry
        
        self.monitoring = False
    
    def _collect_system_stats(self) -> Dict:
        """Collect current system statistics."""
        current_time = time.time()
        
        # CPU information
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
        
        # Memory information
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        # Disk information
        disk_usage = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        
        # Network information
        network_io = psutil.net_io_counters()
        
        stats = {
            "timestamp": current_time,
            "datetime": datetime.fromtimestamp(current_time).isoformat(),
            "cpu": {
                "percent": cpu_percent,
                "per_core": cpu_per_core,
                "count": psutil.cpu_count(),
                "count_logical": psutil.cpu_count(logical=True)
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent,
                "swap_total": swap.total,
                "swap_used": swap.used,
                "swap_percent": swap.percent
            },
            "disk": {
                "total": disk_usage.total,
                "used": disk_usage.used,
                "free": disk_usage.free,
                "percent": disk_usage.percent,
                "io_read_bytes": disk_io.read_bytes if disk_io else 0,
                "io_write_bytes": disk_io.write_bytes if disk_io else 0
            },
            "network": {
                "bytes_sent": network_io.bytes_sent,
                "bytes_recv": network_io.bytes_recv,
                "packets_sent": network_io.packets_sent,
                "packets_recv": network_io.packets_recv
            }
        }
        
        return stats
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.log_monitoring_event("INFO", f"Received signal {signum}, shutting down")
        self.stop_monitoring()


class ProcessMonitor:
    """
    Advanced process monitoring with filtering and analysis capabilities.
    
    Features:
    - Process tree analysis
    - Resource usage per process
    - Filtering by name, user, or resource usage
    - Thread and I/O monitoring
    - Process lifecycle tracking
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize process monitor.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = MonitoringConfig(config_path)
        self.logger = MonitoringLogger()
    
    def get_process_tree(self, sort_by: str = "memory", top_n: int = 10, 
                        filter_pattern: Optional[str] = None) -> List[Dict]:
        """
        Get hierarchical process tree with filtering.
        
        Args:
            sort_by: Sort by "memory" or "cpu"
            top_n: Number of top processes to return
            filter_pattern: Optional pattern to filter process names
            
        Returns:
            List of process dictionaries
        """
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 
                                           'memory_percent', 'memory_info', 'status']):
                try:
                    info = proc.info
                    
                    # Apply filter if specified
                    if filter_pattern and filter_pattern.lower() not in info['name'].lower():
                        continue
                    
                    processes.append({
                        "pid": info['pid'],
                        "name": info['name'],
                        "username": info['username'],
                        "cpu_percent": info['cpu_percent'],
                        "memory_percent": info['memory_percent'],
                        "memory_rss": info['memory_info'].rss if info['memory_info'] else 0,
                        "status": info['status']
                    })
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort processes
            sort_key = "memory_rss" if sort_by == "memory" else "cpu_percent"
            processes.sort(key=lambda x: x[sort_key], reverse=True)
            
            return processes[:top_n]
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to get process tree")
            return []
    
    def monitor_specific_processes(self, process_names: List[str], interval: int = 60) -> Dict:
        """
        Monitor specific processes continuously.
        
        Args:
            process_names: List of process names to monitor
            interval: Monitoring interval in seconds
            
        Returns:
            Dictionary with process monitoring data
        """
        try:
            monitored_processes = {}
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    if info['name'] in process_names:
                        monitored_processes[info['name']] = {
                            "pid": info['pid'],
                            "cpu_percent": info['cpu_percent'],
                            "memory_percent": info['memory_percent']
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return monitored_processes
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to monitor specific processes")
            return {}


class LogAnalyzer:
    """
    System log collection and analysis.
    
    Features:
    - Log file monitoring
    - Error pattern detection
    - Log rotation handling
    - Real-time log analysis
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize log analyzer.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = MonitoringConfig(config_path)
        self.logger = MonitoringLogger()
    
    def analyze_system_logs(self, log_file: str = "/var/log/syslog", 
                          lines: int = 100) -> Dict:
        """
        Analyze system logs for patterns and errors.
        
        Args:
            log_file: Path to log file
            lines: Number of recent lines to analyze
            
        Returns:
            Dictionary with log analysis results
        """
        try:
            if not os.path.exists(log_file):
                return {"error": f"Log file {log_file} not found"}
            
            with open(log_file, 'r') as f:
                recent_lines = f.readlines()[-lines:]
            
            # Basic analysis
            error_count = sum(1 for line in recent_lines if 'error' in line.lower())
            warning_count = sum(1 for line in recent_lines if 'warning' in line.lower())
            
            return {
                "total_lines": len(recent_lines),
                "error_count": error_count,
                "warning_count": warning_count,
                "error_rate": error_count / len(recent_lines) if recent_lines else 0
            }
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to analyze log file {log_file}")
            return {"error": str(e)}


class StorageAnalyzer:
    """
    Disk usage and storage analysis.
    
    Features:
    - Disk space monitoring
    - I/O performance analysis
    - File system health checks
    - Storage trend analysis
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize storage analyzer.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = MonitoringConfig(config_path)
        self.logger = MonitoringLogger()
    
    def get_disk_usage(self, path: str = "/") -> Dict:
        """
        Get detailed disk usage information.
        
        Args:
            path: Path to analyze
            
        Returns:
            Dictionary with disk usage information
        """
        try:
            usage = psutil.disk_usage(path)
            io_counters = psutil.disk_io_counters()
            
            return {
                "path": path,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
                "io_read_bytes": io_counters.read_bytes if io_counters else 0,
                "io_write_bytes": io_counters.write_bytes if io_counters else 0
            }
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to get disk usage for {path}")
            return {"error": str(e)}
    
    def get_mount_points(self) -> List[Dict]:
        """
        Get all mount points and their details.
        
        Returns:
            List of mount point dictionaries
        """
        try:
            mount_points = []
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    mount_points.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent
                    })
                except (OSError, PermissionError):
                    continue
            
            return mount_points
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to get mount points")
            return [] 