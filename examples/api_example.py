#!/usr/bin/env python3
"""
API Examples

This example demonstrates how to use SyInfo's API features
for programmatic access to system information and monitoring data.
"""

import sys
import json
import time
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from syinfo.api import info_api, monitoring_api, analysis_api


def info_api_example():
    """Demonstrate Info API usage."""
    print("=" * 60)
    print("SyInfo - Info API Example")
    print("=" * 60)
    
    # 1. System Information API
    print("\n1. System Information API:")
    print("-" * 30)
    
    # Get basic system info
    try:
        system_info = info_api.get_system_info()
        print("System Information:")
        print(f"  OS: {system_info['os']}")
        print(f"  Kernel: {system_info['kernel']}")
        print(f"  Architecture: {system_info['architecture']}")
        print(f"  Hostname: {system_info['hostname']}")
        print(f"  Uptime: {system_info['uptime']}")
    except Exception as e:
        print(f"Error getting system info: {e}")
    
    # Get detailed system info
    try:
        detailed_info = info_api.get_detailed_system_info()
        print(f"\nDetailed System Information:")
        print(f"  CPU Cores: {detailed_info['cpu']['cores']}")
        print(f"  CPU Model: {detailed_info['cpu']['model']}")
        print(f"  Total Memory: {detailed_info['memory']['total']}")
        print(f"  Available Memory: {detailed_info['memory']['available']}")
        print(f"  Disk Total: {detailed_info['disk']['total']}")
        print(f"  Disk Free: {detailed_info['disk']['free']}")
    except Exception as e:
        print(f"Error getting detailed system info: {e}")
    
    # 2. Device Information API
    print("\n2. Device Information API:")
    print("-" * 30)
    
    # Get CPU information
    try:
        cpu_info = info_api.get_cpu_info()
        print("CPU Information:")
        print(f"  Model: {cpu_info['model']}")
        print(f"  Cores: {cpu_info['cores']}")
        print(f"  Speed: {cpu_info['speed']}")
        print(f"  Usage: {cpu_info['usage']}%")
    except Exception as e:
        print(f"Error getting CPU info: {e}")
    
    # Get memory information
    try:
        memory_info = info_api.get_memory_info()
        print(f"\nMemory Information:")
        print(f"  Total: {memory_info['total']}")
        print(f"  Available: {memory_info['available']}")
        print(f"  Used: {memory_info['used']}")
        print(f"  Usage: {memory_info['percent']}%")
    except Exception as e:
        print(f"Error getting memory info: {e}")
    
    # Get disk information
    try:
        disk_info = info_api.get_disk_info()
        print(f"\nDisk Information:")
        print(f"  Total: {disk_info['total']}")
        print(f"  Used: {disk_info['used']}")
        print(f"  Free: {disk_info['free']}")
        print(f"  Usage: {disk_info['percent']}%")
    except Exception as e:
        print(f"Error getting disk info: {e}")
    
    # 3. Network Information API
    print("\n3. Network Information API:")
    print("-" * 30)
    
    # Get network interfaces
    try:
        interfaces = info_api.get_network_interfaces()
        print("Network Interfaces:")
        for interface, info in interfaces.items():
            if info['addresses']:
                print(f"  {interface}:")
                print(f"    IP: {info['addresses'].get('inet', 'N/A')}")
                print(f"    MAC: {info['addresses'].get('ether', 'N/A')}")
                print(f"    Status: {info['status']}")
    except Exception as e:
        print(f"Error getting network interfaces: {e}")
    
    # Get network statistics
    try:
        net_stats = info_api.get_network_stats()
        print(f"\nNetwork Statistics:")
        print(f"  Bytes Sent: {net_stats['bytes_sent']}")
        print(f"  Bytes Received: {net_stats['bytes_recv']}")
        print(f"  Packets Sent: {net_stats['packets_sent']}")
        print(f"  Packets Received: {net_stats['packets_recv']}")
    except Exception as e:
        print(f"Error getting network stats: {e}")


