"""
System metrics collection module.

This module provides comprehensive system metrics collection including
CPU, memory, disk, and network statistics.
"""

import os
import time
import psutil
from datetime import datetime
from typing import Dict, List, Optional
import threading

from ..utils.logger import MonitoringLogger
from ..utils.config_manager import MonitoringConfig


class SystemCollector:
    """
    System metrics collector with real-time monitoring capabilities.
    
    Features:
    - CPU usage monitoring (overall and per-core)
    - Memory usage tracking (RAM and swap)
    - Disk I/O and usage monitoring
    - Network interface statistics
    - Configurable collection intervals
    - Thread-safe data collection
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize system collector.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = MonitoringConfig(config_path)
        self.logger = MonitoringLogger()
        self.collecting = False
        self.collector_thread = None
        self.stop_event = threading.Event()
        
    def start_collection(self, interval: int = 60, duration: Optional[int] = None) -> bool:
        """
        Start continuous system metrics collection.
        
        Args:
            interval: Collection interval in seconds
            duration: Total collection duration in seconds (None for continuous)
            
        Returns:
            True if collection started successfully, False otherwise
        """
        try:
            if self.collecting:
                self.logger.log_monitoring_event("WARNING", "Collection already running")
                return False
                
            self.logger.log_monitoring_event("INFO", f"Starting system collection (interval: {interval}s)")
            self.collecting = True
            self.stop_event.clear()
            
            # Start collection in separate thread
            self.collector_thread = threading.Thread(
                target=self._collection_loop,
                args=(interval, duration),
                daemon=True
            )
            self.collector_thread.start()
            
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to start system collection")
            return False
    
    def stop_collection(self) -> bool:
        """
        Stop system metrics collection.
        
        Returns:
            True if collection stopped successfully, False otherwise
        """
        try:
            if not self.collecting:
                return True
                
            self.logger.log_monitoring_event("INFO", "Stopping system collection")
            self.collecting = False
            self.stop_event.set()
            
            if self.collector_thread and self.collector_thread.is_alive():
                self.collector_thread.join(timeout=10)
                
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to stop system collection")
            return False
    
    def collect_snapshot(self) -> Dict:
        """
        Collect a single snapshot of system metrics.
        
        Returns:
            Dictionary containing current system metrics
        """
        try:
            current_time = time.time()
            
            # CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
            cpu_freq = psutil.cpu_freq()
            
            # Memory information
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk information
            disk_usage = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Network information
            network_io = psutil.net_io_counters()
            network_interfaces = self._get_network_interfaces()
            
            # System load
            load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else (0, 0, 0)
            
            metrics = {
                "timestamp": current_time,
                "datetime": datetime.fromtimestamp(current_time).isoformat(),
                "cpu": {
                    "percent": cpu_percent,
                    "per_core": cpu_per_core,
                    "count": psutil.cpu_count(),
                    "count_logical": psutil.cpu_count(logical=True),
                    "frequency": {
                        "current": cpu_freq.current if cpu_freq else 0,
                        "min": cpu_freq.min if cpu_freq else 0,
                        "max": cpu_freq.max if cpu_freq else 0
                    }
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "free": memory.free,
                    "percent": memory.percent,
                    "swap_total": swap.total,
                    "swap_used": swap.used,
                    "swap_free": swap.free,
                    "swap_percent": swap.percent
                },
                "disk": {
                    "total": disk_usage.total,
                    "used": disk_usage.used,
                    "free": disk_usage.free,
                    "percent": disk_usage.percent,
                    "io_read_bytes": disk_io.read_bytes if disk_io else 0,
                    "io_write_bytes": disk_io.write_bytes if disk_io else 0,
                    "io_read_count": disk_io.read_count if disk_io else 0,
                    "io_write_count": disk_io.write_count if disk_io else 0
                },
                "network": {
                    "bytes_sent": network_io.bytes_sent,
                    "bytes_recv": network_io.bytes_recv,
                    "packets_sent": network_io.packets_sent,
                    "packets_recv": network_io.packets_recv,
                    "interfaces": network_interfaces
                },
                "system": {
                    "load_1min": load_avg[0],
                    "load_5min": load_avg[1],
                    "load_15min": load_avg[2],
                    "uptime": time.time() - psutil.boot_time()
                }
            }
            
            return metrics
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to collect system snapshot")
            return {}
    
    def _collection_loop(self, interval: int, duration: Optional[int]):
        """Main collection loop."""
        start_time = time.time()
        
        while self.collecting and not self.stop_event.is_set():
            try:
                # Check duration limit
                if duration and (time.time() - start_time) > duration:
                    self.logger.log_monitoring_event("INFO", "Collection duration reached")
                    break
                
                # Collect system metrics
                metrics = self.collect_snapshot()
                
                # Store metrics (this would integrate with storage module)
                # self.storage.store_system_metrics(metrics)
                
                # Wait for next interval
                self.stop_event.wait(interval)
                
            except Exception as e:
                self.logger.log_error_with_context(e, "Error in collection loop")
                time.sleep(5)  # Brief pause before retry
        
        self.collecting = False
    
    def _get_network_interfaces(self) -> Dict:
        """Get network interface statistics."""
        try:
            interfaces = {}
            for interface, stats in psutil.net_if_stats().items():
                if stats.isup:
                    try:
                        io_stats = psutil.net_io_counters(pernic=True).get(interface)
                        if io_stats:
                            interfaces[interface] = {
                                "bytes_sent": io_stats.bytes_sent,
                                "bytes_recv": io_stats.bytes_recv,
                                "packets_sent": io_stats.packets_sent,
                                "packets_recv": io_stats.packets_recv,
                                "speed": stats.speed,
                                "mtu": stats.mtu
                            }
                    except Exception:
                        continue
            
            return interfaces
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to get network interfaces")
            return {}
    
    def get_collection_status(self) -> Dict:
        """
        Get current collection status.
        
        Returns:
            Dictionary with collection status information
        """
        return {
            "collecting": self.collecting,
            "thread_alive": self.collector_thread.is_alive() if self.collector_thread else False,
            "stop_requested": self.stop_event.is_set()
        } 