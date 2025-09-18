"""SyInfo Simple Monitoring - Optional lightweight monitoring

Simple monitoring capabilities without over-engineering.
Only include if monitoring features are actually needed.
"""

import threading
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import psutil

from .exceptions import DataCollectionError


class SimpleMonitor:
    """Simple system monitoring with basic functionality."""

    def __init__(self, interval: int = 60):
        """Initialize monitor.

        Args:
            interval: Monitoring interval in seconds
        """
        self.interval = interval
        self.is_running = False
        self.data_points: List[Dict[str, Any]] = []
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def start(
        self,
        duration: Optional[int] = None,
        callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> None:
        """Start monitoring.

        Args:
            duration: Duration in seconds (None for infinite)
            callback: Optional callback for each data point
        """
        if self.is_running:
            raise DataCollectionError("Monitoring is already running")

        self.is_running = True
        self._stop_event.clear()
        self.data_points = []

        def monitor_loop():
            start_time = time.time()

            while not self._stop_event.is_set():
                try:
                    # Collect data point
                    data_point = self._collect_data_point()
                    self.data_points.append(data_point)

                    # Call callback if provided
                    if callback:
                        callback(data_point)

                    # Check duration
                    if duration and (time.time() - start_time) >= duration:
                        break

                    # Wait for next interval
                    self._stop_event.wait(self.interval)

                except Exception as e:
                    print(f"Monitoring error: {e}")
                    continue

            self.is_running = False

        self._thread = threading.Thread(target=monitor_loop, daemon=True)
        self._thread.start()

    def stop(self) -> Dict[str, Any]:
        """Stop monitoring and return collected data.

        Returns:
            Dictionary with monitoring results
        """
        if not self.is_running:
            return {"error": "Monitoring is not running"}

        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)

        # Calculate summary statistics
        if self.data_points:
            summary = self._calculate_summary()
        else:
            summary = {"error": "No data points collected"}

        return {
            "summary": summary,
            "data_points": self.data_points,
            "total_points": len(self.data_points),
        }

    def _collect_data_point(self) -> Dict[str, Any]:
        """Collect a single data point."""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent,
            "network_io": dict(psutil.net_io_counters()._asdict()),
        }

    def _calculate_summary(self) -> Dict[str, Any]:
        """Calculate summary statistics from collected data."""
        if not self.data_points:
            return {}

        # Extract metrics
        cpu_values = [dp["cpu_percent"] for dp in self.data_points]
        memory_values = [dp["memory_percent"] for dp in self.data_points]
        disk_values = [dp["disk_percent"] for dp in self.data_points]

        return {
            "duration_seconds": len(self.data_points) * self.interval,
            "cpu_avg": sum(cpu_values) / len(cpu_values),
            "cpu_max": max(cpu_values),
            "memory_avg": sum(memory_values) / len(memory_values),
            "memory_peak": max(memory_values),
            "disk_avg": sum(disk_values) / len(disk_values),
            "start_time": self.data_points[0]["timestamp"],
            "end_time": self.data_points[-1]["timestamp"],
        }


def create_simple_monitor(interval: int = 60) -> SimpleMonitor:
    """Create a simple monitor instance.

    Args:
        interval: Monitoring interval in seconds

    Returns:
        SimpleMonitor instance
    """
    return SimpleMonitor(interval=interval)


__all__ = ["SimpleMonitor", "create_simple_monitor"]
