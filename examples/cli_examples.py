#!/usr/bin/env python3
"""
SyInfo CLI Examples

Comprehensive examples for using the SyInfo command line interface.
This file demonstrates all CLI capabilities including basic info gathering,
network operations, system monitoring, data export, and integration with other tools.

License: MIT
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path


def basic_information_examples():
    """Demonstrate basic information gathering with flag-based CLI."""
    print("=" * 60)
    print("SyInfo - Basic Information Examples")
    print("=" * 60)

    # ===============================================
    # DEVICE INFORMATION
    # ===============================================
    print("\n=== Device Information ===")
    os.system("syinfo -d")
    
    print("\n=== Device Information (JSON) ===")
    os.system("syinfo -dj | jq '.cpu_info.model'")
    
    # ===============================================
    # NETWORK OPERATIONS
    # ===============================================
    print("\n=== Network Discovery ===")
    os.system("syinfo -n -t 10")
    
    print("\n=== Network Information (JSON) ===")
    os.system("syinfo -nj -t 8 | jq '.network_devices | length'")
    
    # ===============================================
    # SYSTEM INFORMATION (COMBINED)
    # ===============================================
    print("\n=== Combined System Information ===")
    os.system("syinfo -s -t 10")


def monitoring_examples():
    """Demonstrate system monitoring capabilities."""
    print("\n" + "=" * 60)
    print("SyInfo - System Monitoring Examples")
    print("=" * 60)

    # ===============================================
    # BASIC MONITORING
    # ===============================================
    print("\n=== Basic System Monitoring ===")
    print("Monitoring system for 15 seconds with 3-second intervals...")
    os.system("syinfo -m -t 15 -i 3")
    
    # ===============================================
    # JSON MONITORING DATA
    # ===============================================
    print("\n=== JSON Monitoring Data ===")
    print("Getting monitoring data as JSON...")
    os.system("syinfo -mpj -t 12 -i 2 | tail -1 | jq '.summary'")
    
    # ===============================================
    # MONITORING METRICS EXTRACTION
    # ===============================================
    print("\n=== Monitoring Metrics Extraction ===")
    
    print("CPU Average:")
    os.system("syinfo -mpj -t 10 -i 2 | tail -1 | jq -r '.summary.cpu_avg'")
    
    print("\nMemory Peak:")
    os.system("syinfo -mpj -t 10 -i 2 | tail -1 | jq -r '.summary.memory_peak'")
    
    print("\nData Points Count:")
    os.system("syinfo -mpj -t 10 -i 2 | tail -1 | jq '.total_points'")


def data_export_examples():
    """Demonstrate data export capabilities."""
    print("\n" + "=" * 60)
    print("SyInfo - Data Export Examples")
    print("=" * 60)

    # ===============================================
    # SYSTEM INFO EXPORT
    # ===============================================
    print("\n=== Device Info Export ===")
    print("Exporting device information to JSON file...")
    os.system("syinfo -dpj > device_info.json")
    print("Device info saved to device_info.json")
    
    # ===============================================
    # MONITORING DATA EXPORT
    # ===============================================
    print("\n=== Monitoring Data Export ===")
    print("Exporting 30-second monitoring data...")
    os.system("syinfo -mpj -t 30 -i 5 | tail -1 > monitoring_data.json")
    print("Monitoring data saved to monitoring_data.json")
    
    # ===============================================
    # NETWORK DATA EXPORT
    # ===============================================
    print("\n=== Network Data Export ===")
    print("Exporting network scan data...")
    os.system("syinfo -npj -t 8 | tail -1 > network_scan.json")
    print("Network scan saved to network_scan.json")


def advanced_usage_examples():
    """Demonstrate advanced CLI usage patterns."""
    print("\n" + "=" * 60)
    print("SyInfo - Advanced Usage Examples")
    print("=" * 60)

    # ===============================================
    # PERFORMANCE ANALYSIS
    # ===============================================
    print("\n=== Performance Analysis ===")
    
    print("Finding high CPU usage periods:")
    os.system("""syinfo -mpj -t 20 -i 2 | tail -1 | jq '.data_points[] | select(.cpu_percent > 5) | "\\(.timestamp): \\(.cpu_percent)%"'""")
    
    print("\nNetwork throughput calculation:")
    os.system("""syinfo -mpj -t 15 -i 5 | tail -1 | jq '.data_points | [.[0], .[-1]] | .[1].network_io.bytes_sent - .[0].network_io.bytes_sent | . / 1024 / 1024 | "Throughput: \\(.) MB"'""")
    
    # ===============================================
    # MONITORING AUTOMATION
    # ===============================================
    print("\n=== Monitoring Automation ===")
    
    print("CPU threshold monitoring:")
    cpu_check = """