def monitoring_api_example():
    """Demonstrate Monitoring API usage."""
    print("\n" + "=" * 60)
    print("SyInfo - Monitoring API Example")
    print("=" * 60)
    
    # 1. System Monitoring API
    print("\n1. System Monitoring API:")
    print("-" * 30)
    
    # Get current system metrics
    try:
        system_metrics = monitoring_api.get_system_metrics()
        print("Current System Metrics:")
        print(f"  CPU Usage: {system_metrics['cpu']['percent']}%")
        print(f"  Memory Usage: {system_metrics['memory']['percent']}%")
        print(f"  Disk Usage: {system_metrics['disk']['percent']}%")
        print(f"  Network I/O: {system_metrics['network']['bytes_sent']} sent, {system_metrics['network']['bytes_recv']} received")
    except Exception as e:
        print(f"Error getting system metrics: {e}")
    
    # 2. Process Monitoring API
    print("\n2. Process Monitoring API:")
    print("-" * 30)
    
    # Get top processes
    try:
        top_processes = monitoring_api.get_top_processes(top_n=5, sort_by='memory')
        print("Top 5 Processes by Memory Usage:")
        for i, proc in enumerate(top_processes, 1):
            print(f"  {i}. {proc['name']} (PID: {proc['pid']})")
            print(f"     Memory: {proc['memory_percent']:.1f}% | CPU: {proc['cpu_percent']:.1f}%")
    except Exception as e:
        print(f"Error getting top processes: {e}")
    
    # 3. Data Collection API
    print("\n3. Data Collection API:")
    print("-" * 30)
    
    # Start data collection
    try:
        collection_id = monitoring_api.start_data_collection(
            output_dir="./api_collection",
            interval=5,
            duration=10
        )
        print(f"Started data collection with ID: {collection_id}")
        
        # Wait for collection to complete
        time.sleep(2)
        
        # Get collection status
        status = monitoring_api.get_collection_status(collection_id)
        print(f"Collection Status: {status['status']}")
        
        # Stop collection
        monitoring_api.stop_data_collection(collection_id)
        print("Data collection stopped")
        
    except Exception as e:
        print(f"Error with data collection: {e}")


def analysis_api_example():
    """Demonstrate Analysis API usage."""
    print("\n" + "=" * 60)
    print("SyInfo - Analysis API Example")
    print("=" * 60)
    
    # 1. Performance Analysis API
    print("\n1. Performance Analysis API:")
    print("-" * 30)
    
    # Analyze system performance
    try:
        performance = analysis_api.analyze_system_performance()
        print("System Performance Analysis:")
        print(f"  Overall Score: {performance['score']}/100")
        print(f"  CPU Performance: {performance['cpu']['status']}")
        print(f"  Memory Performance: {performance['memory']['status']}")
        print(f"  Disk Performance: {performance['disk']['status']}")
        print(f"  Network Performance: {performance['network']['status']}")
    except Exception as e:
        print(f"Error analyzing performance: {e}")
    
    # 2. Health Check API
    print("\n2. Health Check API:")
    print("-" * 30)
    
    # Get system health
    try:
        health = analysis_api.get_system_health()
        print("System Health Check:")
        print(f"  Overall Health: {health['overall_health']}")
        print(f"  Health Score: {health['score']}/100")
        
        if health['issues']:
            print("  Issues Found:")
            for issue in health['issues']:
                print(f"    - {issue['type']}: {issue['message']}")
        else:
            print("  No issues found")
            
    except Exception as e:
        print(f"Error getting system health: {e}")
    
    # 3. Trend Analysis API
    print("\n3. Trend Analysis API:")
    print("-" * 30)
    
    # Analyze trends (if data is available)
    try:
        trends = analysis_api.analyze_trends(hours=1)
        print("System Trends (Last Hour):")
        print(f"  CPU Trend: {trends['cpu']['trend']}")
        print(f"  Memory Trend: {trends['memory']['trend']}")
        print(f"  Disk Trend: {trends['disk']['trend']}")
    except Exception as e:
        print(f"Error analyzing trends: {e}")


def main():
    """Run all API examples."""
    info_api_example()
    monitoring_api_example()
    analysis_api_example()
    
    print("\n" + "=" * 60)
    print("API examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main() 