#!/usr/bin/env python3
"""
Simple Monitoring Example

Demonstrates the simplified monitoring capabilities of SyInfo.
"""

import sys
import time
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import syinfo


def main():
    """Demonstrate simple monitoring functionality."""
    print("=" * 60)
    print("SyInfo - Simple Monitoring Example")
    print("=" * 60)

    # Create a simple monitor
    print("\n1. Creating Simple Monitor")
    print("-" * 30)

    monitor = syinfo.create_simple_monitor(interval=2)  # 2 second intervals
    print("Monitor created with 2-second intervals")

    # Start monitoring for a short duration
    print("\n2. Starting Monitoring (10 seconds)")
    print("-" * 30)
    print("Monitoring system for 10 seconds...")

    monitor.start(duration=10)

    # Wait for monitoring to complete
    time.sleep(11)  # Wait a bit longer than monitoring duration

    # Get results
    results = monitor.stop()

    # Display results
    print("\n3. Monitoring Results")
    print("-" * 30)

    if "summary" in results:
        summary = results["summary"]
        print(f"Duration: {summary.get('duration_seconds', 0)} seconds")
        print(f"Average CPU Usage: {summary.get('cpu_avg', 0):.1f}%")
        print(f"Peak CPU Usage: {summary.get('cpu_max', 0):.1f}%")
        print(f"Average Memory Usage: {summary.get('memory_avg', 0):.1f}%")
        print(f"Peak Memory Usage: {summary.get('memory_peak', 0):.1f}%")
        print(f"Data Points Collected: {results.get('total_points', 0)}")
    else:
        print(f"Monitoring results: {results}")

    print("\n" + "=" * 60)
    print("Simple monitoring example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
