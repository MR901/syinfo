SyInfo Documentation
====================

Simple, well-designed system information library with real-time monitoring and analysis capabilities (log search, package inventory, health checks).

Technical Overview
------------------

SyInfo collects system and hardware data via:

- psutil for CPU, memory, disks, network IO
- /proc, /sys parsing for Linux details
- optional GPU backends (GPUtil/NVIDIA tools, fallback to lspci)
- YAML/JSON/CSV export and a tree print view
- **Real-time system monitoring** with customizable intervals and durations

The public API (`syinfo.*`) wraps the core collectors and provides stable
functions for application use. The CLI provides powerful flag-based commands
for both one-time information gathering and continuous monitoring.

Supported Platforms
-------------------

- Linux (primary)
- macOS and Windows (best-effort for core info; some features may vary)

Dependencies
------------

- Required: psutil, PyYAML, tabulate, getmac, py-cpuinfo, pydantic, rich, click
- Optional: scapy (network discovery), GPUtil/NVIDIA tools (GPU)

Key Features
------------

- **Device Information**: Hardware details, CPU, memory, storage
- **Network Discovery**: Scan and identify devices on your network
- **System Monitoring**: Real-time performance tracking with JSON export
- **Analysis**: Log queries, package inventory, health checks
- **Advanced Logging**: Production-ready logging with incident tracking and syslog support
- **Flexible CLI**: Flag-based commands perfect for scripting and automation
- **JSON Integration**: Native jq compatibility for data processing

Contents
--------

- :doc:`usage`
- :doc:`api`
- :doc:`logging`
- :doc:`monitoring_with_syinfo`
- :doc:`publishing`

.. toctree::
   :maxdepth: 2
   :caption: Contents

   usage
   api
   logging
   monitoring_with_syinfo
   publishing

Architecture
------------

.. mermaid:: images/diagrams/package-architecture.mmd

The simplified architecture focuses on core functionality without over-engineering.

System Components
-----------------

.. mermaid:: images/diagrams/system-components.mmd

Data Flow
---------

.. mermaid:: images/diagrams/data-flow.mmd

Images
------

.. image:: images/logo.png
   :alt: SyInfo logo
   :width: 200
