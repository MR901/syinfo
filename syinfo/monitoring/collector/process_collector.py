"""
Process metrics collection module.

This module provides comprehensive process monitoring including
resource usage, process tree analysis, and performance metrics.
"""

import psutil
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import threading

from ..utils.logger import MonitoringLogger
from ..utils.config_manager import MonitoringConfig


class ProcessCollector:
    """
    Process metrics collector with filtering and analysis capabilities.
    
    Features:
    - Process tree analysis
    - Resource usage per process
    - Process filtering by name, user, or resource usage
    - Thread and I/O monitoring
    - Process lifecycle tracking
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize process collector.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = MonitoringConfig(config_path)
        self.logger = MonitoringLogger()
        self.collecting = False
        self.collector_thread = None
        self.stop_event = threading.Event()
        
    def start_collection(self, interval: int = 60, top_n: int = 10, 
                        filter_pattern: Optional[str] = None) -> bool:
        """
        Start continuous process metrics collection.
        
        Args:
            interval: Collection interval in seconds
            top_n: Number of top processes to monitor
            filter_pattern: Optional pattern to filter process names
            
        Returns:
            True if collection started successfully, False otherwise
        """
        try:
            if self.collecting:
                self.logger.log_monitoring_event("WARNING", "Process collection already running")
                return False
                
            self.logger.log_monitoring_event("INFO", f"Starting process collection (interval: {interval}s)")
            self.collecting = True
            self.stop_event.clear()
            
            # Start collection in separate thread
            self.collector_thread = threading.Thread(
                target=self._collection_loop,
                args=(interval, top_n, filter_pattern),
                daemon=True
            )
            self.collector_thread.start()
            
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to start process collection")
            return False
    
    def stop_collection(self) -> bool:
        """
        Stop process metrics collection.
        
        Returns:
            True if collection stopped successfully, False otherwise
        """
        try:
            if not self.collecting:
                return True
                
            self.logger.log_monitoring_event("INFO", "Stopping process collection")
            self.collecting = False
            self.stop_event.set()
            
            if self.collector_thread and self.collector_thread.is_alive():
                self.collector_thread.join(timeout=10)
                
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to stop process collection")
            return False
    
    def collect_process_snapshot(self, top_n: int = 10, 
                                filter_pattern: Optional[str] = None) -> List[Dict]:
        """
        Collect a snapshot of process metrics.
        
        Args:
            top_n: Number of top processes to return
            filter_pattern: Optional pattern to filter process names
            
        Returns:
            List of process dictionaries
        """
        try:
            processes = []
            current_time = time.time()
            
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 
                                           'memory_percent', 'memory_info', 'status', 'create_time']):
                try:
                    info = proc.info
                    
                    # Apply filter if specified
                    if filter_pattern and filter_pattern.lower() not in info['name'].lower():
                        continue
                    
                    # Get additional process information
                    try:
                        with proc.oneshot():
                            cpu_percent = proc.cpu_percent()
                            memory_info = proc.memory_info()
                            num_threads = proc.num_threads()
                            num_fds = proc.num_fds() if hasattr(proc, 'num_fds') else 0
                            io_counters = proc.io_counters()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                    
                    process_data = {
                        "timestamp": current_time,
                        "datetime": datetime.fromtimestamp(current_time).isoformat(),
                        "pid": info['pid'],
                        "name": info['name'],
                        "username": info['username'],
                        "status": info['status'],
                        "create_time": info['create_time'],
                        "cpu_percent": cpu_percent,
                        "memory_percent": info['memory_percent'],
                        "memory_rss": memory_info.rss,
                        "memory_vms": memory_info.vms,
                        "num_threads": num_threads,
                        "num_fds": num_fds,
                        "io_read_bytes": io_counters.read_bytes if io_counters else 0,
                        "io_write_bytes": io_counters.write_bytes if io_counters else 0,
                        "io_read_count": io_counters.read_count if io_counters else 0,
                        "io_write_count": io_counters.write_count if io_counters else 0
                    }
                    
                    processes.append(process_data)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage and return top N
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            return processes[:top_n]
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to collect process snapshot")
            return []
    
    def get_process_tree(self, pid: Optional[int] = None) -> Dict:
        """
        Get process tree structure.
        
        Args:
            pid: Root process ID (None for system root)
            
        Returns:
            Dictionary representing process tree
        """
        try:
            if pid is None:
                # Get system root processes
                root_processes = []
                for proc in psutil.process_iter(['pid', 'name', 'ppid']):
                    try:
                        info = proc.info
                        if info['ppid'] == 1:  # Init process children
                            root_processes.append({
                                "pid": info['pid'],
                                "name": info['name'],
                                "children": self._get_process_children(info['pid'])
                            })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                return {"root_processes": root_processes}
            else:
                # Get specific process tree
                try:
                    proc = psutil.Process(pid)
                    return {
                        "pid": proc.pid,
                        "name": proc.name(),
                        "children": self._get_process_children(pid)
                    }
                except psutil.NoSuchProcess:
                    return {"error": f"Process {pid} not found"}
                    
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to get process tree for PID {pid}")
            return {"error": str(e)}
    
    def monitor_specific_processes(self, process_names: List[str], 
                                 interval: int = 60) -> Dict:
        """
        Monitor specific processes by name.
        
        Args:
            process_names: List of process names to monitor
            interval: Monitoring interval in seconds
            
        Returns:
            Dictionary with process monitoring data
        """
        try:
            monitored_processes = {}
            current_time = time.time()
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    if info['name'] in process_names:
                        monitored_processes[info['name']] = {
                            "timestamp": current_time,
                            "datetime": datetime.fromtimestamp(current_time).isoformat(),
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
    
    def _collection_loop(self, interval: int, top_n: int, filter_pattern: Optional[str]):
        """Main collection loop."""
        while self.collecting and not self.stop_event.is_set():
            try:
                # Collect process metrics
                processes = self.collect_process_snapshot(top_n, filter_pattern)
                
                # Store metrics (this would integrate with storage module)
                # self.storage.store_process_metrics(processes)
                
                # Wait for next interval
                self.stop_event.wait(interval)
                
            except Exception as e:
                self.logger.log_error_with_context(e, "Error in process collection loop")
                time.sleep(5)  # Brief pause before retry
        
        self.collecting = False
    
    def _get_process_children(self, pid: int) -> List[Dict]:
        """Get children of a specific process."""
        try:
            children = []
            proc = psutil.Process(pid)
            
            for child in proc.children(recursive=False):
                try:
                    children.append({
                        "pid": child.pid,
                        "name": child.name(),
                        "children": self._get_process_children(child.pid)
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return children
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return []
    
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