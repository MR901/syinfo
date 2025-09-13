# SyInfo Examples

Simple examples demonstrating SyInfo's core functionality.

## Files

### `basic_system_info.py`
Demonstrates core system information collection:
- Device information (CPU, memory, disk)
- Network information
- Basic system details

### `api_example.py`
Shows how to use the complete SyInfo API:
- System information functions
- Hardware details
- Export capabilities

### `cli_examples.py`
Examples of using the command-line interface:
- Various CLI commands
- Output formatting options

### `simple_monitoring.py`
Demonstrates the simplified monitoring features:
- Creating a simple monitor
- Collecting performance data
- Getting monitoring results

## Running Examples

```bash
# Run from the examples directory
cd examples

# Basic functionality
python basic_system_info.py

# API usage
python api_example.py

# CLI examples
python cli_examples.py

# Simple monitoring
python simple_monitoring.py
```

## Prerequisites

- Python 3.8+
- SyInfo installed (from parent directory: `pip install .`)
- For network features: `pip install syinfo[network]`
