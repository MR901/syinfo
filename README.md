# SyInfo - Simple System Information Library

[![PyPI version](https://badge.fury.io/py/syinfo.svg)](https://badge.fury.io/py/syinfo)
[![Python versions](https://img.shields.io/pypi/pyversions/syinfo.svg)](https://pypi.org/project/syinfo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple, well-designed Python library for gathering system information including hardware specifications, network configuration, and optional lightweight monitoring.

## Key Features

### Hardware Information
- **CPU Details**: Model, cores, frequency, usage statistics
- **Memory Analysis**: RAM, swap, detailed memory mapping
- **Storage Info**: Disk usage, I/O statistics, filesystem details
- **GPU Detection**: NVIDIA, AMD, Intel graphics cards
- **Device Identification**: Manufacturer, model, serial numbers

### Network Capabilities  
- **Interface Detection**: All network adapters with detailed info
- **Connectivity Analysis**: Public/private IP, DNS, gateways
- **Device Discovery**: Scan and identify devices on local network
- **Traffic Monitoring**: Network I/O statistics and trends
- **WiFi Information**: SSID, signal strength, encryption

### Simple Monitoring (Optional)
- **Lightweight Monitoring**: Basic CPU, memory, disk tracking
- **Data Export**: JSON, CSV, YAML formats
- **Simple API**: Easy-to-use monitoring functions

### Developer Features
- **Type Hints**: Full typing support for better IDE experience
- **Simple Exceptions**: Clean error handling
- **Easy Testing**: Straightforward test structure
- **Clear Documentation**: Simple, focused documentation

## Installation

```bash
# Basic installation
pip install syinfo

# With monitoring features
pip install syinfo[monitoring]

# With network features  
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
print(f"Public IP: {info['public_ip']}")
```

### Hardware Information

```python
# Get detailed hardware info
hardware = syinfo.get_hardware_info()

print("CPU Information:")
print(f"  Model: {hardware['cpu']['model']}")
print(f"  Cores: {hardware['cpu']['cores_physical']} physical, {hardware['cpu']['cores_logical']} logical")
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

### System Tree View

```python
# Display detailed system information in tree format
syinfo.print_system_tree()
```

### Simple Monitoring

```python
# Create a simple system monitor  
monitor = syinfo.create_simple_monitor(interval=30)

# Start monitoring for 5 minutes
monitor.start(duration=300)
results = monitor.stop()
print(f"Average CPU Usage: {results['summary']['cpu_avg']:.1f}%")
print(f"Peak Memory Usage: {results['summary']['memory_peak']:.1f}%")
```

### Command Line Interface

```bash
# System information
syinfo info system

# Hardware details
syinfo info device

# Network information
syinfo info network

# Export system info
syinfo export --format json --output system_info.json
```

## Performance & Reliability

### Benchmarks
- **Data Collection**: < 2 seconds for complete system scan
- **Memory Usage**: < 50MB peak memory consumption  
- **Network Scan**: < 15 seconds for typical home network
- **CPU Overhead**: < 1% during continuous monitoring

### Error Handling
```python
from syinfo.exceptions import SystemAccessError, DataCollectionError

try:
    info = syinfo.get_system_info()
except SystemAccessError as e:
    print(f"Permission error: {e}")
    print(f"Try running with elevated privileges")
except DataCollectionError as e:
    print(f"Data collection failed: {e}")
    print(f"Some system information may be unavailable")
```

## Advanced Usage

### Custom Data Collection

```python
from syinfo.core import DeviceInfoCollector, NetworkScanner

# Custom device information collector
collector = DeviceInfoCollector()
device_info = collector.get_system_info()

# Advanced network scanning
scanner = NetworkScanner()
devices = scanner.scan_network(
    timeout=30,
    resolve_hostnames=True,
    get_vendor_info=True,
    port_scan=True
)
```

### Configuration & Customization

```python
# Configure monitoring
monitor_config = {
    'interval': 60,
    'metrics': ['cpu', 'memory', 'disk', 'network'],
    'thresholds': {
        'cpu_warning': 80,
        'memory_critical': 95
    },
    'export_format': 'json',
    'data_retention_days': 30
}

monitor = syinfo.create_system_monitor(**monitor_config)
```

### Data Export & Integration

```python
# Export system information
json_data = syinfo.export_system_info('json')
yaml_data = syinfo.export_system_info('yaml', output_file='system.yaml')

# Integration with monitoring systems
data = syinfo.get_system_info()
# Send to Prometheus, InfluxDB, etc.
```

## Architecture & Design

### Clean Architecture
- **Core Domain**: Pure business logic, no external dependencies
- **Application Layer**: Use cases and application services  
- **Infrastructure**: External integrations, file systems, networks
- **Interfaces**: Clean APIs and abstractions

### SOLID Principles
- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Derived classes are substitutable
- **Interface Segregation**: Many specific interfaces
- **Dependency Inversion**: Depend on abstractions

### Error Handling Strategy
```python
# Hierarchical exception handling
SyInfoException
├── ConfigurationError
├── DataCollectionError
├── NetworkError
├── SystemAccessError
├── ValidationError
├── MonitoringError
└── StorageError
```

## Testing & Quality

### Comprehensive Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=syinfo --cov-report=html

# Run performance tests
pytest tests/performance/

# Run security tests
bandit -r syinfo
```

### Code Quality Tools
- **Black**: Code formatting
- **isort**: Import sorting  
- **Ruff**: Fast Python linting
- **MyPy**: Static type checking
- **Bandit**: Security scanning
- **Pre-commit**: Git hooks for quality

## Documentation

### API Reference
- [Core API](docs/api/core.md) - Basic system information
- [Monitoring API](docs/api/monitoring.md) - Real-time monitoring
- [Network API](docs/api/network.md) - Network operations
- [CLI Reference](docs/cli/index.md) - Command line tools

### Guides
- [Installation Guide](docs/installation.md)
- [Quick Start Tutorial](docs/quickstart.md)
- [Advanced Usage](docs/advanced.md)
- [Contributing](CONTRIBUTING.md)

### Examples
- [Basic Usage](examples/basic_usage.py)
- [Monitoring Setup](examples/monitoring_example.py)
- [Network Discovery](examples/network_example.py)
- [Data Export](examples/export_example.py)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/MR901/syinfo.git
cd syinfo
python -m venv venv
source venv/bin/activate
pip install -e .[dev,full]
pre-commit install
```

### Code Standards
- Follow PEP 8 and use type hints
- Write comprehensive tests (>80% coverage)
- Update documentation for changes
- Use semantic commit messages

## Roadmap

### Version 0.3.0
- Windows and macOS support
- Docker container information
- Cloud provider metadata
- GraphQL API endpoint
- Real-time web dashboard

### Version 0.4.0
- Machine learning anomaly detection
- Predictive failure analysis
- Custom plugin system
- REST API server mode
- Kubernetes integration

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **psutil** - Cross-platform system and process utilities
- **GPUtil** - GPU monitoring capabilities
- **scapy** - Network packet manipulation
- **tabulate** - Pretty-print tabular data

## Support

- **Documentation**: [https://syinfo.readthedocs.io](https://syinfo.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/MR901/syinfo/issues)  
- **Discussions**: [GitHub Discussions](https://github.com/MR901/syinfo/discussions)
- **Email**: mohitrajput901@gmail.com
