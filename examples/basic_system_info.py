#!/usr/bin/env python3
"""
Basic System Information Example

This example demonstrates how to use SyInfo's core classes to
gather basic system information.
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import syinfo
from syinfo.core import device_info, sys_info


def main():
    """Demonstrate basic system information gathering."""
    print("=" * 60)
    print("SyInfo - Basic System Information Example")
    print("=" * 60)

    # 1. Using High-Level API
    print("\n1. High-Level API Usage:")
    print("-" * 30)

    try:
        # Get basic system info using the main API
        basic_info = syinfo.get_system_info()
        print(f"System: {basic_info.get('system_name', 'Unknown')}")
        print(f"Hostname: {basic_info.get('hostname', 'Unknown')}")
        print(f"CPU Model: {basic_info.get('cpu_model', 'Unknown')}")
        print(f"CPU Cores: {basic_info.get('cpu_cores', 'Unknown')}")
        print(f"Total Memory: {basic_info.get('total_memory', 'Unknown')}")
        print(f"Memory Usage: {basic_info.get('memory_usage_percent', 'Unknown')}%")
        print(f"Python Version: {basic_info.get('python_version', 'Unknown')}")
        
    except Exception as e:
        print(f"Error getting system info: {e}")

    # 2. Using Core Classes
    print("\n2. Core Classes Usage:")
    print("-" * 30)

    try:
        # Get comprehensive device information
        device_info_obj = device_info.DeviceInfo()
        complete_info = device_info_obj.get_all()
        
        # Extract and display key information
        dev_info = complete_info.get('dev_info', {})
        print(f"Mac Address: {dev_info.get('mac_address', 'Unknown')}")
        print(f"System Type: {dev_info.get('chassis', 'Unknown')}")
        print(f"Hostname: {dev_info.get('static_hostname', 'Unknown')}")
        
        # CPU information
        cpu_info = complete_info.get('cpu_info', {})
        cores = cpu_info.get('cores', {})
        print(f"Physical Cores: {cores.get('physical', 'Unknown')}")
        print(f"Total Cores: {cores.get('total', 'Unknown')}")
        
        # Memory information
        memory_info = complete_info.get('memory_info', {})
        virtual_mem = memory_info.get('virtual', {})
        print(f"Memory Usage: {virtual_mem.get('percent', 'Unknown')}%")
        print(f"Total Memory: {virtual_mem.get('readable', {}).get('total', 'Unknown')}")
        print(f"Available Memory: {virtual_mem.get('readable', {}).get('available', 'Unknown')}")
        
    except Exception as e:
        print(f"Error getting device info: {e}")

    # 3. System Information Display
    print("\n3. Formatted System Display:")
    print("-" * 30)

    try:
        # Use the built-in system tree display
        print("Complete system information tree:")
        syinfo.print_system_tree()
        
    except Exception as e:
        print(f"Error displaying system tree: {e}")

    # 4. Hardware-Focused Information
    print("\n4. Hardware Information:")
    print("-" * 30)

    try:
        hardware_info = syinfo.get_hardware_info()
        
        # CPU details
        cpu = hardware_info.get('cpu', {})
        print(f"CPU Model: {cpu.get('model', 'Unknown')}")
        print(f"CPU Frequency: {cpu.get('frequency', 'Unknown')} MHz")
        print(f"CPU Usage: {cpu.get('usage_percent', 'Unknown')}%")
        
        # Memory details  
        memory = hardware_info.get('memory', {})
        print(f"Memory Total: {memory.get('total', 'Unknown')}")
        print(f"Memory Used: {memory.get('used', 'Unknown')}")
        print(f"Memory Available: {memory.get('available', 'Unknown')}")
        
        # GPU information (if available)
        gpu = hardware_info.get('gpu', {})
        if gpu:
            print(f"GPU: {gpu.get('name', 'Unknown')}")
            print(f"GPU Memory: {gpu.get('memory_total', 'Unknown')}")
        
    except Exception as e:
        print(f"Error getting hardware info: {e}")

    # 5. Brief Information
    print("\n5. Brief System Summary:")
    print("-" * 30)

    try:
        syinfo.print_brief_info()
        
    except Exception as e:
        print(f"Error displaying brief info: {e}")

    print("\n" + "=" * 60)
    print("Basic system information example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()