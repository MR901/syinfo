#!/usr/bin/env python3
"""
SyInfo API Examples

This example demonstrates how to use SyInfo's Python API for
gathering system information, network discovery, and monitoring.
"""

import json
import sys
import time
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import syinfo


def info_api_example():
    """Demonstrate Info API usage."""
    print("=" * 60)
    print("SyInfo - Info API Example")
    print("=" * 60)

    # 1. System Information API
    print("\n1. System Information API:")
    print("-" * 30)

    try:
        # Get basic system info
        basic_info = syinfo.get_system_info()
        print(f"System: {basic_info.get('system_name', 'Unknown')}")
        print(f"CPU Model: {basic_info.get('cpu_model', 'Unknown')}")
        print(f"Total Memory: {basic_info.get('total_memory', 'Unknown')}")
        print(f"Python Version: {basic_info.get('python_version', 'Unknown')}")
        
    except Exception as e:
        print(f"Error getting system info: {e}")

    # 2. Complete Information API
    print("\n2. Complete Information API:")
    print("-" * 30)
    
    try:
        complete_info = syinfo.get_complete_info(include_network=False)
        
        # Display CPU information
        cpu_info = complete_info.get('cpu_info', {})
        print(f"CPU Cores: {cpu_info.get('cores', {}).get('physical', 'Unknown')}")
        print(f"CPU Usage: {cpu_info.get('percentage_used', {}).get('total', 'Unknown')}%")
        
        # Display memory information
        memory_info = complete_info.get('memory_info', {})
        virtual_mem = memory_info.get('virtual', {})
        print(f"Memory Usage: {virtual_mem.get('percent', 'Unknown')}%")
        print(f"Available Memory: {virtual_mem.get('readable', {}).get('available', 'Unknown')}")
        
    except Exception as e:
        print(f"Error getting complete info: {e}")

    # 3. Hardware Information API
    print("\n3. Hardware Information API:")
    print("-" * 30)
    
    try:
        hardware_info = syinfo.get_hardware_info()
        
        # Display hardware details
        cpu = hardware_info.get('cpu', {})
        memory = hardware_info.get('memory', {})
        
        print(f"CPU Model: {cpu.get('model', 'Unknown')}")
        print(f"Physical Cores: {cpu.get('cores_physical', 'Unknown')}")
        print(f"Logical Cores: {cpu.get('cores_logical', 'Unknown')}")
        print(f"Memory Total: {memory.get('total', 'Unknown')}")
        print(f"Memory Available: {memory.get('available', 'Unknown')}")
        
    except Exception as e:
        print(f"Error getting hardware info: {e}")


def network_api_example():
    """Demonstrate Network API usage."""
    print("\n" + "=" * 60)
    print("SyInfo - Network API Example")
    print("=" * 60)

    # 1. Network Information API
    print("\n1. Network Information API:")
    print("-" * 30)

    try:
        network_info = syinfo.get_network_info(scan_devices=False)
        
        print(f"Hostname: {network_info.get('hostname', 'Unknown')}")
        print(f"MAC Address: {network_info.get('mac_address', 'Unknown')}")
        print(f"Internet Present: {network_info.get('internet_present', 'Unknown')}")
        
        # Display current addresses
        current_addr = network_info.get('current_addresses', {})
        print(f"Public IP: {current_addr.get('public_ip', 'Unknown')}")
        print(f"Local IP: {current_addr.get('ip_address', 'Unknown')}")
        print(f"Gateway: {current_addr.get('gateway', 'Unknown')}")
        
    except Exception as e:
        print(f"Error getting network info: {e}")

    # 2. Network Device Discovery API
    print("\n2. Network Device Discovery API:")
    print("-" * 30)

    try:
        print("Discovering devices on network (this may take a few seconds)...")
        devices = syinfo.discover_network_devices(timeout=8)
        
        if devices and len(devices) > 0:
            print(f"Found {len(devices)} devices:")
            for i, device in enumerate(devices[:5], 1):  # Show first 5 devices
                print(f"  {i}. {device.get('ip', 'Unknown IP')} - {device.get('hostname', 'Unknown Host')}")
                if device.get('vendor'):
                    print(f"     Vendor: {device['vendor']}")
        else:
            print("No devices found or discovery requires sudo privileges")
            
    except Exception as e:
        print(f"Error discovering network devices: {e}")


