# SyInfo Documentation

> **Simple, well-designed system information library**

## Quick Start

### Installation
```bash
pip install syinfo
```

### Basic Usage

```python
import syinfo

# Get system information
info = syinfo.get_system_info()
print(f"OS: {info['system_name']}")
print(f"CPU: {info['cpu_model']}")
print(f"Memory: {info['total_memory']}")

# Get hardware details
hardware = syinfo.get_hardware_info()
print(f"CPU Cores: {hardware['cpu']['cores_physical']}")

# Network discovery (optional)
devices = syinfo.discover_network_devices(timeout=5)
print(f"Found {len(devices)} network devices")

# Simple monitoring
monitor = syinfo.create_simple_monitor(interval=30)
monitor.start(duration=300)  # Monitor for 5 minutes
results = monitor.stop()
print(f"Average CPU: {results['summary']['cpu_avg']:.1f}%")
```

### Command Line

```bash
# System information
syinfo info system    # Complete system info
syinfo info device    # Hardware only
syinfo info network   # Network only  
syinfo info brief     # Quick summary

# Export data
syinfo export --format json
syinfo export --format yaml --output system.yaml
```

## Features

- **Hardware Information**: CPU, memory, disk, GPU details
- **Network Information**: Interfaces, device discovery
- **Simple Monitoring**: Lightweight performance tracking
- **Export Options**: JSON, YAML, CSV formats
- **Clean API**: Simple functions for common tasks
- **CLI Interface**: Easy command-line access

## API Reference

### Core Functions

#### `syinfo.get_system_info()` 
Returns simplified system information dictionary with easy-access keys.

#### `syinfo.get_hardware_info()`
Returns detailed hardware information.

#### `syinfo.get_network_info(scan_devices=False)`
Returns network information, optionally scanning for devices.

#### `syinfo.discover_network_devices(timeout=10)`
Scan for devices on the local network.

#### `syinfo.create_simple_monitor(interval=60)`
Create a simple system monitor.

#### `syinfo.export_system_info(format="json", output_file=None)`
Export system information in various formats.

### Available Features

```python
features = syinfo.get_available_features()
# Returns: {'core': True, 'network': True, 'monitoring': True}
```

## Installation Options

```bash
# Basic installation
pip install syinfo

# With network features (recommended)
pip install syinfo[network]

# Full installation
pip install syinfo[full]
```

## Requirements

- Python 3.8+
- Linux (primary), macOS, Windows
- Core dependencies: psutil, PyYAML, tabulate

## Examples

See the `examples/` directory for more detailed examples:
- `basic_system_info.py` - Core functionality
- `monitoring_example.py` - Simple monitoring
- `api_example.py` - Full API usage

## Support

- **Issues**: [GitHub Issues](https://github.com/MR901/syinfo/issues)
- **Email**: mohitrajput901@gmail.com
- **Repository**: [GitHub](https://github.com/MR901/syinfo)

## License

MIT License - see LICENSE file for details.
