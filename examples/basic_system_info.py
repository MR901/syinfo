#!/usr/bin/env python3
"""
Basic System Information Example

This example demonstrates how to use SyInfo's core system information features
to get basic details about the system, devices, and network.
"""

import sys
import json
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from syinfo.core import sys_info, device_info, network_info


def main():
    """Demonstrate basic system information collection."""
    print("=" * 60)
    print("SyInfo - Basic System Information Example")
    print("=" * 60)
    
    # 1. System Information
    print("\n1. System Information:")
    print("-" * 30)
    
    sys_info_obj = sys_info.SysInfo()
    
    # Get basic system info
    basic_info = sys_info_obj.get_basic_info()
    print(f"OS: {basic_info['os']}")
    print(f"Kernel: {basic_info['kernel']}")
    print(f"Architecture: {basic_info['architecture']}")
    print(f"Hostname: {basic_info['hostname']}")
    print(f"Uptime: {basic_info['uptime']}")
    
    # Get detailed system info
    detailed_info = sys_info_obj.get_detailed_info()
    print(f"\nCPU Cores: {detailed_info['cpu']['cores']}")
    print(f"Total Memory: {detailed_info['memory']['total']}")
    print(f"Available Memory: {detailed_info['memory']['available']}")
    
    # 2. Device Information
    print("\n2. Device Information:")
    print("-" * 30)
    
    device_info_obj = device_info.DeviceInfo()
    
    # Get CPU information
    cpu_info = device_info_obj.get_cpu_info()
    print(f"CPU Model: {cpu_info['model']}")
    print(f"CPU Cores: {cpu_info['cores']}")
    print(f"CPU Speed: {cpu_info['speed']}")
    
    # Get memory information
    memory_info = device_info_obj.get_memory_info()
    print(f"Total RAM: {memory_info['total']}")
    print(f"Available RAM: {memory_info['available']}")
    print(f"Memory Usage: {memory_info['percent']}%")
    
    # Get disk information
    disk_info = device_info_obj.get_disk_info()
    print(f"Disk Usage: {disk_info['usage']}%")
    print(f"Disk Space: {disk_info['free']} free of {disk_info['total']}")
    
    # 3. Network Information
    print("\n3. Network Information:")
    print("-" * 30)
    
    network_info_obj = network_info.NetworkInfo()
    
    # Get network interfaces
    interfaces = network_info_obj.get_network_interfaces()
    for interface, info in interfaces.items():
        if info['addresses']:
            print(f"Interface: {interface}")
            print(f"  IP Address: {info['addresses'].get('inet', 'N/A')}")
            print(f"  MAC Address: {info['addresses'].get('ether', 'N/A')}")
            print(f"  Status: {info['status']}")
    
    # Get network statistics
    net_stats = network_info_obj.get_network_stats()
    print(f"\nNetwork Statistics:")
    print(f"  Bytes Sent: {net_stats['bytes_sent']}")
    print(f"  Bytes Received: {net_stats['bytes_recv']}")
    print(f"  Packets Sent: {net_stats['packets_sent']}")
    print(f"  Packets Received: {net_stats['packets_recv']}")
    
    # 4. Print brief system info (legacy function)
    print("\n4. Brief System Info (Legacy):")
    print("-" * 30)
    sys_info.print_brief_sys_info()
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main() 