def monitoring_api_example():
    """Demonstrate Monitoring API usage."""
    print("\n" + "=" * 60)
    print("SyInfo - Monitoring API Example")
    print("=" * 60)

    # 1. Simple Monitor Creation
    print("\n1. Simple Monitor Creation:")
    print("-" * 30)

    try:
        # Create monitor with 2-second intervals
        monitor = syinfo.create_simple_monitor(interval=2)
        print("Monitor created successfully")
        print(f"Monitor interval: {monitor.interval} seconds")
        
    except Exception as e:
        print(f"Error creating monitor: {e}")
        return

    # 2. Start Monitoring
    print("\n2. Start Monitoring:")
    print("-" * 30)

    try:
        print("Starting monitoring for 8 seconds...")
        monitor.start(duration=8)
        print("Monitoring started")
        
        # Wait for monitoring to complete
        time.sleep(9)
        
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
        
        print("Monitoring completed")
        
    except Exception as e:
        print(f"Error during monitoring: {e}")
        return

    # 3. Analyze Results
    print("\n3. Monitor Results Analysis:")
    print("-" * 30)

    try:
        print(f"Data Points Collected: {results.get('total_points', 0)}")
        
        summary = results.get('summary', {})
        if summary:
            print(f"Duration: {summary.get('duration_seconds', 0)} seconds")
            print(f"CPU Average: {summary.get('cpu_avg', 0):.1f}%")
            print(f"CPU Maximum: {summary.get('cpu_max', 0):.1f}%")
            print(f"Memory Average: {summary.get('memory_avg', 0):.1f}%")
            print(f"Memory Peak: {summary.get('memory_peak', 0):.1f}%")
            print(f"Disk Usage: {summary.get('disk_avg', 0):.1f}%")
        
        # Analyze individual data points
        data_points = results.get('data_points', [])
        if data_points:
            print(f"\nFirst Data Point:")
            first = data_points[0]
            print(f"  Timestamp: {first.get('timestamp', 'Unknown')}")
            print(f"  CPU: {first.get('cpu_percent', 0):.1f}%")
            print(f"  Memory: {first.get('memory_percent', 0):.1f}%")
            
            if len(data_points) > 1:
                print(f"\nLast Data Point:")
                last = data_points[-1]
                print(f"  Timestamp: {last.get('timestamp', 'Unknown')}")
                print(f"  CPU: {last.get('cpu_percent', 0):.1f}%")
                print(f"  Memory: {last.get('memory_percent', 0):.1f}%")
        
    except Exception as e:
        print(f"Error analyzing results: {e}")


def data_export_example():
    """Demonstrate Data Export functionality."""
    print("\n" + "=" * 60)
    print("SyInfo - Data Export Example")
    print("=" * 60)

    # 1. JSON Export
    print("\n1. JSON Export:")
    print("-" * 30)

    try:
        json_data = syinfo.export_system_info("json")
        
        # Parse JSON to verify it's valid
        parsed_data = json.loads(json_data)
        print("JSON export successful")
        print(f"JSON data size: {len(json_data)} characters")
        print("JSON structure keys:", list(parsed_data.keys())[:5])
        
        # Save to file
        with open("system_info_export.json", "w") as f:
            f.write(json_data)
        print("JSON data saved to system_info_export.json")
        
    except Exception as e:
        print(f"Error with JSON export: {e}")

    # 2. YAML Export
    print("\n2. YAML Export:")
    print("-" * 30)

    try:
        yaml_data = syinfo.export_system_info("yaml", output_file="system_info_export.yaml")
        print("YAML export successful")
        print(f"YAML data size: {len(yaml_data)} characters")
        print("YAML data saved to system_info_export.yaml")
        
    except Exception as e:
        print(f"Error with YAML export: {e}")


def feature_detection_example():
    """Demonstrate Feature Detection functionality."""
    print("\n" + "=" * 60)
    print("SyInfo - Feature Detection Example")
    print("=" * 60)

    # 1. Available Features
    print("\n1. Available Features:")
    print("-" * 30)

    try:
        features = syinfo.get_available_features()
        print("Available features:")
        for feature, available in features.items():
            status = "[AVAILABLE]" if available else "[NOT AVAILABLE]"
            print(f"  {status} {feature}: {available}")
            
    except Exception as e:
        print(f"Error getting available features: {e}")

    # 2. Feature Status
    print("\n2. Feature Status Display:")
    print("-" * 30)

    try:
        syinfo.print_feature_status()
        
    except Exception as e:
        print(f"Error printing feature status: {e}")


def display_examples():
    """Demonstrate Display functionality."""
    print("\n" + "=" * 60)
    print("SyInfo - Display Examples")
    print("=" * 60)

    # 1. System Tree Display
    print("\n1. System Tree Display:")
    print("-" * 30)

    try:
        print("Displaying system information tree...")
        syinfo.print_system_tree()
        
    except Exception as e:
        print(f"Error displaying system tree: {e}")

    # 2. Brief Information
    print("\n2. Brief Information Display:")
    print("-" * 30)

    try:
        syinfo.print_brief_info()
        
    except Exception as e:
        print(f"Error displaying brief info: {e}")


def main():
    """Run all API examples."""
    print("SyInfo Python API Examples")
    print("=" * 26)
    print("This script demonstrates the complete SyInfo Python API")
    print("including system information, network operations, monitoring,")
    print("and data export capabilities.\n")
    
    try:
        # Core information APIs
        info_api_example()
        
        # Network operations
        network_api_example()
        
        # System monitoring
        monitoring_api_example()
        
        # Data export
        data_export_example()
        
        # Feature detection
        feature_detection_example()
        
        # Display functionality
        display_examples()
        
        print("\n" + "=" * 60)
        print("All API examples completed successfully!")
        print("Check the generated files:")
        print("  - system_info_export.json")
        print("  - system_info_export.yaml")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\nAPI examples interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error running API examples: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()