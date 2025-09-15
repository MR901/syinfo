Logging with SyInfo
===================

SyInfo includes a sophisticated, production-ready logging system designed specifically for Python packages. The logger provides advanced features while maintaining simplicity for basic usage.

Quick Start
-----------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   import syinfo
   
   # Get default logger
   logger = syinfo.Logger.get_logger()
   
   # Use standard logging methods
   logger.debug("Debug information")
   logger.info("General information")
   logger.warning("Warning message")
   logger.error("Error occurred")
   logger.critical("Critical error")

Advanced Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from syinfo import Logger, LoggerConfig
   import logging
   
   # Create advanced configuration
   config = LoggerConfig(
       log_level=logging.DEBUG,
       log_files=["app.log", "debug.log"],
       output_to_stdout=True,
       verbose_logs=True,
       enable_incident_counting=True,
       enable_traceback=True,
       enable_syslog=True
   )
   
   # Get configured logger
   logger = Logger.get_logger(config)

Logger Features
---------------

Singleton Pattern
~~~~~~~~~~~~~~~~~

SyInfo's logger uses a singleton pattern, ensuring all parts of your application share the same logger configuration:

.. code-block:: python

   logger1 = syinfo.Logger.get_logger()
   logger2 = syinfo.Logger.get_logger()
   
   # Both are the same instance
   assert logger1 is logger2

Incident Counting
~~~~~~~~~~~~~~~~~

Automatically numbers warnings and errors for easier tracking:

.. code-block:: python

   config = LoggerConfig(enable_incident_counting=True)
   logger = syinfo.Logger.get_logger(config)
   
   logger.warning("First issue")     # (incident #1) First issue
   logger.warning("Second issue")    # (incident #2) Second issue
   logger.error("Critical problem")  # (incident #1) Critical problem

Enhanced Tracebacks
~~~~~~~~~~~~~~~~~~~

Beautiful, readable tracebacks with file context:

.. code-block:: python

   config = LoggerConfig(enable_traceback=True)
   logger = syinfo.Logger.get_logger(config)
   
   try:
       raise ValueError("Demo error")
   except ValueError:
       logger.error("Something went wrong")

Output:

.. code-block:: text

   2025-09-15 16:30:45 |    ERROR | Something went wrong
   ╭─ Traceback (ValueError)
   ├─ [1] demo.py:25 in main()
   │     raise ValueError("Demo error")
   ╰─ ValueError: Demo error

File Logging
~~~~~~~~~~~~

Support for multiple log files with automatic directory creation:

.. code-block:: python

   config = LoggerConfig(
       log_files=["logs/app.log", "logs/errors.log"],
       truncate_log_files=True  # Clear files on startup
   )
   logger = syinfo.Logger.get_logger(config)

System Logging (Syslog)
~~~~~~~~~~~~~~~~~~~~~~~

Integration with system logging facilities:

.. code-block:: python

   import logging.handlers
   
   config = LoggerConfig(
       enable_syslog=True,
       syslog_facility=logging.handlers.SysLogHandler.LOG_LOCAL0
   )
   logger = syinfo.Logger.get_logger(config)

The logger automatically detects the appropriate syslog socket based on your platform:

- **Linux**: ``/dev/log`` or ``/var/run/rsyslog/kmsg``
- **macOS**: ``/var/run/syslog``  
- **Windows**: Network syslog (``localhost:514``)

Verbose Logging
~~~~~~~~~~~~~~~

Include function names and line numbers in log messages:

.. code-block:: python

   config = LoggerConfig(verbose_logs=True)
   logger = syinfo.Logger.get_logger(config)
   
   logger.info("Processing data")

Output:

.. code-block:: text

   2025-09-15 16:30:45 |     INFO | process_data:142 | Processing data

Configuration Options
---------------------

LoggerConfig Class
~~~~~~~~~~~~~~~~~~

.. autoclass:: syinfo.utils.logger.LoggerConfig
   :members:
   :undoc-members:

**Parameters:**

- ``log_level`` (int): Minimum log level (DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50)
- ``log_files`` (List[str]): List of file paths to write logs to
- ``truncate_log_files`` (bool): Clear existing files on startup vs append
- ``output_to_stdout`` (bool): Show logs in console
- ``verbose_logs`` (bool): Include function names and line numbers
- ``enable_incident_counting`` (bool): Add numbers to warnings/errors
- ``enable_traceback`` (bool): Include Python tracebacks in errors
- ``enable_syslog`` (bool): Send logs to system syslog
- ``syslog_address`` (Union[str, Tuple[str, int]]): Syslog destination
- ``syslog_facility`` (int): Syslog facility (LOG_USER, LOG_LOCAL0-7, etc.)
- ``syslog_socktype`` (int): Socket type for network syslog (UDP/TCP)

Runtime Management
------------------

Dynamic Configuration
~~~~~~~~~~~~~~~~~~~~~

Change logger settings after initialization:

