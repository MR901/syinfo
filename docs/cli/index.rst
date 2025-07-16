Command Line Interface
=====================

SyInfo provides a comprehensive command-line interface with both legacy and new subcommand structures.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   legacy_commands
   subcommands
   options
   examples

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

   # Start monitoring with 30-second interval
   syinfo monitor --start --interval 30
   
   # Start monitoring for 1 hour
   syinfo monitor --start --interval 60 --duration 3600
   
   # Check monitoring status
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
   syinfo monitor --start --verbose

**Filtering and Options**

.. code-block:: bash

   # Monitor specific processes
   syinfo monitor --start --process-filter "python|node"
   
   # Monitor specific metrics
   syinfo monitor --start --metrics cpu,memory,disk
   
   # Custom output directory
   syinfo monitor --start --output-dir /opt/monitoring

**Integration with Scripts**

.. code-block:: bash

   # Check if monitoring is running
   if syinfo monitor --status --quiet; then
       echo "Monitoring is active"
   else
       echo "Starting monitoring..."
       syinfo monitor --start
   fi
   
   # Collect data and analyze
   syinfo monitor --collect --output current_data.csv
   syinfo analyze --trends --data-file current_data.csv

Error Handling
-------------

**Common Error Codes**

* `0` - Success
* `1` - General error
* `2` - Configuration error
* `3` - Permission error
* `4` - Dependency error

**Error Messages**

.. code-block:: bash

   # Check for errors
   syinfo monitor --start 2>&1 | grep -i error
   
   # Verbose error output
   syinfo monitor --start --verbose 2>&1

**Troubleshooting**

.. code-block:: bash

   # Check version and dependencies
   syinfo --version
   python -c "import syinfo; print(syinfo.MONITORING_AVAILABLE)"
   
   # Test basic functionality
   syinfo info --device
   
   # Check configuration
   syinfo setup --create-config --dry-run

Next Steps
---------

* **Legacy Commands**: :doc:`legacy_commands`
* **Subcommands**: :doc:`subcommands`
* **Options**: :doc:`options`
* **Examples**: :doc:`examples` 