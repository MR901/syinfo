SyInfo Documentation
===================

.. image:: images/logo/logo.png
   :alt: SyInfo Logo
   :align: center
   :width: 200px

**System Information & Monitoring Tool**

SyInfo is a comprehensive Python library and command-line tool for system information gathering and advanced system monitoring. It provides both legacy system information capabilities and modern monitoring features with data analysis and visualization.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   user_guide/index
   api/index
   cli/index
   developer/index
   installation
   examples/index
   changelog

Quick Start
----------

**Installation**

.. code-block:: bash

   pip install syinfo

**Basic Usage**

.. code-block:: python

   from syinfo import DeviceInfo, NetworkInfo, SysInfo
   
   # Get device information
   device_info = DeviceInfo.get_all()
   
   # Get network information
   network_info = NetworkInfo.get_all()
   
   # Get combined system information
   system_info = SysInfo.get_all()

**Command Line**

.. code-block:: bash

   # Legacy commands (backward compatible)
   syinfo -d                    # Device info
   syinfo -n                    # Network info
   syinfo -s                    # System info
   
   # New subcommand structure
   syinfo info --device         # Device info
   syinfo monitor --start       # Start monitoring
   syinfo analyze --trends      # Analyze data trends

Key Features
-----------

* **System Information**: Comprehensive device, network, and system information
* **Real-time Monitoring**: CPU, memory, disk, network, and process monitoring
* **Data Analysis**: Trend analysis and anomaly detection
* **Visualization**: Charts and dashboards for system metrics
* **Automated Scheduling**: Cron job integration for continuous monitoring
* **Backward Compatibility**: Full compatibility with existing SyInfo usage
* **Dual Mode**: Both Python library and CLI tool support

Installation Options
-------------------

* **Basic Installation**: Core system information features
* **Full Installation**: Includes monitoring and analysis features
* **Development Installation**: For contributing to the project

.. code-block:: bash

   # Basic installation
   pip install syinfo
   
   # Full installation with monitoring features
   pip install syinfo[monitoring]
   
   # Development installation
   git clone https://github.com/MR901/syinfo.git
   cd syinfo
   pip install -e .

System Requirements
------------------

* **Python**: 3.7 or higher
* **Operating System**: Linux, macOS, Windows
* **Dependencies**: 
  - Core: No additional dependencies
  - Monitoring: psutil, matplotlib, pandas, pyyaml

Getting Help
-----------

* **Documentation**: This documentation
* **GitHub**: https://github.com/MR901/syinfo
* **Email**: mohitrajput901@gmail.com
* **Issues**: https://github.com/MR901/syinfo/issues

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 