.. code-block:: python

   # Get logger instance for advanced operations
   logger_instance = syinfo.Logger.get_instance()
   
   # Change log level
   logger_instance.set_log_level("DEBUG")
   logger_instance.set_log_level(logging.WARNING)
   
   # Add new file handler
   logger_instance.add_file_handler("new_log.log", truncate=True)
   
   # Enable syslog dynamically
   logger_instance.enable_syslog()
   
   # Disable syslog
   logger_instance.disable_syslog()

Statistics and Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~

Track logger usage and performance:

.. code-block:: python

   logger_instance = syinfo.Logger.get_instance()
   
   # Get statistics
   stats = logger_instance.get_stats()
   print(f"Warnings: {stats['warning_count']}")
   print(f"Errors: {stats['error_count']}")
   print(f"Handlers: {stats['handlers']}")
   
   # Reset incident counters
   logger_instance.reset_incident_counters()

Handler Management
~~~~~~~~~~~~~~~~~~

Control specific handler types:

.. code-block:: python

   import logging
   
   logger_instance = syinfo.Logger.get_instance()
   
   # Remove all file handlers
   logger_instance.remove_handlers_by_type(logging.FileHandler)
   
   # Remove syslog handlers
   logger_instance.remove_handlers_by_type(logging.handlers.SysLogHandler)

Best Practices
--------------

Library Usage
~~~~~~~~~~~~~

When using SyInfo in your applications:

.. code-block:: python

   # Configure logging early in your application
   from syinfo import get_logger, LoggerConfig
   import logging
   
   # Set up logging before importing other modules
   config = LoggerConfig(
       log_level=logging.INFO,
       log_files=["app.log"],
       output_to_stdout=True,
       enable_incident_counting=True
   )
   
   logger = Logger.get_logger(config)
   logger.info("Application starting")
   
   # Now use SyInfo functionality
   import syinfo
   system_info = syinfo.get_system_info()

Production Deployment
~~~~~~~~~~~~~~~~~~~~~

Recommended configuration for production:

.. code-block:: python

   import logging.handlers
   from syinfo import LoggerConfig, get_logger
   
   config = LoggerConfig(
       log_level=logging.INFO,  # INFO level for production
       log_files=["/var/log/myapp/app.log"],
       output_to_stdout=False,  # Disable console in production
       verbose_logs=False,      # Clean logs for production
       enable_incident_counting=True,
       enable_traceback=True,
       enable_syslog=True,
       syslog_facility=logging.handlers.SysLogHandler.LOG_LOCAL0
   )
   
   logger = Logger.get_logger(config)

Development Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

Recommended for development and debugging:

.. code-block:: python

   import logging
   from syinfo import LoggerConfig, get_logger
   
   config = LoggerConfig(
       log_level=logging.DEBUG,  # Show all messages
       log_files=["debug.log"],
       output_to_stdout=True,    # See logs in console
       verbose_logs=True,        # Include function/line info
       enable_incident_counting=False,  # Cleaner output
       enable_traceback=True
   )
   
   logger = Logger.get_logger(config)

Integration Examples
--------------------

With SyInfo Monitoring
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from syinfo import get_logger, LoggerConfig, create_system_monitor
   import logging
   
   # Configure logger for monitoring
   config = LoggerConfig(
       log_level=logging.INFO,
       log_files=["monitoring.log"],
       output_to_stdout=True
   )
   logger = Logger.get_logger(config)
   
   # Start monitoring with logging
   logger.info("Starting system monitoring")
   monitor = create_system_monitor(interval=5)
   monitor.start(duration=60)
   
   # Monitoring will generate internal log messages
   import time
   time.sleep(61)
   
   results = monitor.stop()
   logger.info(f"Monitoring completed: {results['total_points']} data points")

With Error Handling
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from syinfo import Logger, get_system_info
   from syinfo.exceptions import SystemAccessError, DataCollectionError
   
   logger = Logger.get_logger()
   
   try:
       logger.info("Collecting system information")
       info = get_system_info()
       logger.info(f"Successfully collected info for {info.get('system_name')}")
       
   except SystemAccessError as e:
       logger.error(f"Permission denied: {e}")
       
   except DataCollectionError as e:
       logger.error(f"Data collection failed: {e}")
       
   except Exception as e:
       logger.error(f"Unexpected error: {e}")

API Reference
-------------

Functions
~~~~~~~~~

.. autoclass:: syinfo.utils.logger.Logger
   :members: get_logger, get_instance

Classes
~~~~~~~

.. autoclass:: syinfo.utils.logger.Logger
   :members:
   :undoc-members:

.. autoclass:: syinfo.utils.logger.LoggerConfig
   :members:
   :undoc-members:

Utilities
~~~~~~~~~

.. autofunction:: syinfo.utils.logger.format_exception_traceback

Examples
--------

Complete Example
~~~~~~~~~~~~~~~~

See ``examples/basic/logger_demo.py`` for a comprehensive demonstration of all logger features:

.. code-block:: bash

   python examples/basic/logger_demo.py

This example shows:

- Basic logging usage
- Advanced configuration
- Statistics and management
- Integration with SyInfo functionality
- File logging and syslog
- Error handling with tracebacks

The logger is designed to be both simple for basic usage and powerful for advanced scenarios, making it suitable for everything from quick scripts to production applications.
