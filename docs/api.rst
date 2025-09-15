API Reference
=============

Core Functions
--------------

System Information
~~~~~~~~~~~~~~~~~~

.. autofunction:: syinfo.get_system_info

.. autofunction:: syinfo.get_complete_info

.. autofunction:: syinfo.get_hardware_info

.. autofunction:: syinfo.get_network_info

.. autofunction:: syinfo.discover_network_devices

Display Functions
~~~~~~~~~~~~~~~~~

.. autofunction:: syinfo.print_system_tree

.. autofunction:: syinfo.print_brief_info

Export Functions
~~~~~~~~~~~~~~~~

.. autofunction:: syinfo.export_system_info

Feature Detection
~~~~~~~~~~~~~~~~~

.. autofunction:: syinfo.get_available_features

.. autofunction:: syinfo.print_feature_status

Logging Classes
~~~~~~~~~~~~~~~

.. autoclass:: syinfo.Logger
   :members: get_logger, get_instance

Monitoring Functions (New!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: syinfo.create_system_monitor

Create a simple system monitor for real-time performance tracking.

**Example:**

.. code-block:: python

   import syinfo
   import time
   
   # Create monitor with 5-second intervals
   monitor = syinfo.create_system_monitor(interval=5)
   
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

.. autoexception:: syinfo.exceptions.NetworkError

.. autoexception:: syinfo.exceptions.SystemAccessError

.. autoexception:: syinfo.exceptions.ValidationError

.. autoexception:: syinfo.exceptions.ConfigurationError

Constants
---------

.. automodule:: syinfo.constants
   :members:

Usage Examples
--------------

Basic System Information:

.. code-block:: python

   import syinfo
   
   # Get basic system info
   info = syinfo.get_system_info()
   print(f"OS: {info['system_name']}")
   print(f"CPU: {info['cpu_model']}")
   
   # Get complete information
   complete = syinfo.get_complete_info(include_network=True)
   
   # Pretty print system tree
   syinfo.print_system_tree()

Hardware Details:

.. code-block:: python

   # Get hardware information
   hardware = syinfo.get_hardware_info()
   
   cpu_info = hardware['cpu']
   memory_info = hardware['memory']
   
   print(f"CPU Cores: {cpu_info['cores_physical']}")
   print(f"Memory Total: {memory_info['total']}")

Network Operations:

.. code-block:: python

   # Discover network devices
   devices = syinfo.discover_network_devices(timeout=10)
   
   for device in devices:
       print(f"{device['ip']} - {device['hostname']}")

Data Export:

.. code-block:: python

   # Export as JSON
   json_data = syinfo.export_system_info('json')
   
   # Export to file
   syinfo.export_system_info('yaml', output_file='system.yaml')

System Monitoring:

.. code-block:: python

   # Create and start monitor
   monitor = syinfo.create_system_monitor(interval=10)
   monitor = syinfo.create_system_monitor(interval=10)
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
   logger = syinfo.Logger.get_logger()
   logger.info("Application started")
   
   # Advanced configuration
   config = LoggerConfig(
       log_level=logging.DEBUG,
       log_files=["app.log"],
       enable_incident_counting=True,
       enable_traceback=True
   )
   logger = syinfo.Logger.get_logger(config)
   
   # Runtime management
   logger_instance = syinfo.Logger.get_instance()
   stats = logger_instance.get_stats()
   print(f"Warnings: {stats['warning_count']}")

Error Handling:

.. code-block:: python

   from syinfo.exceptions import SystemAccessError, DataCollectionError
   
   logger = syinfo.Logger.get_logger()
   
   try:
       info = syinfo.get_system_info()
       logger.info("System info collected successfully")
   except SystemAccessError as e:
       logger.error(f"Permission error: {e}")
   except DataCollectionError as e:
       logger.error(f"Collection failed: {e}")
