#!/usr/bin/env python3
"""Example: Process monitoring with string-based filtering.

This example demonstrates how to use ProcessMonitor to monitor specific
processes based on string matching in their name, command line, or executable path.
"""

import time
import syinfo
from syinfo.resource_monitor.process_monitoring import ProcessMonitor


def example_monitor_python_processes():
    """Monitor all Python processes for 30 seconds."""
    print("🐍 Monitoring Python processes for 30 seconds...")
    print("=" * 60)
    
    # Create monitor for Python processes
    monitor = ProcessMonitor(
        filters=["python"],  # Match processes containing "python"
        match_fields=["name", "cmdline"],  # Check both process name and command line
        case_sensitive=False,  # Case insensitive matching
        interval=5,  # Check every 5 seconds
        include_children=True,  # Include child process info
    )
    
    def print_callback(data_point):
        """Callback to print real-time data."""
        count = data_point['process_count']
        total_cpu = data_point['total_cpu_percent']
        total_mem = data_point['total_memory_human']
        print(f"  Found {count} Python processes - CPU: {total_cpu:.1f}% - Memory: {total_mem}")
    
    try:
        monitor.start(duration=30, callback=print_callback)
        
        # Wait for monitoring to complete
        while monitor.is_running:
            time.sleep(1)
            
        # Get results with summary
        results = monitor.stop(print_summary=True)
        print(f"\nCollected {results['total_points']} data points")
        
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        monitor.stop()


def example_monitor_with_regex():
    """Monitor processes using regex patterns."""
    print("\n🔍 Monitoring processes with regex (browser-related) for 20 seconds...")
    print("=" * 60)
    
    # Monitor browser processes using regex
    monitor = ProcessMonitor(
        filters=[r"(firefox|chrome|chromium|safari|edge)"],
        use_regex=True,
        match_fields=["name", "exe"],
        interval=3,
    )
    
    def print_callback(data_point):
        """Callback to print browser process info."""
        processes = data_point.get('processes', [])
        if processes:
            print(f"  Browser processes active:")
            for proc in processes[:3]:  # Show top 3
                name = proc.get('name', 'unknown')
                cpu = proc.get('cpu_percent', 0)
                mem = proc.get('memory_rss_human', '0 B')
                print(f"    - {name} (PID {proc.get('pid')}): CPU {cpu:.1f}%, Memory {mem}")
        else:
            print("  No browser processes found")
    
    try:
        monitor.start(duration=20, callback=print_callback)
        
        while monitor.is_running:
            time.sleep(1)
            
        results = monitor.stop(print_summary=True)
        
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        monitor.stop()


def example_monitor_with_persistence():
    """Monitor processes with file persistence."""
    print("\n💾 Monitoring system processes with file persistence...")
    print("=" * 60)
    
    # Monitor system processes and save to file
    monitor = ProcessMonitor(
        filters=["systemd", "kernel", "kthread"],
        match_fields=["name"],
        interval=2,
        output_path="./process_monitor_data",  # Will create timestamped file
        rotate_max_lines=50,  # Rotate after 50 lines
    )
    
    try:
        print("Starting 15-second monitoring with file persistence...")
        monitor.start(duration=15)
        
        while monitor.is_running:
            time.sleep(1)
            
        results = monitor.stop(print_summary=True, save_plot_to="./plots/")
        
        if results.get('plot_path'):
            print(f"📊 Plot saved to: {results['plot_path']}")
            
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        monitor.stop()


def example_convenience_function():
    """Use the convenience function from syinfo module."""
    print("\n🚀 Using convenience function from syinfo...")
    print("=" * 60)
    
    # Use the top-level convenience function
    monitor = syinfo.create_process_monitor(
        filters=["bash", "zsh", "sh"],
        interval=3,
    )
    
    print("Monitoring shell processes for 10 seconds...")
    
    try:
        monitor.start(duration=10)
        
        while monitor.is_running:
            time.sleep(1)
            
        results = monitor.stop(print_summary=True)
        
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        monitor.stop()


if __name__ == "__main__":
    print("🔍 SyInfo Process Monitor Examples")
    print("=" * 60)
    
    try:
        # Run examples
        example_monitor_python_processes()
        example_monitor_with_regex()
        example_monitor_with_persistence()
        example_convenience_function()
        
        print("\n✅ All examples completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
