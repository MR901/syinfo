SyInfo
======

A comprehensive Python package for hardware, network, and software information gathering and monitoring.

SyInfo provides detailed information about your system's hardware components, network configuration, software details, and real-time monitoring capabilities for Linux systems.

Features
--------

* **Hardware Information**: Detailed CPU, memory, disk, GPU, and device manufacturer information
* **Network Information**: Network interfaces, WiFi details, connected devices, and network statistics
* **Software Information**: Operating system details, kernel information, and software configuration
* **Real-time Monitoring**: Monitor system resources, processes, and performance metrics
* **Data Collection**: Automatically collect and store monitoring data
* **Analysis Tools**: Analyze system performance and health
* **CLI Interface**: Command-line tools for easy access
* **API Access**: Programmatic access to all features
* **Configurable**: Customizable monitoring settings and intervals

Installation
-----------

**Complete Installation (Recommended):**
.. code-block:: shell

    # Clone the repository
    git clone <repository-url>
    cd syinfo
    
    # Run the installation script (installs CLI support and dependencies)
    sudo chmod +x install
    sudo ./install
    
    # Install the Python package
    pip install .
    
    # Clean up (optional)
    sudo ./cleanup.sh

**From PyPI (Basic Installation):**
.. code-block:: shell

    pip install syinfo

**Note:** The `./install` script installs additional dependencies and CLI support. For full functionality, use the complete installation method.

Quick Start
----------

**Hardware Information:**
.. code-block:: python

    from syinfo.core import device_info
    
    # Get comprehensive hardware information
    device = device_info.DeviceInfo()
    hardware_info = device.get_all()
    
    print(f"CPU: {hardware_info['cpu_info']['design']['model name']}")
    print(f"Memory: {hardware_info['memory_info']['virtual']['readable']['total']}")
    print(f"GPU: {list(hardware_info['gpu_info'].keys())}")

**Network Information:**
.. code-block:: python

    from syinfo.core import network_info
    
    # Get network details
    network = network_info.NetworkInfo()
    network_data = network.get_all()
    
    print(f"WiFi: {network_data['network_info']['wifi']['wifi_name']}")
    print(f"IP Address: {network_data['network_info']['current_addresses']['public_ip']}")
    print(f"Connected Devices: {len(network_data['network_info']['devices_on_network'])}")

**Software Information:**
.. code-block:: python

    from syinfo.core import sys_info
    
    # Get complete system information (hardware + network + software)
    sys_info_obj = sys_info.SysInfo()
    complete_info = sys_info_obj.get_all()
    
    print(f"OS: {complete_info['dev_info']['operating_system']['full_name']}")
    print(f"Kernel: {complete_info['dev_info']['operating_system']['kernel']}")
    print(f"Architecture: {complete_info['dev_info']['operating_system']['architecture']}")

**Command Line Interface:**
.. code-block:: shell

    # Get hardware information
    python -m syinfo info device
    
    # Get network information
    python -m syinfo info network
    
    # Get complete system information
    python -m syinfo info system
    
    # Start monitoring
    python -m syinfo monitor start --interval 30
    
    # Analyze system health
    python -m syinfo analyze health

**Monitoring Example:**
.. code-block:: python

    from syinfo.monitoring.core import SystemMonitor
    
    # Create system monitor
    monitor = SystemMonitor()
    
    # Start monitoring for 60 seconds
    monitor.start_monitoring(interval=10, duration=60)

Usage Examples
-------------

**Hardware Information:**
.. code-block:: python

    from syinfo.core import device_info
    
    # Get CPU information
    device = device_info.DeviceInfo()
    cpu_info = device.get_cpu_info()
    print(f"CPU Model: {cpu_info['model']}")
    print(f"CPU Cores: {cpu_info['cores']}")
    print(f"CPU Speed: {cpu_info['speed']}")
    
    # Get memory information
    memory_info = device.get_memory_info()
    print(f"Total RAM: {memory_info['total']}")
    print(f"Available RAM: {memory_info['available']}")
    
    # Get disk information
    disk_info = device.get_disk_info()
    print(f"Disk Usage: {disk_info['usage']}%")
    print(f"Disk Space: {disk_info['free']} free of {disk_info['total']}")

