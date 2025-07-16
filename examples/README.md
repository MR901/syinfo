# SyInfo Examples

This directory contains comprehensive examples demonstrating how to use SyInfo's system information and monitoring features.

## 📁 Example Files

### 1. `basic_system_info.py`
**Purpose:** Demonstrates basic system information collection using SyInfo's core features.

**Features:**
- System information (OS, kernel, architecture, hostname, uptime)
- Device information (CPU, memory, disk details)
- Network information (interfaces, statistics)
- Legacy compatibility functions

**Usage:**
```bash
cd examples
python basic_system_info.py
```

### 2. `monitoring_example.py`
**Purpose:** Demonstrates SyInfo's monitoring capabilities including real-time system and process monitoring.

**Features:**
- System monitoring (CPU, memory, disk, network metrics)
- Process monitoring (top processes, resource usage)
- Data collection and storage
- Performance analysis
- Continuous monitoring with configurable intervals

**Usage:**
```bash
cd examples
python monitoring_example.py
```

### 3. `cli_examples.py`
**Purpose:** Shows how to use SyInfo's command-line interface both programmatically and via subprocess.

**Features:**
- Programmatic CLI command execution
- Command-line interface examples
- Subprocess integration
- Error handling and status checking

**Usage:**
```bash
cd examples
python cli_examples.py
```

### 4. `api_example.py`
**Purpose:** Demonstrates programmatic access to SyInfo's API features.

**Features:**
- Info API (system, device, network information)
- Monitoring API (metrics, process data, collection)
- Analysis API (performance, health, trends)
- Error handling and exception management

**Usage:**
```bash
cd examples
python api_example.py
```

### 5. `configuration_example.py`
**Purpose:** Shows how to configure and customize SyInfo monitoring settings.

**Features:**
- Basic, advanced, and custom configurations
- YAML configuration file creation
- Programmatic configuration
- Configuration comparison and validation

**Usage:**
```bash
cd examples
python configuration_example.py
```

## 🚀 Quick Start

1. **Install SyInfo:**
   ```bash
   pip install syinfo
   ```

2. **Run Basic Example:**
   ```bash
   cd examples
   python basic_system_info.py
   ```

3. **Run Monitoring Example:**
   ```bash
   python monitoring_example.py
   ```

4. **Explore CLI:**
   ```bash
   python cli_examples.py
   ```

## 📋 Prerequisites

- Python 3.7+
- SyInfo package installed
- Required dependencies (psutil, yaml, etc.)

## 🔧 Configuration

The examples use different configuration approaches:

- **Basic Configuration:** Minimal settings for simple monitoring
- **Advanced Configuration:** Comprehensive monitoring with alerts and detailed metrics
- **Custom Configuration:** Tailored settings for specific use cases

Configuration files are generated in the `examples/` directory and can be used with the main SyInfo application.

## 📊 Output Examples

### System Information Output
```
SyInfo - Basic System Information Example
============================================================

1. System Information:
------------------------------
OS: Linux
Kernel: 5.15.0-136-generic
Architecture: x86_64
Hostname: myhost
Uptime: 2 days, 3 hours, 45 minutes
```

### Monitoring Output
```
SyInfo - Monitoring Example
============================================================

1. System Monitoring:
------------------------------
Collecting system snapshot...
Timestamp: 2024-01-15T10:30:00
CPU Usage: 25.5%
Memory Usage: 67.2%
Disk Usage: 45.8%
Network Bytes Sent: 1024000
Network Bytes Received: 2048000
```

## 🛠️ Customization

Each example can be customized by:

1. **Modifying parameters** in the example scripts
2. **Creating custom configurations** using `configuration_example.py`
3. **Extending functionality** by adding new monitoring metrics
4. **Integrating with other tools** using the API examples

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors:**
   - Ensure SyInfo is installed: `pip install syinfo`
   - Check Python path and project structure

2. **Permission Errors:**
   - Some monitoring features may require elevated privileges
   - Check file permissions for data directories

3. **Configuration Errors:**
   - Validate YAML syntax in configuration files
   - Check file paths and permissions

### Debug Mode

Enable debug logging by setting the log level in configuration:
```yaml
logging:
  level: DEBUG
  console_output: true
```

## 📚 Additional Resources

- [SyInfo Documentation](../docs/)
- [API Reference](../docs/api/)
- [CLI Reference](../docs/cli/)
- [Installation Guide](../docs/installation.rst)

## 🤝 Contributing

To add new examples:

1. Create a new Python file in the `examples/` directory
2. Follow the existing naming convention and structure
3. Include comprehensive documentation and comments
4. Test the example thoroughly
5. Update this README with the new example

## 📄 License

These examples are part of the SyInfo project and follow the same license terms. 