#!/usr/bin/env python3
"""
Monitoring Example

This example demonstrates how to use SyInfo's monitoring features
for real-time system and process monitoring.
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from syinfo.monitoring.core import SystemMonitor, ProcessMonitor
    from syinfo.monitoring.data import DataCollector, DataAnalyzer
    from syinfo.monitoring.utils import MonitoringConfig
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False
    print("Warning: Monitoring features not available. Install required dependencies.")


def basic_monitoring_example():
    """Demonstrate basic monitoring functionality."""
    if not MONITORING_AVAILABLE:
        print("Monitoring features not available. Skipping monitoring example.")
        return
    
    print("=" * 60)
    print("SyInfo - Monitoring Example")
    print("=" * 60)
    
    # 1. System Monitoring
    print("\n1. System Monitoring:")
    print("-" * 30)
    
    # Create system monitor
    system_monitor = SystemMonitor()
    
    # Collect a single snapshot
    print("Collecting system snapshot...")
    snapshot = system_monitor._collect_system_stats()
    
    print(f"Timestamp: {snapshot['datetime']}")
    print(f"CPU Usage: {snapshot['cpu']['percent']}%")
    print(f"Memory Usage: {snapshot['memory']['percent']}%")
    print(f"Disk Usage: {snapshot['disk']['percent']}%")
    print(f"Network Bytes Sent: {snapshot['network']['bytes_sent']}")
    print(f"Network Bytes Received: {snapshot['network']['bytes_recv']}")
    
    # 2. Process Monitoring
    print("\n2. Process Monitoring:")
    print("-" * 30)
    
    # Create process monitor
    process_monitor = ProcessMonitor()
    
    # Get top processes by memory usage
    print("Top 5 processes by memory usage:")
    top_processes = process_monitor.get_process_tree(
        sort_by="memory", 
        top_n=5
    )
    
    for i, proc in enumerate(top_processes, 1):
        print(f"{i}. {proc['name']} (PID: {proc['pid']})")
        print(f"   Memory: {proc['memory_percent']:.1f}% | CPU: {proc['cpu_percent']:.1f}%")
        print(f"   Command: {proc['command'][:50]}...")
    
    # 3. Data Collection
    print("\n3. Data Collection:")
    print("-" * 30)
    
    # Create data collector
    collector = DataCollector(output_dir="./monitoring_data")
    
    # Collect system data
    print("Collecting system data...")
    system_data = collector.collect_system_data()
    print(f"Collected {len(system_data)} system metrics")
    
    # Collect process data
    print("Collecting process data...")
    process_data = collector.collect_process_data(top_n=10)
    print(f"Collected data for {len(process_data)} processes")
    
    # Save data to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    system_file = f"./monitoring_data/system_{timestamp}.json"
    process_file = f"./monitoring_data/process_{timestamp}.json"
    
    with open(system_file, 'w') as f:
        json.dump(system_data, f, indent=2)
    
    with open(process_file, 'w') as f:
        json.dump(process_data, f, indent=2)
    
    print(f"Data saved to:")
    print(f"  System: {system_file}")
    print(f"  Process: {process_file}")
    
    # 4. Data Analysis
    print("\n4. Data Analysis:")
    print("-" * 30)
    
    # Create data analyzer
    analyzer = DataAnalyzer()
    
    # Analyze system performance
    system_analysis = analyzer.analyze_system_performance(system_data)
    print("System Performance Analysis:")
    print(f"  Average CPU Usage: {system_analysis['avg_cpu']:.1f}%")
    print(f"  Peak CPU Usage: {system_analysis['peak_cpu']:.1f}%")
    print(f"  Average Memory Usage: {system_analysis['avg_memory']:.1f}%")
    print(f"  Peak Memory Usage: {system_analysis['peak_memory']:.1f}%")
    
    # Analyze process performance
    process_analysis = analyzer.analyze_process_performance(process_data)
    print("\nProcess Performance Analysis:")
    print(f"  Total Processes: {process_analysis['total_processes']}")
    print(f"  High CPU Processes: {process_analysis['high_cpu_processes']}")
    print(f"  High Memory Processes: {process_analysis['high_memory_processes']}")
    
    print("\n" + "=" * 60)
    print("Monitoring example completed successfully!")
    print("=" * 60)


def continuous_monitoring_example():
    """Demonstrate continuous monitoring with configurable intervals."""
    if not MONITORING_AVAILABLE:
        print("Monitoring features not available. Skipping continuous monitoring.")
        return
    
    print("\n" + "=" * 60)
    print("Continuous Monitoring Example")
    print("=" * 60)
    
    # Create system monitor with custom configuration
    config = {
        'monitoring': {
            'system': {
                'enabled': True,
                'interval': 5  # 5 seconds
            },
            'process': {
                'enabled': True,
                'interval': 10  # 10 seconds
            }
        }
    }
    
    system_monitor = SystemMonitor()
    
    print("Starting continuous monitoring for 30 seconds...")
    print("Press Ctrl+C to stop early")
    
    try:
        # Start monitoring for 30 seconds
        system_monitor.start_monitoring(interval=5, duration=30)
        
        # Monitor for 30 seconds
        time.sleep(30)
        
        # Stop monitoring
        system_monitor.stop_monitoring()
        print("Continuous monitoring completed!")
        
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
        system_monitor.stop_monitoring()


def main():
    """Run all monitoring examples."""
    basic_monitoring_example()
    
    # Uncomment to run continuous monitoring
    # continuous_monitoring_example()


if __name__ == "__main__":
    main() 