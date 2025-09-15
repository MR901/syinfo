"""System monitor with optional on-disk persistence and rotation.

Crash-safe persistence: when output_path is set, each data point is appended
as one JSON object per line (JSONL). Optional rotation by lines/bytes.
"""

import json
import os
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import psutil

from syinfo.exceptions import DataCollectionError


class SystemMonitor:
    """Simple system monitoring with optional on-disk persistence.

    If ``output_path`` is provided, each data point is appended to a JSONL file
    (one JSON object per line). Basic rotation can be enabled by lines or bytes.
    """

    def __init__(
        self,
        interval: int = 60,
        output_path: Optional[str] = None,
        rotate_max_lines: Optional[int] = None,
        rotate_max_bytes: Optional[int] = None,
        keep_in_memory: bool = True,
        summary_on_stop: bool = True,
    ):
        """Initialize monitor.

        Args:
            interval: Monitoring interval in seconds
            output_path: Optional path (file or directory) to persist data (JSONL)
            rotate_max_lines: Rotate file after this many lines (optional)
            rotate_max_bytes: Rotate file after this many bytes (optional)
            keep_in_memory: Keep collected data points in memory (default True)
            summary_on_stop: Write summary JSON on stop (when output_path is set)
        """
        self.interval = interval
        self.is_running = False
        self.data_points: List[Dict[str, Any]] = []
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # Persistence configuration
        self._output_path = Path(output_path) if output_path else None
        self._resolved_output_path: Optional[Path] = None
        self._rotate_max_lines = rotate_max_lines
        self._rotate_max_bytes = rotate_max_bytes
        self._keep_in_memory = keep_in_memory
        self._summary_on_stop = summary_on_stop
        self._log_fp: Optional[Any] = None
        self._lines_written = 0
        self._bytes_written = 0

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

        # Prepare persistence
        if self._output_path:
            self._prepare_output()

        def monitor_loop() -> None:
            start_time = time.time()

            while not self._stop_event.is_set():
                try:
                    # Collect data point
                    data_point = self._collect_data_point()
                    if self._keep_in_memory:
                        self.data_points.append(data_point)

                    # Persist to disk for crash-safety
                    if self._log_fp:
                        self._write_jsonl(data_point)

                    # Callback
                    if callback:
                        callback(data_point)

                    # Duration check
                    if duration and (time.time() - start_time) >= duration:
                        break

                    # Sleep until next interval
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

        # Write summary next to JSONL file
        if self._summary_on_stop and self._resolved_output_path:
            try:
                summary_path = self._resolved_output_path.with_suffix(".summary.json")
                with open(summary_path, "w", encoding="utf-8") as sfp:
                    json.dump(summary, sfp, ensure_ascii=False, indent=2, default=str)
            except Exception:
                pass

        # Close file handle
        try:
            if self._log_fp:
                self._log_fp.flush()
                self._log_fp.close()
        finally:
            self._log_fp = None

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

        cpu_values = [dp["cpu_percent"] for dp in self.data_points]
        memory_values = [dp["memory_percent"] for dp in self.data_points]
        disk_values = [dp["disk_percent"] for dp in self.data_points]

        return {
            "duration_seconds": len(self.data_points) * self.interval,
            "cpu_avg": sum(cpu_values) / len(cpu_values) if cpu_values else 0.0,
            "cpu_max": max(cpu_values) if cpu_values else 0.0,
            "memory_avg": sum(memory_values) / len(memory_values) if memory_values else 0.0,
            "memory_peak": max(memory_values) if memory_values else 0.0,
            "disk_avg": sum(disk_values) / len(disk_values) if disk_values else 0.0,
            "start_time": self.data_points[0]["timestamp"] if self.data_points else None,
            "end_time": self.data_points[-1]["timestamp"] if self.data_points else None,
        }

    # ----------------------------
    # Persistence helpers
    # ----------------------------
    def _prepare_output(self) -> None:
        assert self._output_path is not None
        path = self._output_path
        if path.exists() and path.is_dir():
            fname = f"monitor-{datetime.now().strftime('%Y%m%d-%H%M%S')}.jsonl"
            self._resolved_output_path = path / fname
        else:
            parent = path.parent if path.suffix else path
            parent.mkdir(parents=True, exist_ok=True)
            if path.suffix:
                self._resolved_output_path = path
            else:
                fname = f"monitor-{datetime.now().strftime('%Y%m%d-%H%M%S')}.jsonl"
                self._resolved_output_path = parent / fname

        self._log_fp = open(self._resolved_output_path, "a", encoding="utf-8")
        try:
            self._bytes_written = self._resolved_output_path.stat().st_size
        except Exception:
            self._bytes_written = 0
        self._lines_written = 0

    def _write_jsonl(self, data_point: Dict[str, Any]) -> None:
        if not self._log_fp or not self._resolved_output_path:
            return
        try:
            line = json.dumps(data_point, ensure_ascii=False, default=str)
        except Exception:
            safe_dp = {k: (str(v) if not isinstance(v, (str, int, float, bool, type(None), dict, list)) else v) for k, v in data_point.items()}
            line = json.dumps(safe_dp, ensure_ascii=False)
        self._log_fp.write(line + "\n")
        self._log_fp.flush()
        self._lines_written += 1
        self._bytes_written += len(line) + 1
        self._maybe_rotate()

    def _maybe_rotate(self) -> None:
        if not self._resolved_output_path or not self._log_fp:
            return
        by_lines = self._rotate_max_lines is not None and self._lines_written >= int(self._rotate_max_lines)
        by_bytes = self._rotate_max_bytes is not None and self._bytes_written >= int(self._rotate_max_bytes)
        if not (by_lines or by_bytes):
            return
        try:
            self._log_fp.flush()
            self._log_fp.close()
        except Exception:
            pass
        finally:
            self._log_fp = None

        ts_suffix = datetime.now().strftime("%Y%m%d-%H%M%S")
        rotated = self._resolved_output_path.with_name(
            self._resolved_output_path.stem + f".{ts_suffix}" + self._resolved_output_path.suffix
        )
        try:
            os.replace(self._resolved_output_path, rotated)
        except Exception:
            try:
                self._resolved_output_path.rename(rotated)
            except Exception:
                pass
        self._log_fp = open(self._resolved_output_path, "a", encoding="utf-8")
        self._lines_written = 0
        self._bytes_written = 0


def create_system_monitor(
    interval: int = 60,
    output_path: Optional[str] = None,
    rotate_max_lines: Optional[int] = None,
    rotate_max_bytes: Optional[int] = None,
    keep_in_memory: bool = True,
    summary_on_stop: bool = True,
) -> SystemMonitor:
    """Create a system monitor instance."""
    return SystemMonitor(
        interval=interval,
        output_path=output_path,
        rotate_max_lines=rotate_max_lines,
        rotate_max_bytes=rotate_max_bytes,
        keep_in_memory=keep_in_memory,
        summary_on_stop=summary_on_stop,
    )


__all__ = ["SystemMonitor", "create_system_monitor"]


