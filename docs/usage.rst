Usage
=====

Install
-------

.. code-block:: bash

   pip install syinfo
   # optional extras
   pip install 'syinfo[network]'
   pip install 'syinfo[full]'

From source:

.. code-block:: bash

   git clone https://github.com/MR901/syinfo.git
   cd syinfo
   python3 -m venv .venv && source .venv/bin/activate
   pip install -e '.[dev]'

Quickstart
----------

.. code-block:: python

   import syinfo

   info = syinfo.get_system_info()
   print('OS:', info['system_name'])
   print('CPU:', info['cpu_model'])

   syinfo.print_system_tree()

CLI - Flag-Based Commands
-------------------------

.. mermaid:: images/diagrams/cli-workflow.mmd
   :alt: CLI Workflow

The CLI uses a simple flag-based interface:

Device Information:

.. code-block:: bash

   syinfo -d                    # Device/hardware information
   syinfo -dj | jq '.cpu_info' # Device info as JSON

Network Operations:

.. code-block:: bash

   syinfo -n -t 10             # Network scan for 10 seconds
   syinfo -s -t 15             # Combined system info
   syinfo -nj -t 5 | jq '.'    # Network info as JSON

System Monitoring (NEW!):

.. code-block:: bash

   syinfo -m -t 30 -i 5        # Monitor for 30 seconds, 5-second intervals
   syinfo -mpj -t 60 -i 10     # Monitoring with JSON output
   syinfo -mpj -t 120 -i 15 | tail -1 | jq '.summary'

Data Export:

.. code-block:: bash

   syinfo -dpj > device_info.json
   syinfo -mpj -t 300 -i 30 | tail -1 > monitoring_data.json

CLI Flag Reference
------------------

========== =================== =============================================
Flag       Long Flag           Description
========== =================== =============================================
``-d``     ``--device``        Show device/hardware information
``-n``     ``--network``       Show network information and scan devices
``-s``     ``--system``        Show combined device and network information
``-m``     ``--monitor``       **Start system monitoring**
``-t``     ``--time``          Duration in seconds (network scan or monitoring)
``-i``     ``--interval``      **Monitoring interval in seconds (default: 5)**
``-p``     ``--disable-print`` Suppress formatted output
``-j``     ``--return-json``   Output as JSON
``-o``     ``--disable-vendor-search`` Skip vendor lookup (faster)
========== =================== =============================================

Monitoring Examples
-------------------

.. mermaid:: images/diagrams/monitoring-workflow.mmd
   :alt: Monitoring Workflow

System monitoring workflow:

Basic Monitoring:

.. code-block:: bash

   # Monitor for 60 seconds with 10-second intervals
   syinfo -m -t 60 -i 10
   
   # Quick 30-second system check
   syinfo -m -t 30 -i 5

JSON Monitoring Data:

.. code-block:: bash

   # Get monitoring data as JSON
   syinfo -mpj -t 120 -i 10 | tail -1 | jq '.summary'
   
   # Extract CPU average
   syinfo -mpj -t 60 -i 5 | tail -1 | jq -r '.summary.cpu_avg'
   
   # Count data points collected
   syinfo -mpj -t 30 -i 2 | tail -1 | jq '.total_points'

Performance Analysis:

.. code-block:: bash

   # Save monitoring data to file
   syinfo -mpj -t 300 -i 30 | tail -1 > performance_data.json
   
   # Monitor and alert on high CPU
   CPU_AVG=$(syinfo -mpj -t 60 -i 10 | tail -1 | jq -r '.summary.cpu_avg')
   if (( $(echo "$CPU_AVG > 80" | bc -l) )); then
     echo "High CPU usage: $CPU_AVG%"
   fi

Python API
----------

.. code-block:: python

   import syinfo
   
   # Get system information
   info = syinfo.get_complete_info(include_network=False)
   hardware = syinfo.get_hardware_info()
   
   # Create and use monitor
   monitor = syinfo.create_simple_monitor(interval=5)
   monitor.start(duration=60)
   import time; time.sleep(61)
   results = monitor.stop()
   
   print(f"CPU Average: {results['summary']['cpu_avg']:.1f}%")

Screenshots (optional)
----------------------

.. image:: images/example_python_print_device.png
   :alt: Device print example
   :width: 600

.. image:: images/example_print_network.png
   :alt: Network print example
   :width: 600

Advanced/Dev
------------

- Robust GPU strategy: tries GPUtil, then nvidia-smi, then lspci; prints normalized table.
- Exports: JSON/YAML/CSV via ``syinfo.export_system_info``.
- Programmatic: use ``syinfo.get_complete_info(include_network=True)`` for full data.
- Real-time monitoring: ``syinfo.create_simple_monitor(interval=N)`` for system tracking.
- Tests & linting (if dev extras installed)::

 .. code-block:: bash

    pytest -q
    python -m ruff check --fix . && python -m black .
