#!/usr/bin/env python3
"""
SyInfo Monitoring Examples

This example demonstrates how to use SyInfo's monitoring capabilities
both programmatically and through the CLI interface.

License: MIT
"""

import json
import time
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import syinfo


def basic_monitoring_example():
    """Demonstrate basic monitoring functionality."""
    print("=" * 60)
    print("SyInfo - Basic Monitoring Example")
    print("=" * 60)

    print("Creating a monitor with 2-second intervals...")
    monitor = syinfo.create_simple_monitor(interval=2)
    
    print("Starting monitoring for 10 seconds...")
    monitor.start(duration=10)
    
    # Wait for monitoring to complete
    time.sleep(11)
    
    # Get results
    if monitor.is_running:
        results = monitor.stop()
    else:
        # Monitoring completed automatically
        results = {
            "total_points": len(monitor.data_points),
            "data_points": monitor.data_points,
            "summary": monitor._calculate_summary() if monitor.data_points else {}
        }
    
    print(f"\nMonitoring Results:")
    print(f"- Data Points Collected: {results['total_points']}")
    print(f"- Average CPU Usage: {results.get('summary', {}).get('cpu_avg', 0):.1f}%")
    print(f"- Peak Memory Usage: {results.get('summary', {}).get('memory_peak', 0):.1f}%")
    print(f"- Disk Usage: {results.get('summary', {}).get('disk_avg', 0):.1f}%")
    
    return results


def advanced_monitoring_example():
    """Demonstrate advanced monitoring with callback and analysis."""
    print("\n" + "=" * 60)
    print("SyInfo - Advanced Monitoring Example")
    print("=" * 60)

    # Storage for high CPU events
    high_cpu_events = []
    
    def cpu_callback(data_point):
        """Callback to detect high CPU usage in real-time."""
        cpu_usage = data_point.get('cpu_percent', 0)
        if cpu_usage > 5:  # Lowered threshold for demo
            event = {
                'timestamp': data_point['timestamp'],
                'cpu_percent': cpu_usage,
                'memory_percent': data_point.get('memory_percent', 0)
            }
            high_cpu_events.append(event)
            print(f"  WARNING: High CPU detected: {cpu_usage:.1f}% at {data_point['timestamp']}")
    
    print("Starting advanced monitoring with real-time CPU detection...")
    monitor = syinfo.create_simple_monitor(interval=1)
    
    # Start monitoring with callback
    monitor.start(duration=8, callback=cpu_callback)
    
    # Let it run
    time.sleep(9)
    
    # Get results
    if monitor.is_running:
        results = monitor.stop()
    else:
        results = {
            "total_points": len(monitor.data_points),
            "data_points": monitor.data_points,
            "summary": monitor._calculate_summary() if monitor.data_points else {}
        }
    
    print(f"\nAdvanced Monitoring Results:")
    print(f"- Total Data Points: {results['total_points']}")
    print(f"- High CPU Events Detected: {len(high_cpu_events)}")
    
    if results.get('summary'):
        summary = results['summary']
        print(f"- Duration: {summary.get('duration_seconds', 0)} seconds")
        print(f"- CPU Average: {summary.get('cpu_avg', 0):.1f}%")
        print(f"- CPU Maximum: {summary.get('cpu_max', 0):.1f}%")
        print(f"- Memory Average: {summary.get('memory_avg', 0):.1f}%")
    
    return results, high_cpu_events


def data_analysis_example():
    """Demonstrate monitoring data analysis."""
    print("\n" + "=" * 60)
    print("SyInfo - Data Analysis Example")
    print("=" * 60)

    print("Collecting monitoring data for analysis...")
    monitor = syinfo.create_simple_monitor(interval=1)
    monitor.start(duration=6)
    
    time.sleep(7)
    
    if monitor.is_running:
        results = monitor.stop()
    else:
        results = {
            "total_points": len(monitor.data_points),
            "data_points": monitor.data_points,
            "summary": monitor._calculate_summary() if monitor.data_points else {}
        }
    
    data_points = results.get('data_points', [])
    
    if not data_points:
        print("No data points collected.")
        return
    
    print(f"\nAnalyzing {len(data_points)} data points...")
    
    # CPU analysis
    cpu_values = [dp.get('cpu_percent', 0) for dp in data_points]
    cpu_trend = "increasing" if cpu_values[-1] > cpu_values[0] else "decreasing"
    
    # Memory analysis  
    memory_values = [dp.get('memory_percent', 0) for dp in data_points]
    memory_stable = max(memory_values) - min(memory_values) < 2  # Within 2%
    
    # Network analysis
    network_active = any(
        dp.get('network_io', {}).get('bytes_sent', 0) > 0 
        for dp in data_points
    )
    
    print(f"\nAnalysis Results:")
    print(f"- CPU Trend: {cpu_trend}")
    print(f"- Memory Stable: {'Yes' if memory_stable else 'No'}")
    print(f"- Network Activity: {'Yes' if network_active else 'No'}")
    
    # Find peak usage time
    if cpu_values:
        peak_cpu_idx = cpu_values.index(max(cpu_values))
        peak_time = data_points[peak_cpu_idx].get('timestamp', 'Unknown')
        print(f"- Peak CPU Time: {peak_time}")
        print(f"- Peak CPU Value: {max(cpu_values):.1f}%")


