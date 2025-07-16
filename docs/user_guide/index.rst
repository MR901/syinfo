User Guide
==========

Welcome to the SyInfo User Guide! This guide will help you get started with SyInfo and learn how to use its features effectively.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   system_information
   monitoring
   analysis
   visualization
   automation
   configuration
   troubleshooting

What is SyInfo?
--------------

SyInfo is a comprehensive system information and monitoring tool that provides:

* **System Information**: Detailed device, network, and system information
* **Real-time Monitoring**: Continuous monitoring of system resources
* **Data Analysis**: Trend analysis and anomaly detection
* **Visualization**: Charts and dashboards for system metrics
* **Automation**: Scheduled monitoring with cron jobs
* **Dual Interface**: Both Python library and command-line tool

Key Concepts
-----------

**Legacy Mode vs Monitoring Mode**

SyInfo operates in two modes:

* **Legacy Mode**: Original system information gathering (backward compatible)
* **Monitoring Mode**: Advanced monitoring and analysis capabilities

**Dual Interface**

* **Python Library**: Programmatic access to all features
* **Command Line**: Interactive and scriptable interface

**Feature Availability**

* **Core Features**: Always available (system information)
* **Monitoring Features**: Available with full installation

Quick Examples
-------------

**Basic System Information**

.. code-block:: python

   from syinfo import DeviceInfo, NetworkInfo, SysInfo
   
   # Get device information
   device = DeviceInfo.get_all()
   print(f"Hostname: {device['hostname']}")
   print(f"Platform: {device['platform']}")

**Command Line Usage**

.. code-block:: bash

   # Legacy commands
   syinfo -d                    # Device info
   syinfo -n                    # Network info
   syinfo -s                    # System info
   
   # New subcommands
   syinfo info --device         # Device info
   syinfo monitor --start       # Start monitoring
   syinfo analyze --trends      # Analyze trends

**Real-time Monitoring**

.. code-block:: python

   from syinfo.api import MonitoringAPI
   
   api = MonitoringAPI()
   api.start_monitoring(interval=60)
   
   # Get current stats
   stats = api.get_current_stats()
   print(f"CPU: {stats['cpu_percent']}%")
   print(f"Memory: {stats['memory_percent']}%")

Getting Started
--------------

1. **Install SyInfo**: See :doc:`../installation`
2. **Read Getting Started**: :doc:`getting_started`
3. **Explore System Information**: :doc:`system_information`
4. **Try Monitoring**: :doc:`monitoring`
5. **Analyze Data**: :doc:`analysis`
6. **Create Visualizations**: :doc:`visualization`

System Requirements
------------------

* **Python**: 3.7 or higher
* **Operating System**: Linux, macOS, Windows
* **Memory**: 100MB minimum (more for monitoring)
* **Storage**: 50MB for installation, additional for data storage

Installation Options
-------------------

* **Basic**: Core system information features
* **Full**: Includes monitoring and analysis
* **Development**: For contributing to the project

.. code-block:: bash

   # Basic installation
   pip install syinfo
   
   # Full installation
   pip install syinfo[monitoring]
   
   # Development installation
   git clone https://github.com/MR901/syinfo.git
   cd syinfo
   pip install -e .

Next Steps
----------

* **Getting Started**: :doc:`getting_started`
* **System Information**: :doc:`system_information`
* **Monitoring**: :doc:`monitoring`
* **API Reference**: :doc:`../api/index`
* **CLI Reference**: :doc:`../cli/index` 