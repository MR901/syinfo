# SyInfo - Simple System Information Library
<p align="center">
  <img src="docs/images/logo.png" alt="SyInfo logo - textual art" width="420" />
</p>

[![PyPI version](https://badge.fury.io/py/syinfo.svg)](https://badge.fury.io/py/syinfo)
[![Python versions](https://img.shields.io/pypi/pyversions/syinfo.svg)](https://pypi.org/project/syinfo/)

A simple, well-designed Python library for gathering system information including hardware specifications, network configuration, and real-time system monitoring.

## Key Features

### Device Information
- **CPU Details**: Model, cores, frequency, usage statistics
- **Memory Analysis**: RAM, swap, detailed memory mapping
- **Storage Info**: Disk usage, I/O statistics, filesystem details
- **GPU Detection**: NVIDIA, AMD, Intel graphics cards
- **Device Identification**: Manufacturer, model, serial numbers

### Network Capabilities  
- **Interface Detection**: All network adapters with detailed info
- **Connectivity Analysis**: Public/private IP, DNS, gateways
- **Device Discovery**: Scan and identify devices on local network
- **Network I/O Statistics**: Real-time and historical data
- **WiFi Information**: SSID, signal strength, encryption

### System Monitoring (New!)
- **Real-time Monitoring**: CPU, memory, disk, and network tracking
- **Customizable Intervals**: 1 second to hours, configurable duration
- **JSON Export**: Perfect for scripting and automation with jq
- **Performance Analytics**: Averages, peaks, and trend analysis
- **Non-blocking**: Background monitoring with graceful interruption

### Powerful CLI Interface
- **Flag-based Commands**: Easy scripting (`syinfo -npj -t 10 | jq '.summary'`)
- **JSON Output**: Native jq compatibility for data processing
- **Monitoring Support**: Real-time system performance tracking
- **Flexible Options**: Combine flags for exactly what you need

## Installation

```bash
# Basic installation
pip install syinfo

# With network discovery features
pip install syinfo[network]

# Full installation (all features)
pip install syinfo[full]
```

## Quick Start

### Basic Usage

```python
import syinfo

# Get comprehensive system information
info = syinfo.get_system_info()
print(f"System: {info['system_name']}")
print(f"CPU: {info['cpu_model']} ({info['cpu_cores']} cores)")
print(f"Memory: {info['total_memory']} ({info['memory_usage_percent']:.1f}% used)")
```

### Hardware Information

```python
# Get detailed hardware info
hardware = syinfo.get_hardware_info()

print("CPU Information:")
print(f"  Model: {hardware['cpu']['model']}")
print(f"  Cores: {hardware['cpu']['cores_physical']} physical")
print(f"  Usage: {hardware['cpu']['usage_percent']:.1f}%")

print("Memory Information:")  
print(f"  Total: {hardware['memory']['total']}")
print(f"  Available: {hardware['memory']['available']}")
print(f"  Usage: {hardware['memory']['usage_percent']:.1f}%")
```

### Network Discovery

```python
# Discover devices on network
devices = syinfo.discover_network_devices(timeout=10)
print(f"Found {len(devices)} devices:")

for device in devices:
    print(f"  {device['ip']:15} - {device['hostname']} ({device['vendor']})")
```

### System Monitoring (New!)

```python
# Create a simple system monitor  
monitor = syinfo.create_simple_monitor(interval=5)

# Start monitoring for 60 seconds
monitor.start(duration=60)
import time
time.sleep(61)
results = monitor.stop()

print(f"Average CPU Usage: {results['summary']['cpu_avg']:.1f}%")
print(f"Peak Memory Usage: {results['summary']['memory_peak']:.1f}%")
print(f"Data Points Collected: {results['total_points']}")
```

## CLI Interface - Flag-Based Commands

### Device Information
```bash
# Device/hardware information
syinfo -d

# With JSON output
syinfo -dj | jq '.cpu_info.model'
```

### Network Operations
```bash
# Network information
syinfo -n -t 10          # Scan network for 10 seconds

# Network with device info
syinfo -s -t 15          # Combined system info, 15-second network scan

# JSON output for parsing
syinfo -nj -t 5 | jq '.network_devices | length'
```

### System Monitoring (New!)
```bash
# Monitor system for 30 seconds, 5-second intervals
syinfo -m -t 30 -i 5

# JSON monitoring data
syinfo -mpj -t 60 -i 10 | tail -1 | jq '.summary'

# Extract specific metrics
syinfo -mpj -t 120 -i 15 | tail -1 | jq -r '.summary.cpu_avg'

# Continuous monitoring to file
syinfo -mpj -t 300 -i 30 | tail -1 > performance.json
```

### Advanced CLI Usage
```bash
# Disable output, just get JSON
syinfo -dpj > device_info.json

# Network scan without vendor lookup (faster)
syinfo -noj -t 5

# Monitor and process with jq
syinfo -mpj -t 60 -i 10 | tail -1 | jq '.data_points[].cpu_percent | max'

# Complex monitoring workflows
CPU_AVG=$(syinfo -mpj -t 30 -i 5 | tail -1 | jq -r '.summary.cpu_avg')
if (( $(echo "$CPU_AVG > 80" | bc -l) )); then
  echo "High CPU usage detected: $CPU_AVG%"
fi
```

## CLI Flag Reference

| Flag | Long Flag | Description |
|------|-----------|-------------|
| `-d` | `--device` | Show device/hardware information |
| `-n` | `--network` | Show network information and scan devices |
| `-s` | `--system` | Show combined device and network information |
| `-m` | `--monitor` | **Start system monitoring** |
| `-t` | `--time` | Duration in seconds (network scan or monitoring) |
| `-i` | `--interval` | **Monitoring interval in seconds (default: 5)** |
| `-p` | `--disable-print` | Suppress formatted output |
| `-j` | `--return-json` | Output as JSON |
| `-o` | `--disable-vendor-search` | Skip vendor lookup (faster network scans) |

## System Monitoring Features

### Real-time Performance Tracking
- **CPU Usage**: Per-core and overall utilization
- **Memory Statistics**: Usage, available, swap information
- **Disk I/O**: Read/write operations and usage percentages
- **Network Activity**: Bytes and packets sent/received

### JSON Data Structure
```json
{
  "total_points": 12,
  "data_points": [
    {
      "timestamp": "2025-09-14T02:20:42.029017",
      "cpu_percent": 7.8,
      "memory_percent": 68.2,
      "disk_percent": 82.8,
      "network_io": {
        "bytes_sent": 3301001170,
        "bytes_recv": 4409283972,
        "packets_sent": 3556700,
        "packets_recv": 5418377
      }
    }
  ],
  "summary": {
    "duration_seconds": 60,
    "cpu_avg": 5.3,
    "cpu_max": 8.3,
    "memory_avg": 68.2,
    "memory_peak": 68.4,
    "disk_avg": 82.8,
    "start_time": "2025-09-14T02:20:42.029017",
    "end_time": "2025-09-14T02:21:42.029017"
  }
}
```

### Monitoring Use Cases
```bash
# Server performance monitoring
syinfo -mpj -t 3600 -i 60 | tail -1 > hourly_stats.json

# Quick system check
syinfo -m -t 10 -i 2

# CPU spike detection
syinfo -mpj -t 300 -i 5 | tail -1 | jq '.data_points[] | select(.cpu_percent > 90)'

# Network throughput analysis
syinfo -mpj -t 120 -i 10 | tail -1 | jq '.data_points | [.[0], .[-1]] | .[1].network_io.bytes_sent - .[0].network_io.bytes_sent'
```

## Error Handling

```python
from syinfo.exceptions import SystemAccessError, DataCollectionError

try:
    info = syinfo.get_system_info()
except SystemAccessError as e:
    print(f"Permission error: {e}")
except DataCollectionError as e:
    print(f"Data collection failed: {e}")
```

## Performance & Reliability

### Benchmarks
- **Data Collection**: < 2 seconds for complete system scan
- **Memory Usage**: < 50MB peak memory consumption  
- **Network Scan**: < 15 seconds for typical home network
- **Monitoring Overhead**: < 1% CPU during continuous monitoring

## Development

### Setup
```bash
git clone https://github.com/MR901/syinfo.git
cd syinfo
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e .[dev,full]
```

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=syinfo --cov-report=html

# Test monitoring functionality
python -c "import syinfo; m=syinfo.create_simple_monitor(1); m.start(5); import time; time.sleep(6); print(m.stop())"
```

## Examples

Check out the [examples/](examples/) directory for comprehensive usage examples:
- [API Usage](examples/api_example.py) - Python API examples
- [CLI Examples](examples/cli_examples.py) - Command line usage
- [Monitoring Examples](examples/monitoring_example.py) - System monitoring

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/MR901/syinfo/issues)  
- **Email**: mohitrajput901@gmail.com
- **GitHub**: [https://github.com/MR901/syinfo](https://github.com/MR901/syinfo)