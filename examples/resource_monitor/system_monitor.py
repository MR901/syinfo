"""Resource monitor example: SystemMonitor minimal demo."""

import json
import time

from syinfo import SystemMonitor


def main() -> None:
    monitor = SystemMonitor(interval=2, keep_in_memory=True)
    monitor.start()
    try:
        time.sleep(6)
        results = monitor.stop()
    except KeyboardInterrupt:
        results = monitor.stop() if monitor.is_running else {
            "total_points": 0,
            "data_points": [],
        }

    print(json.dumps(results, default=str))


if __name__ == "__main__":
    main()



