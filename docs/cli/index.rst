Command Line Interface
=====================

SyInfo provides a comprehensive command-line interface with both legacy and new subcommand structures.

Overview
--------

SyInfo CLI supports two command structures:

* **Legacy Commands**: Original single-flag commands (backward compatible)
* **Subcommands**: New organized command structure with better organization

Basic Usage
----------

**Legacy Commands**

.. code-block:: bash

   syinfo -d                    # Device information
   syinfo -n                    # Network information
   syinfo -s                    # System information
   syinfo --help                # Show help
   syinfo --version             # Show version

**New Subcommands**

.. code-block:: bash

   syinfo info --device         # Device information
   syinfo info --network        # Network information
   syinfo info --system         # System information
   syinfo monitor --start       # Start monitoring
   syinfo analyze --trends      # Analyze trends
   syinfo setup --create-config # Create configuration

Command Categories
-----------------

**Information Commands**

* `info` - System information gathering
* `--device` - Device information
* `--network` - Network information
* `--system` - System information

**Monitoring Commands**

* `monitor` - System monitoring
* `--start` - Start monitoring
* `--stop` - Stop monitoring
* `--status` - Check status
* `--collect` - Collect snapshot

**Analysis Commands**

* `analyze` - Data analysis
* `--trends` - Analyze trends
* `--anomalies` - Detect anomalies
* `--dashboard` - Create dashboard

**Setup Commands**

* `setup` - Configuration and setup
* `--create-config` - Create configuration file
* `--setup-dirs` - Setup directories
* `--install-cron` - Install cron job

Global Options
-------------

**Common Options**

.. code-block:: bash

   syinfo --help                # Show help
   syinfo --version             # Show version
   syinfo --verbose             # Verbose output
   syinfo --quiet               # Quiet output
   syinfo --config FILE         # Use config file
   syinfo --output FILE         # Output to file
   syinfo --format FORMAT       # Output format (json, csv, table)

**Output Formats**

* `json` - JSON format
* `csv` - CSV format
* `table` - Formatted table
* `yaml` - YAML format

Examples
--------

**System Information**

.. code-block:: bash

   # Get device information
   syinfo info --device
   
   # Get network information in JSON format
   syinfo info --network --format json
   
   # Get system information and save to file
   syinfo info --system --output system_info.json

**Monitoring**

.. code-block:: bash

   # Start monitoring with 30second interval
   syinfo monitor --start --interval30# Start monitoring for 1 hour
   syinfo monitor --start --interval 60duration 3600# Check monitoring status
   syinfo monitor --status
   
   # Collect one-time snapshot
   syinfo monitor --collect --output snapshot.csv

**Analysis**

.. code-block:: bash

   # Analyze trends in monitoring data
   syinfo analyze --trends --data-file monitoring_data.csv
   
   # Detect anomalies
   syinfo analyze --anomalies --data-file monitoring_data.csv
   
   # Create dashboard
   syinfo analyze --dashboard --data-file monitoring_data.csv --output dashboard.html

**Setup and Configuration**

.. code-block:: bash

   # Create default configuration
   syinfo setup --create-config
   
   # Create configuration with custom path
   syinfo setup --create-config --output-path my_config.yaml
   
   # Setup monitoring directories
   syinfo setup --setup-dirs
   
   # Install cron job for continuous monitoring
   syinfo setup --install-cron --interval-minutes 5

**Legacy Commands (Backward Compatible)**

.. code-block:: bash

   # Device information
   syinfo -d
   
   # Network information
   syinfo -n
   
   # System information
   syinfo -s
   
   # Combined information
   syinfo -d -n -s

Advanced Usage
-------------

**Configuration Files**

.. code-block:: bash

   # Use custom configuration
   syinfo monitor --start --config my_config.yaml
   
   # Create configuration from template
   syinfo setup --create-config --template production

**Output and Formatting**

.. code-block:: bash

   # Save output to file
   syinfo info --system --output system_info.json
   
   # Use specific format
   syinfo info --device --format csv
   
   # Verbose output
   syinfo info --system --verbose

**Monitoring with Custom Settings**

.. code-block:: bash

   # Start monitoring with custom interval
   syinfo monitor --start --interval 30--output-dir ./monitoring_data
   
   # Monitor specific metrics only
   syinfo monitor --start --metrics cpu,memory,disk
   
   # Start monitoring with alerts
   syinfo monitor --start --alerts --threshold 80dling
-------------

**Common Error Scenarios**

.. code-block:: bash

   # Permission denied
   sudo syinfo info --system
   
   # Configuration file not found
   syinfo monitor --start --config /path/to/config.yaml
   
   # Invalid format
   syinfo info --device --format invalid_format
   
   # Output directory doesnt exist
   syinfo monitor --start --output-dir /path/to/output

**Debugging**

.. code-block:: bash

   # Enable debug mode
   syinfo info --device --debug
   
   # Show detailed error messages
   syinfo monitor --start --verbose --debug
   
   # Check configuration
   syinfo setup --validate-config

Next Steps
----------

* :doc:`../user_guide/getting_started` - Get started with SyInfo
* :doc:`../api/index` - Learn about the API
* :doc:`../installation` - Installation guide 