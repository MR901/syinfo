"""Monitoring example using SystemMonitor via public API."""

import json
import time

from syinfo import SystemMonitor


def main():
    monitor = SystemMonitor(interval=2, keep_in_memory=True)
    monitor.start(duration=6)
    time.sleep(7)
    results = monitor.stop() if monitor.is_running else {
        "total_points": len(monitor.data_points),
        "data_points": monitor.data_points,
    }
    print(json.dumps(results, default=str))


if __name__ == "__main__":
    main()


