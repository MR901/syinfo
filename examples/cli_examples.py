#!/usr/bin/env python3
"""
CLI Examples

This example demonstrates how to use SyInfo's CLI features
both programmatically and through command-line interface.
"""

import sys
import subprocess
import json
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from syinfo.cli.commands import info_commands, monitor_commands, analyze_commands


def programmatic_cli_example():
    """Demonstrate using CLI commands programmatically."""
    print("=" * 60)
    print("SyInfo - Programmatic CLI Example")
    print("=" * 60)
    
    # 1. System Information Commands
    print("\n1. System Information Commands:")
    print("-" * 30)
    
    # Get system info
    result = info_commands.InfoCommands.get_system_info()
    if result['success']:
        print("System Information:")
        print(f"  OS: {result['data']['os']}")
        print(f"  Kernel: {result['data']['kernel']}")
        print(f"  Architecture: {result['data']['architecture']}")
    else:
        print(f"Error: {result['error']}")
    
    # Get device info
    result = info_commands.InfoCommands.get_device_info()
    if result['success']:
        print("\nDevice Information:")
        print(f"  CPU: {result['data']['cpu']['model']}")
        print(f"  Memory: {result['data']['memory']['total']}")
        print(f"  Disk: {result['data']['disk']['total']}")
    else:
        print(f"Error: {result['error']}")
    
    # Get network info
    result = info_commands.InfoCommands.get_network_info()
    if result['success']:
        print("\nNetwork Information:")
        for interface, info in result['data']['interfaces'].items():
            if info['addresses']:
                print(f"  {interface}: {info['addresses'].get('inet', 'N/A')}")
    else:
        print(f"Error: {result['error']}")
    
    # 2. Monitoring Commands
    print("\n2. Monitoring Commands:")
    print("-" * 30)
    
    # Start monitoring (brief example)
    result = monitor_commands.MonitorCommands.start_monitoring(
        interval=10,
        duration=5,
        output_dir="./monitoring_output"
    )
    if result['success']:
        print(f"Monitoring: {result['message']}")
    else:
        print(f"Monitoring Error: {result['error']}")
    
    # Get monitoring status
    result = monitor_commands.MonitorCommands.get_status()
    if result['success']:
        print(f"Monitoring Status: {result['data']['status']}")
    else:
        print(f"Status Error: {result['error']}")
    
    # 3. Analysis Commands
    print("\n3. Analysis Commands:")
    print("-" * 30)
    
    # Analyze system performance
    result = analyze_commands.AnalyzeCommands.analyze_system_performance()
    if result['success']:
        print("System Performance Analysis:")
        print(f"  CPU Usage: {result['data']['cpu_usage']}%")
        print(f"  Memory Usage: {result['data']['memory_usage']}%")
        print(f"  Disk Usage: {result['data']['disk_usage']}%")
    else:
        print(f"Analysis Error: {result['error']}")
    
    # Get system health
    result = analyze_commands.AnalyzeCommands.get_system_health()
    if result['success']:
        print(f"\nSystem Health: {result['data']['health']}")
        print(f"Score: {result['data']['score']}/100")
        if result['data']['issues']:
            print("Issues:")
            for issue in result['data']['issues']:
                print(f"  - {issue}")
    else:
        print(f"Health Check Error: {result['error']}")


def command_line_example():
    """Demonstrate command-line interface usage."""
    print("\n" + "=" * 60)
    print("SyInfo - Command Line Interface Examples")
    print("=" * 60)
    
    # Example commands to run
    commands = [
        "python -m syinfo info system",
        "python -m syinfo info device",
        "python -m syinfo info network",
        "python -m syinfo monitor start --interval 5 --duration 10",
        "python -m syinfo analyze performance",
        "python -m syinfo analyze health",
        "python -m syinfo --help"
    ]
    
    print("Available CLI commands:")
    for i, cmd in enumerate(commands, 1):
        print(f"{i}. {cmd}")
    
    print("\nTo run these commands:")
    print("1. Navigate to the project root directory")
    print("2. Run: python -m syinfo <command>")
    print("\nExamples:")
    print("  python -m syinfo info system")
    print("  python -m syinfo monitor start --interval 30")
    print("  python -m syinfo analyze health")


def subprocess_example():
    """Demonstrate running CLI commands via subprocess."""
    print("\n" + "=" * 60)
    print("SyInfo - Subprocess CLI Example")
    print("=" * 60)
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    
    try:
        # Run system info command
        print("Running: python -m syinfo info system")
        result = subprocess.run(
            ["python", "-m", "syinfo", "info", "system"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("System Info Output:")
            print(result.stdout)
        else:
            print(f"Error: {result.stderr}")
        
        # Run help command
        print("\nRunning: python -m syinfo --help")
        result = subprocess.run(
            ["python", "-m", "syinfo", "--help"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("Help Output:")
            print(result.stdout)
        else:
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("Command timed out")
    except Exception as e:
        print(f"Error running command: {e}")


def main():
    """Run all CLI examples."""
    programmatic_cli_example()
    command_line_example()
    subprocess_example()
    
    print("\n" + "=" * 60)
    print("CLI examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main() 