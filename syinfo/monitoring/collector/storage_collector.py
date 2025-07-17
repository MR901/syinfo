"""
Storage metrics collection module.

This module provides comprehensive storage monitoring including
disk usage, I/O performance, and file system health checks.
"""

import os
import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading

from ..utils.logger import MonitoringLogger
from ..utils.config_manager import MonitoringConfig


class StorageCollector:
    """
    Storage metrics collector with comprehensive disk monitoring.
    
    Features:
    - Disk usage monitoring and analysis
    - I/O performance tracking and reporting
    - File system health checks and mount point analysis
    - Storage trend analysis and capacity planning
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize storage collector.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = MonitoringConfig(config_path)
        self.logger = MonitoringLogger()
        self.collecting = False
        self.collector_thread = None
        self.stop_event = threading.Event()
        
    def start_collection(self, interval: int = 60) -> bool:
        """
        Start continuous storage metrics collection.
        
        Args:
            interval: Collection interval in seconds
            
        Returns:
            True if collection started successfully, False otherwise
        """
        try:
            if self.collecting:
                self.logger.log_monitoring_event("WARNING", "Storage collection already running")
                return False
                
            self.logger.log_monitoring_event("INFO", f"Starting storage collection (interval: {interval}s)")
            self.collecting = True
            self.stop_event.clear()
            
            # Start collection in separate thread
            self.collector_thread = threading.Thread(
                target=self._collection_loop,
                args=(interval,),
                daemon=True
            )
            self.collector_thread.start()
            
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to start storage collection")
            return False
    
    def stop_collection(self) -> bool:
        """
        Stop storage metrics collection.
        
        Returns:
            True if collection stopped successfully, False otherwise
        """
        try:
            if not self.collecting:
                return True
                
            self.logger.log_monitoring_event("INFO", "Stopping storage collection")
            self.collecting = False
            self.stop_event.set()
            
            if self.collector_thread and self.collector_thread.is_alive():
                self.collector_thread.join(timeout=10)
                
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to stop storage collection")
            return False
    
    def collect_storage_snapshot(self) -> Dict:
        """
        Collect a snapshot of storage metrics.
        
        Returns:
            Dictionary containing current storage metrics
        """
        try:
            current_time = time.time()
            
            # Get disk partitions
            partitions = self._get_disk_partitions()
            
            # Get disk I/O statistics
            disk_io = psutil.disk_io_counters(perdisk=True)
            
            # Get overall disk usage
            root_usage = psutil.disk_usage('/')
            
            # Get disk I/O per partition
            partition_io = {}
            for partition in partitions:
                device = partition['device']
                if device in disk_io:
                    partition_io[device] = {
                        "read_bytes": disk_io[device].read_bytes,
                        "write_bytes": disk_io[device].write_bytes,
                        "read_count": disk_io[device].read_count,
                        "write_count": disk_io[device].write_count,
                        "read_time": disk_io[device].read_time,
                        "write_time": disk_io[device].write_time
                    }
            
            metrics = {
                "timestamp": current_time,
                "datetime": datetime.fromtimestamp(current_time).isoformat(),
                "root_usage": {
                    "total": root_usage.total,
                    "used": root_usage.used,
                    "free": root_usage.free,
                    "percent": root_usage.percent
                },
                "partitions": partitions,
                "partition_io": partition_io,
                "summary": self._calculate_storage_summary(partitions)
            }
            
            return metrics
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to collect storage snapshot")
            return {}
    
    def get_disk_usage(self, path: str = "/") -> Dict:
        """
        Get detailed disk usage for a specific path.
        
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
                "io_write_bytes": io_counters.write_bytes if io_counters else 0,
                "io_read_count": io_counters.read_count if io_counters else 0,
                "io_write_count": io_counters.write_count if io_counters else 0
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
                        "opts": partition.opts,
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
    
    def analyze_storage_trends(self, historical_data: List[Dict]) -> Dict:
        """
        Analyze storage usage trends.
        
        Args:
            historical_data: List of historical storage snapshots
            
        Returns:
            Dictionary with trend analysis results
        """
        try:
            if not historical_data:
                return {"error": "No historical data provided"}
            
            # Extract usage data over time
            usage_trends = []
            for snapshot in historical_data:
                if 'root_usage' in snapshot:
                    usage_trends.append({
                        "timestamp": snapshot['timestamp'],
                        "percent": snapshot['root_usage']['percent'],
                        "used": snapshot['root_usage']['used'],
                        "free": snapshot['root_usage']['free']
                    })
            
            if not usage_trends:
                return {"error": "No usage data found in historical data"}
            
            # Calculate trends
            trends = {
                "usage_growth_rate": self._calculate_growth_rate(usage_trends, 'percent'),
                "space_consumption_rate": self._calculate_growth_rate(usage_trends, 'used'),
                "free_space_decline_rate": self._calculate_growth_rate(usage_trends, 'free'),
                "projected_full_date": self._project_full_date(usage_trends),
                "recommendations": self._generate_storage_recommendations(usage_trends)
            }
            
            return trends
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to analyze storage trends")
            return {"error": str(e)}
    
    def _collection_loop(self, interval: int):
        """Main collection loop."""
        while self.collecting and not self.stop_event.is_set():
            try:
                # Collect storage metrics
                metrics = self.collect_storage_snapshot()
                
                # Store metrics (this would integrate with storage module)
                # self.storage.store_storage_metrics(metrics)
                
                # Check for alerts
                alerts = self._check_storage_alerts(metrics)
                if alerts:
                    self.logger.log_monitoring_event("ALERT", f"Storage alerts: {alerts}")
                
                # Wait for next interval
                self.stop_event.wait(interval)
                
            except Exception as e:
                self.logger.log_error_with_context(e, "Error in storage collection loop")
                time.sleep(5)  # Brief pause before retry
        
        self.collecting = False
    
    def _get_disk_partitions(self) -> List[Dict]:
        """Get disk partition information."""
        try:
            partitions = []
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    partitions.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "opts": partition.opts,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent
                    })
                except (OSError, PermissionError):
                    continue
            
            return partitions
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to get disk partitions")
            return []
    
    def _calculate_storage_summary(self, partitions: List[Dict]) -> Dict:
        """Calculate storage summary statistics."""
        try:
            total_space = 0
            total_used = 0
            total_free = 0
            critical_partitions = []
            
            for partition in partitions:
                total_space += partition['total']
                total_used += partition['used']
                total_free += partition['free']
                
                # Check for critical usage
                if partition['percent'] > 90:
                    critical_partitions.append({
                        "mountpoint": partition['mountpoint'],
                        "percent": partition['percent'],
                        "free": partition['free']
                    })
            
            return {
                "total_space": total_space,
                "total_used": total_used,
                "total_free": total_free,
                "overall_percent": (total_used / total_space * 100) if total_space > 0 else 0,
                "critical_partitions": critical_partitions,
                "partition_count": len(partitions)
            }
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to calculate storage summary")
            return {}
    
    def _calculate_growth_rate(self, usage_trends: List[Dict], metric: str) -> float:
        """Calculate growth rate for a specific metric."""
        try:
            if len(usage_trends) < 2:
                return 0.0
            
            # Calculate average daily growth rate
            first_value = usage_trends[0][metric]
            last_value = usage_trends[-1][metric]
            time_span = (usage_trends[-1]['timestamp'] - usage_trends[0]['timestamp']) / 86400  # days
            
            if time_span > 0:
                return (last_value - first_value) / time_span
            else:
                return 0.0
                
        except Exception:
            return 0.0
    
    def _project_full_date(self, usage_trends: List[Dict]) -> Optional[str]:
        """Project when storage will be full."""
        try:
            if len(usage_trends) < 2:
                return None
            
            # Calculate growth rate
            growth_rate = self._calculate_growth_rate(usage_trends, 'percent')
            
            if growth_rate <= 0:
                return None
            
            # Find current usage
            current_usage = usage_trends[-1]['percent']
            remaining_capacity = 100 - current_usage
            
            if remaining_capacity <= 0:
                return "Already full"
            
            # Calculate days until full
            days_until_full = remaining_capacity / growth_rate
            
            if days_until_full > 0:
                projected_date = datetime.now() + timedelta(days=days_until_full)
                return projected_date.isoformat()
            else:
                return None
                
        except Exception:
            return None
    
    def _generate_storage_recommendations(self, usage_trends: List[Dict]) -> List[str]:
        """Generate storage recommendations."""
        recommendations = []
        
        try:
            current_usage = usage_trends[-1]['percent']
            growth_rate = self._calculate_growth_rate(usage_trends, 'percent')
            
            if current_usage > 90:
                recommendations.append("CRITICAL: Storage is nearly full. Immediate action required.")
            elif current_usage > 80:
                recommendations.append("WARNING: Storage usage is high. Consider cleanup or expansion.")
            
            if growth_rate > 5:  # More than 5% per day
                recommendations.append("High storage growth rate detected. Monitor for unusual activity.")
            
            if growth_rate > 0:
                days_until_full = (100 - current_usage) / growth_rate
                if days_until_full < 30:
                    recommendations.append(f"Storage will be full in approximately {days_until_full:.1f} days.")
            
            if not recommendations:
                recommendations.append("Storage usage is normal.")
                
        except Exception:
            recommendations.append("Unable to generate recommendations due to insufficient data.")
        
        return recommendations
    
    def _check_storage_alerts(self, metrics: Dict) -> List[str]:
        """Check for storage alerts."""
        alerts = []
        
        try:
            if 'root_usage' in metrics:
                usage = metrics['root_usage']['percent']
                if usage > 95:
                    alerts.append(f"CRITICAL: Root filesystem {usage:.1f}% full")
                elif usage > 90:
                    alerts.append(f"WARNING: Root filesystem {usage:.1f}% full")
            
            if 'summary' in metrics and 'critical_partitions' in metrics['summary']:
                for partition in metrics['summary']['critical_partitions']:
                    alerts.append(f"CRITICAL: {partition['mountpoint']} {partition['percent']:.1f}% full")
                    
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to check storage alerts")
        
        return alerts
    
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