CPU_AVG=$(syinfo -mpj -t 10 -i 2 | tail -1 | jq -r '.summary.cpu_avg')
if (( $(echo "$CPU_AVG > 2" | bc -l) 2>/dev/null )); then
  echo "CPU usage: $CPU_AVG%"
else
  echo "Low CPU usage detected"
fi
"""
    os.system(cpu_check)
    
    # ===============================================
    # DATA PROCESSING PIPELINES
    # ===============================================
    print("\n=== Data Processing Pipelines ===")
    
    print("Memory usage trend analysis:")
    os.system("syinfo -mpj -t 15 -i 3 | tail -1 | jq '.data_points | [.[].memory_percent] | add / length | \"Average Memory: \\(.)%\"'")
    
    print("\nSystem health summary:")
    os.system("""syinfo -mpj -t 12 -i 2 | tail -1 | jq '{
      cpu_status: (if .summary.cpu_avg > 70 then "HIGH" elif .summary.cpu_avg > 30 then "MEDIUM" else "LOW" end),
      memory_status: (if .summary.memory_avg > 80 then "HIGH" elif .summary.memory_avg > 50 then "MEDIUM" else "LOW" end),
      duration: .summary.duration_seconds,
      data_points: .total_points
    }'""")


def integration_examples():
    """Demonstrate integration with other tools and systems."""
    print("\n" + "=" * 60)
    print("SyInfo - Integration Examples")
    print("=" * 60)

    # ===============================================
    # LOG FILE INTEGRATION
    # ===============================================
    print("\n=== Log File Integration ===")
    
    print("Timestamped performance logging:")
    log_command = '''syinfo -mpj -t 8 -i 2 | tail -1 | jq -r '"[" + now + "] CPU: " + (.summary.cpu_avg | tostring) + "% Memory: " + (.summary.memory_avg | tostring) + "%"' '''
    os.system(log_command)
    
    # ===============================================
    # MONITORING SCRIPTS
    # ===============================================
    print("\n=== Monitoring Scripts ===")
    
    print("System status check script:")
    status_script = """
RESULT=$(syinfo -mpj -t 6 -i 1 | tail -1)
CPU=$(echo "$RESULT" | jq -r '.summary.cpu_avg // 0')
MEM=$(echo "$RESULT" | jq -r '.summary.memory_avg // 0')

echo "System Status:"
echo "  CPU: ${CPU}%"
echo "  Memory: ${MEM}%"
echo "  Status: $(echo "$RESULT" | jq -r 'if (.summary.cpu_avg // 0) > 80 or (.summary.memory_avg // 0) > 90 then "WARNING" else "OK" end')"
"""
    os.system(status_script)


def help_and_usage():
    """Display help and usage information."""
    print("\n" + "=" * 60)
    print("SyInfo - Help and Usage")
    print("=" * 60)
    
    print("\n=== CLI Help ===")
    os.system("syinfo --help")
    
    print("\n=== Version Information ===")
    os.system("syinfo --version")


def main():
    """Run all CLI examples."""
    print("SyInfo CLI Examples")
    print("==================")
    print("This script demonstrates the full range of SyInfo CLI capabilities")
    print("including device information, network operations, system monitoring,")
    print("and data export features.\n")
    
    try:
        # Basic information gathering
        basic_information_examples()
        
        # System monitoring
        monitoring_examples()
        
        # Data export
        data_export_examples()
        
        # Advanced usage patterns
        advanced_usage_examples()
        
        # Integration examples
        integration_examples()
        
        # Help and usage
        help_and_usage()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("Check the generated JSON files:")
        print("  - device_info.json")
        print("  - monitoring_data.json") 
        print("  - network_scan.json")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\nExamples interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError running examples: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()