**Network Information:**
.. code-block:: python

    from syinfo.core import network_info
    
    # Get network interfaces
    network = network_info.NetworkInfo()
    interfaces = network.get_network_interfaces()
    for interface, info in interfaces.items():
        if info['addresses']:
            print(f"Interface: {interface}")
            print(f"  IP Address: {info['addresses'].get('inet', 'N/A')}")
            print(f"  MAC Address: {info['addresses'].get('ether', 'N/A')}")
    
    # Get network statistics
    net_stats = network.get_network_stats()
    print(f"Bytes Sent: {net_stats['bytes_sent']}")
    print(f"Bytes Received: {net_stats['bytes_recv']}")
    
    # Search for devices on network
    from syinfo.core import search_devices_on_network
    devices = search_devices_on_network(time=10)
    print(f"Found {len(devices)} devices on network")

**Software Information:**
.. code-block:: python

    from syinfo.core import sys_info
    
    # Get complete system information
    sys_info_obj = sys_info.SysInfo()
    info = sys_info_obj.get_all()
    
    # Operating system details
    os_info = info['dev_info']['operating_system']
    print(f"OS: {os_info['full_name']}")
    print(f"Distribution: {os_info['distribution']}")
    print(f"Kernel: {os_info['kernel']}")
    print(f"Architecture: {os_info['architecture']}")
    
    # Device manufacturer information
    device_info = info['dev_info']['device']
    print(f"Manufacturer: {device_info.get('sys_vendor', 'N/A')}")
    print(f"Product: {device_info.get('product_name', 'N/A')}")

**Process Monitoring:**
.. code-block:: python

    from syinfo.monitoring.core import ProcessMonitor
    
    # Monitor top processes
    process_monitor = ProcessMonitor()
    top_processes = process_monitor.get_process_tree(
        sort_by="memory", 
        top_n=10
    )

**Data Analysis:**
.. code-block:: python

    from syinfo.monitoring.data import DataAnalyzer
    
    # Analyze system performance
    analyzer = DataAnalyzer()
    performance = analyzer.analyze_system_performance(data)
    health = analyzer.get_system_health()

Configuration
-------------

Create a monitoring configuration file:

.. code-block:: yaml

    monitoring:
      system:
        enabled: true
        interval: 60
        metrics:
          - cpu_usage
          - memory_usage
          - disk_usage
          - network_io
      storage:
        data_directory: "/var/log/syinfo/monitoring"
        retention_days: 7
        format: "csv"

CLI Commands
-----------

* ``python -m syinfo info system`` - Get complete system information (hardware + network + software)
* ``python -m syinfo info device`` - Get hardware information  
* ``python -m syinfo info network`` - Get network information
* ``python -m syinfo monitor start`` - Start system monitoring
* ``python -m syinfo monitor stop`` - Stop monitoring
* ``python -m syinfo analyze performance`` - Analyze system performance
* ``python -m syinfo analyze health`` - Check system health
* ``python -m syinfo --help`` - Show help

Examples
--------

See the `examples/` directory for comprehensive usage examples:

* `basic_system_info.py` - Basic system information
* `monitoring_example.py` - Monitoring features
* `cli_examples.py` - CLI usage
* `api_example.py` - API access
* `configuration_example.py` - Configuration management

Documentation
------------

* `docs/` - Full documentation
* `docs/user_guide/` - User guide
* `docs/api/` - API reference
* `docs/cli/` - CLI reference

Requirements
-----------

* Python 3.7+
* Linux system
* psutil
* pyyaml
* Cython
* getmac
* GPUtil
* scapy
* tabulate
* requests




sudo dpkg --list | grep syinfo
sudo dpkg -r syinfo