def export_monitoring_data_example():
    """Demonstrate exporting monitoring data to various formats."""
    print("\n" + "=" * 60)
    print("SyInfo - Data Export Example")
    print("=" * 60)

    print("Collecting monitoring data for export...")
    monitor = syinfo.create_simple_monitor(interval=2)
    monitor.start(duration=6)
    
    time.sleep(7)
    
    if monitor.is_running:
        results = monitor.stop()
    else:
        results = {
            "total_points": len(monitor.data_points),
            "data_points": monitor.data_points,
            "summary": monitor._calculate_summary() if monitor.data_points else {}
        }
    
    # Export to JSON
    json_file = "monitoring_results.json"
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Exported monitoring data to {json_file}")
    
    # Create CSV-like summary
    csv_file = "monitoring_summary.csv"
    with open(csv_file, 'w') as f:
        f.write("timestamp,cpu_percent,memory_percent,disk_percent\n")
        for dp in results.get('data_points', []):
            f.write(f"{dp.get('timestamp', '')},{dp.get('cpu_percent', 0)},{dp.get('memory_percent', 0)},{dp.get('disk_percent', 0)}\n")
    print(f"Exported CSV summary to {csv_file}")
    
    # Create human-readable report
    report_file = "monitoring_report.txt"
    with open(report_file, 'w') as f:
        f.write("SyInfo Monitoring Report\n")
        f.write("=" * 25 + "\n\n")
        
        summary = results.get('summary', {})
        f.write(f"Duration: {summary.get('duration_seconds', 0)} seconds\n")
        f.write(f"Data Points: {results.get('total_points', 0)}\n")
        f.write(f"CPU Average: {summary.get('cpu_avg', 0):.1f}%\n")
        f.write(f"CPU Maximum: {summary.get('cpu_max', 0):.1f}%\n")
        f.write(f"Memory Average: {summary.get('memory_avg', 0):.1f}%\n")
        f.write(f"Memory Peak: {summary.get('memory_peak', 0):.1f}%\n")
        f.write(f"Disk Usage: {summary.get('disk_avg', 0):.1f}%\n")
    
    print(f"Exported human-readable report to {report_file}")
    
    return results


def cli_monitoring_examples():
    """Demonstrate CLI-based monitoring."""
    print("\n" + "=" * 60)
    print("SyInfo - CLI Monitoring Examples")
    print("=" * 60)

    import subprocess
    
    print("1. Basic CLI monitoring:")
    try:
        result = subprocess.run(
            ["python", "-m", "syinfo", "-m", "-t", "8", "-i", "2"],
            capture_output=True,
            text=True,
            timeout=15
        )
        print("   Basic monitoring completed")
    except subprocess.TimeoutExpired:
        print("   Monitoring timed out (expected)")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n2. JSON CLI monitoring:")
    try:
        result = subprocess.run(
            ["python", "-m", "syinfo", "-mpj", "-t", "6", "-i", "2"],
            capture_output=True,
            text=True,
            timeout=12
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            json_line = lines[-1]  # Last line should be JSON
            try:
                data = json.loads(json_line)
                print(f"   JSON monitoring completed")
                print(f"   - Data points: {data.get('total_points', 0)}")
                print(f"   - CPU average: {data.get('summary', {}).get('cpu_avg', 0):.1f}%")
            except json.JSONDecodeError:
                print("   JSON parsing failed")
        else:
            print(f"   Command failed with code {result.returncode}")
    except subprocess.TimeoutExpired:
        print("   JSON monitoring timed out")
    except Exception as e:
        print(f"   Error: {e}")


def main():
    """Run all monitoring examples."""
    print("SyInfo Monitoring Examples")
    print("=" * 26)
    print("This script demonstrates comprehensive monitoring capabilities")
    print("including real-time tracking, data analysis, and export features.\n")
    
    try:
        # Basic monitoring
        basic_results = basic_monitoring_example()
        
        # Advanced monitoring with callbacks
        advanced_results, cpu_events = advanced_monitoring_example()
        
        # Data analysis
        data_analysis_example()
        
        # Data export
        export_results = export_monitoring_data_example()
        
        # CLI examples
        cli_monitoring_examples()
        
        print("\n" + "=" * 60)
        print("All monitoring examples completed successfully!")
        print("\nGenerated files:")
        print("  - monitoring_results.json")
        print("  - monitoring_summary.csv") 
        print("  - monitoring_report.txt")
        print("\nKey takeaways:")
        print("  - Use create_simple_monitor() for programmatic monitoring")
        print("  - CLI monitoring with -m flag provides JSON output")
        print("  - Real-time callbacks enable event detection")
        print("  - Data can be exported in multiple formats")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\nMonitoring examples interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError running monitoring examples: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
