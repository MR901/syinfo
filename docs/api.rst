API Reference
=============

Public API
----------

Logging
~~~~~~~

.. autoclass:: syinfo.utils.logger.Logger
   :members: get_logger, get_instance

Monitoring
~~~~~~~~~~

.. autoclass:: syinfo.resource_monitor.system_monitor.SystemMonitor
   :members:

.. autoclass:: syinfo.resource_monitor.process_monitoring.ProcessMonitor
   :members:

**Example:**

.. code-block:: python

   from syinfo import SystemMonitor
   import time
   
   # Create monitor with 5-second intervals
   monitor = SystemMonitor(interval=5)
   
   # Start monitoring for 60 seconds
   monitor.start(duration=60)
   time.sleep(61)
   
   # Get results
   results = monitor.stop()
   print(f"Average CPU: {results['summary']['cpu_avg']:.1f}%")
   print(f"Peak Memory: {results['summary']['memory_peak']:.1f}%")

SystemMonitor Class
~~~~~~~~~~~~~~~~~~~

The ``SystemMonitor`` class provides real-time system monitoring capabilities:

**Methods:**

- ``start(duration=None, callback=None)`` - Start monitoring
- ``stop()`` - Stop monitoring and return results
- ``is_running`` - Check if monitoring is active
- ``data_points`` - List of collected data points

**Data Structure:**

.. code-block:: python

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

Core Classes
------------

DeviceInfo
~~~~~~~~~~

.. autoclass:: syinfo.core.device_info.DeviceInfo
   :members:

NetworkInfo
~~~~~~~~~~~

.. autoclass:: syinfo.core.network_info.NetworkInfo
   :members:

SystemInfo
~~~~~~~~~~

.. autoclass:: syinfo.core.system_info.SystemInfo
   :members:

Logging Classes
---------------

Logger
~~~~~~

.. autoclass:: syinfo.utils.logger.Logger
   :members:

LoggerConfig  
~~~~~~~~~~~~

.. autoclass:: syinfo.utils.logger.LoggerConfig
   :members:

Exceptions
----------

.. autoexception:: syinfo.exceptions.SyInfoException

.. autoexception:: syinfo.exceptions.DataCollectionError

.. autoexception:: syinfo.exceptions.SystemAccessError

.. autoexception:: syinfo.exceptions.ValidationError

Constants
---------

.. automodule:: syinfo.constants
   :members:

Usage Examples
--------------

Basic System Information:

.. code-block:: python

   from syinfo import DeviceInfo, SystemInfo
   
   # Get basic system info
   info = SystemInfo.get_all(search_period=0, search_device_vendor_too=False)
   print(f"OS: {info.get('dev_info', {}).get('system')}")

Hardware Details:

.. code-block:: python

   # Get hardware information
   hardware = DeviceInfo.get_all()
   
   cpu_info = hardware['cpu']
   memory_info = hardware['memory']
   
   print(f"CPU Cores: {cpu_info['cores_physical']}")
   print(f"Memory Total: {memory_info['total']}")

Network Operations:

.. code-block:: python

   # Discover network devices (sudo recommended)
   from syinfo.core.search_network import search_devices_on_network
   devices = search_devices_on_network(time=5, seach_device_vendor_too=False)
   for ip, dev in devices.items():
       print(f"{ip} - {dev.get('mac_address')}")

Data Export:

.. code-block:: python

   # Export as JSON/YAML
   from syinfo.utils.export import export_data
   json_data = export_data(hardware, format='json')
   yaml_data = export_data(hardware, format='yaml')

System Monitoring:

.. code-block:: python

   # Create and start monitor
   from syinfo import SystemMonitor
   monitor = SystemMonitor(interval=10)
   monitor.start(duration=300)  # 5 minutes
   
   # Wait and get results
   import time
   time.sleep(301)
   results = monitor.stop()
   
   # Analyze results
   summary = results['summary']
   print(f"Average CPU: {summary['cpu_avg']:.1f}%")
   print(f"Peak Memory: {summary['memory_peak']:.1f}%")
   print(f"Duration: {summary['duration_seconds']} seconds")
   
   # Process individual data points
   for point in results['data_points']:
       if point['cpu_percent'] > 80:
           print(f"High CPU at {point['timestamp']}: {point['cpu_percent']:.1f}%")

Logging Usage:

.. code-block:: python

   from syinfo import Logger, LoggerConfig
   import logging
   
   # Basic logging
   logger = Logger.get_logger()
   logger.info("Application started")
   
   # Advanced configuration
   config = LoggerConfig(
       log_level=logging.DEBUG,
       log_files=["app.log"],
       enable_incident_counting=True,
       enable_traceback=True
   )
   logger = Logger.get_logger(config)
   
   # Runtime management
   logger_instance = Logger.get_instance()
   stats = logger_instance.get_stats()
   print(f"Warnings: {stats['warning_count']}")

Error Handling:

.. code-block:: python

   from syinfo.exceptions import SystemAccessError, DataCollectionError
   from syinfo import Logger, SystemInfo
   
   logger = Logger.get_logger()
   
   try:
       info = SystemInfo.get_all(search_period=0, search_device_vendor_too=False)
       logger.info("System info collected successfully")
   except SystemAccessError as e:
       logger.error(f"Permission error: {e}")
   except DataCollectionError as e:
       logger.error(f"Collection failed: {e}")
