"""Monitoring example using SystemMonitor via public API."""

import json
import time

import syinfo as si


def main():
    monitor = si.create_system_monitor(interval=2, output_path="./monitoring", rotate_max_lines=5)
    monitor.start(duration=6)
    time.sleep(7)
    results = monitor.stop() if monitor.is_running else {
        "total_points": len(monitor.data_points),
        "data_points": monitor.data_points,
        "summary": monitor._calculate_summary() if monitor.data_points else {},
    }
    print(json.dumps(results, default=str))


if __name__ == "__main__":
    main()


