Getting Started
==============

This guide will help you get up and running with SyInfo quickly.

Installation
-----------

First, install SyInfo:

.. code-block:: bash

   # Basic installation (system information only)
   pip install syinfo
   
   # Full installation (with monitoring features)
   pip install syinfo[monitoring]

Verify the installation:

.. code-block:: bash

   syinfo --version
   syinfo --help

Basic Usage
----------

**Python Library**

.. code-block:: python

   from syinfo import DeviceInfo, NetworkInfo, SysInfo
   
   # Get device information
   device_info = DeviceInfo.get_all()
   print(f"Hostname: {device_info['hostname']}")
   print(f"Platform: {device_info['platform']}")
   print(f"Architecture: {device_info['architecture']}")
   
   # Get network information
   network_info = NetworkInfo.get_all()
   print(f"Network interfaces: {list(network_info['interfaces'].keys())}")
   
   # Get combined system information
   system_info = SysInfo.get_all()
   print(f"System summary: {system_info.keys()}")

**Command Line**

.. code-block:: bash

   # Legacy commands (backward compatible)
   syinfo -d                    # Device information
   syinfo -n                    # Network information
   syinfo -s                    # System information
   
   # New subcommand structure
   syinfo info --device         # Device information
   syinfo info --network        # Network information
   syinfo info --system         # System information

Your First Monitoring Session
----------------------------

If you installed with monitoring features, you can start monitoring your system:

**Start Monitoring**

.. code-block:: bash

   # Start monitoring with default settings
   syinfo monitor --start
   
   # Start with custom interval (30 seconds)
   syinfo monitor --start --interval 30
   
   # Start monitoring for 1 hour
   syinfo monitor --start --interval 60 --duration 3600

**Check Status**

.. code-block:: bash

   # Get current monitoring status
   syinfo monitor --status
   
   # Collect one-time snapshot
   syinfo monitor --collect

**Stop Monitoring**

.. code-block:: bash

   # Stop monitoring
   syinfo monitor --stop

**Analyze Data**

.. code-block:: bash

   # Analyze trends in collected data
   syinfo analyze --trends --data-file monitoring_data.csv
   
   # Detect anomalies
   syinfo analyze --anomalies --data-file monitoring_data.csv
   
   # Create visualization dashboard
   syinfo analyze --dashboard --data-file monitoring_data.csv

Python API for Monitoring
------------------------

.. code-block:: python

   from syinfo.api import MonitoringAPI
   
   # Initialize API
   api = MonitoringAPI()
   
   # Start monitoring
   result = api.start_monitoring(interval=60)
   if result["success"]:
       print("Monitoring started successfully")
   
   # Get current statistics
   stats = api.get_current_stats()
   if stats["success"]:
       data = stats["data"]
       print(f"CPU Usage: {data['cpu_percent']}%")
       print(f"Memory Usage: {data['memory_percent']}%")
       print(f"Disk Usage: {data['disk_percent']}%")

Configuration
-------------

**Create Configuration File**

.. code-block:: bash

   # Create default configuration
   syinfo setup --create-config
   
   # Create with custom path
   syinfo setup --create-config --output-path my_config.yaml

**Setup Monitoring Directories**

.. code-block:: bash

   # Setup default directories
   syinfo setup --setup-dirs
   
   # Setup with custom path
   syinfo setup --setup-dirs --base-path /opt/monitoring

**Install Automated Monitoring**

.. code-block:: bash

   # Install cron job for continuous monitoring
   syinfo setup --install-cron
   
   # Install with custom interval (5 minutes)
   syinfo setup --install-cron --interval-minutes 5

Example Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   monitoring:
     interval: 60
     output_dir: ./monitoring_data
     include_processes: true
     include_logs: false
   
   collectors:
     system:
       enabled: true
       metrics: [cpu, memory, disk, network]
     process:
       enabled: true
       max_processes: 100
     log:
       enabled: false
       log_files: []
     storage:
       enabled: true
   
   analysis:
     trends:
       enabled: true
       window_size: 10
     anomalies:
       enabled: true
       threshold: 2.0
   
   visualization:
     enabled: true
     output_format: png
     chart_types: [cpu_usage, memory_usage, disk_usage]

Common Use Cases
---------------

**System Information Gathering**

.. code-block:: python

   from syinfo import SysInfo
   
   # Get comprehensive system information
   info = SysInfo.get_all(search_period=10)
   
   # Print formatted output
   SysInfo.print(info)
   
   # Save as JSON
   import json
   with open('system_info.json', 'w') as f:
       json.dump(info, f, indent=2)

**Continuous Monitoring**

.. code-block:: python

   from syinfo.api import MonitoringAPI
   import time
   
   api = MonitoringAPI()
   
   # Start monitoring
   api.start_monitoring(interval=30)
   
   try:
       while True:
           # Get current stats every minute
           stats = api.get_current_stats()
           if stats["success"]:
               data = stats["data"]
               print(f"CPU: {data['cpu_percent']}%, "
                     f"Memory: {data['memory_percent']}%, "
                     f"Disk: {data['disk_percent']}%")
           time.sleep(60)
   except KeyboardInterrupt:
       # Stop monitoring
       api.stop_monitoring()
       print("Monitoring stopped")

**Data Analysis**

.. code-block:: python

   from syinfo.api import AnalysisAPI
   
   api = AnalysisAPI()
   
   # Analyze trends
   trends = api.analyze_trends("monitoring_data.csv")
   if trends["success"]:
       print("Trend analysis:", trends["data"])
   
   # Detect anomalies
   anomalies = api.detect_anomalies("monitoring_data.csv")
   if anomalies["success"]:
       print("Anomalies detected:", anomalies["data"])

**Automated Reporting**

.. code-block:: python

   from syinfo.api import MonitoringAPI, AnalysisAPI
   import schedule
   import time
   
   def generate_daily_report():
       # Collect current data
       monitor_api = MonitoringAPI()
       data = monitor_api.collect_snapshot()
       
       # Analyze trends
       analysis_api = AnalysisAPI()
       trends = analysis_api.analyze_trends("daily_data.csv")
       
       # Generate report
       report = analysis_api.generate_report("daily_data.csv", "daily_report.json")
       print("Daily report generated")
   
   # Schedule daily report at 9 AM
   schedule.every().day.at("09:00").do(generate_daily_report)
   
   while True:
       schedule.run_pending()
       time.sleep(60)

Troubleshooting
--------------

**Check Feature Availability**

.. code-block:: python

   from syinfo import MONITORING_AVAILABLE
   print(f"Monitoring features available: {MONITORING_AVAILABLE}")

**Test Basic Functionality**

.. code-block:: bash

   # Test device info
   syinfo info --device
   
   # Test network info
   syinfo info --network
   
   # Test system info
   syinfo info --system

**Check Dependencies**

.. code-block:: bash

   # Check if monitoring dependencies are installed
   python -c "import psutil, matplotlib, pandas; print('All dependencies available')"

**Common Issues**

* **Import errors**: Install with monitoring extras
* **Permission errors**: Use `--user` flag or sudo
* **Missing dependencies**: Install required packages manually

Next Steps
----------

* **System Information**: :doc:`system_information`
* **Monitoring**: :doc:`monitoring`
* **Analysis**: :doc:`analysis`
* **Visualization**: :doc:`visualization`
* **API Reference**: :doc:`../api/index`
* **CLI Reference**: :doc:`../cli/index` 