API Reference
=============

This section provides comprehensive API documentation for SyInfo.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   core
   monitoring
   analysis
   cli_commands

Overview
--------

SyInfo provides several API layers:

* **Core API**: System information gathering (DeviceInfo, NetworkInfo, SysInfo)
* **Monitoring API**: Real-time system monitoring and data collection
* **Analysis API**: Data analysis and trend detection
* **CLI API**: Command-line interface commands

Core API
--------

The core API provides system information gathering capabilities.

**DeviceInfo**

.. code-block:: python

   from syinfo import DeviceInfo
   
   # Get all device information
   device_info = DeviceInfo.get_all()
   
   # Get specific information
   hostname = DeviceInfo.get_hostname()
   platform = DeviceInfo.get_platform()
   architecture = DeviceInfo.get_architecture()

**NetworkInfo**

.. code-block:: python

   from syinfo import NetworkInfo
   
   # Get all network information
   network_info = NetworkInfo.get_all()
   
   # Get specific information
   interfaces = NetworkInfo.get_interfaces()
   connections = NetworkInfo.get_connections()

**SysInfo**

.. code-block:: python

   from syinfo import SysInfo
   
   # Get comprehensive system information
   system_info = SysInfo.get_all(search_period=10)
   
   # Print formatted output
   SysInfo.print(system_info)

Monitoring API
-------------

The monitoring API provides real-time system monitoring capabilities.

**MonitoringAPI**

.. code-block:: python

   from syinfo.api import MonitoringAPI
   
   api = MonitoringAPI()
   
   # Start monitoring
   result = api.start_monitoring(interval=60)
   
   # Get current statistics
   stats = api.get_current_stats()
   
   # Stop monitoring
   api.stop_monitoring()

Analysis API
-----------

The analysis API provides data analysis and trend detection.

**AnalysisAPI**

.. code-block:: python

   from syinfo.api import AnalysisAPI
   
   api = AnalysisAPI()
   
   # Analyze trends
   trends = api.analyze_trends("data.csv")
   
   # Detect anomalies
   anomalies = api.detect_anomalies("data.csv")

CLI Commands
-----------

The CLI provides command-line access to all features.

**Legacy Commands**

.. code-block:: bash

   syinfo -d                    # Device information
   syinfo -n                    # Network information
   syinfo -s                    # System information

**New Subcommands**

.. code-block:: bash

   syinfo info --device         # Device information
   syinfo monitor --start       # Start monitoring
   syinfo analyze --trends      # Analyze trends

Quick Reference
--------------

**Core Classes**

* :class:`syinfo.DeviceInfo` - Device information gathering
* :class:`syinfo.NetworkInfo` - Network information gathering
* :class:`syinfo.SysInfo` - System information gathering

**Monitoring Classes**

* :class:`syinfo.monitoring.core.SystemMonitor` - System monitoring
* :class:`syinfo.monitoring.core.ProcessMonitor` - Process monitoring
* :class:`syinfo.monitoring.data.DataCollector` - Data collection
* :class:`syinfo.monitoring.data.DataAnalyzer` - Data analysis
* :class:`syinfo.monitoring.data.DataVisualizer` - Data visualization

**API Classes**

* :class:`syinfo.api.MonitoringAPI` - Monitoring API
* :class:`syinfo.api.AnalysisAPI` - Analysis API
* :class:`syinfo.api.InfoAPI` - Information API

**Utility Classes**

* :class:`syinfo.monitoring.utils.MonitoringConfig` - Configuration management
* :class:`syinfo.monitoring.utils.MonitoringLogger` - Logging
* :class:`syinfo.monitoring.scheduler.CronManager` - Cron job management

**Constants**

* :data:`syinfo.MONITORING_AVAILABLE` - Feature availability flag
* :data:`syinfo.__version__` - Package version

Examples
--------

**Basic System Information**

.. code-block:: python

   from syinfo import DeviceInfo, NetworkInfo, SysInfo
   
   # Get device information
   device = DeviceInfo.get_all()
   print(f"Hostname: {device['hostname']}")
   print(f"Platform: {device['platform']}")
   
   # Get network information
   network = NetworkInfo.get_all()
   print(f"Interfaces: {list(network['interfaces'].keys())}")
   
   # Get system information
   system = SysInfo.get_all()
   print(f"System info: {system.keys()}")

**Real-time Monitoring**

.. code-block:: python

   from syinfo.api import MonitoringAPI
   import time
   
   api = MonitoringAPI()
   
   # Start monitoring
   api.start_monitoring(interval=30)
   
   try:
       for _ in range(10):
           stats = api.get_current_stats()
           if stats["success"]:
               data = stats["data"]
               print(f"CPU: {data['cpu_percent']}%, "
                     f"Memory: {data['memory_percent']}%")
           time.sleep(60)
   finally:
       api.stop_monitoring()

**Data Analysis**

.. code-block:: python

   from syinfo.api import AnalysisAPI
   
   api = AnalysisAPI()
   
   # Analyze trends
   trends = api.analyze_trends("monitoring_data.csv")
   if trends["success"]:
       print("Trends:", trends["data"])
   
   # Detect anomalies
   anomalies = api.detect_anomalies("monitoring_data.csv")
   if anomalies["success"]:
       print("Anomalies:", anomalies["data"])

**Configuration Management**

.. code-block:: python

   from syinfo.monitoring.utils import MonitoringConfig
   
   # Load configuration
   config = MonitoringConfig("config.yaml")
   
   # Get monitoring settings
   interval = config.get("monitoring.interval", 60)
   output_dir = config.get("monitoring.output_dir", "./data")
   
   # Update configuration
   config.set("monitoring.interval", 30)
   config.save()

Next Steps
---------

* **Core API**: :doc:`core`
* **Monitoring API**: :doc:`monitoring`
* **Analysis API**: :doc:`analysis`
* **CLI Commands**: :doc:`cli_commands` 