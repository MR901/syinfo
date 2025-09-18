Builder Pattern API
===================

Overview
--------

SyInfo provides a fluent, Keras-style builder API for configuring and collecting
system information without changing the underlying core modules.

Key classes:

- ``InfoBuilder``: Fluent configuration entrypoint
- ``SyInfoSystem``: Built orchestrator with ``collect`` and ``collect_async``
- Config dataclasses in ``syinfo.builder.config``

Quick Start
-----------

.. code-block:: python

   from syinfo import InfoBuilder
   import asyncio, time

   # Basic system
   sys1 = (InfoBuilder()
           .include_hardware()
           .enable_caching(ttl=300)
           .build())
   print(sys1.summary())
   data = sys1.collect()

   # Network (no active scan)
   async def run():
       sys2 = (InfoBuilder()
               .include_hardware()
               .include_network(timeout=0, include_vendor_info=False)
               .build())
       net = await sys2.collect_async(scope="network")
       print(list(net.get("network_info", {}).keys())[:5])

   asyncio.run(run())

   # Monitoring
   sys3 = (InfoBuilder()
           .include_monitoring(interval=2)
           .build())
   mon = sys3.create_monitor()
   mon.start(duration=6)
   time.sleep(7)
   res = mon.stop()
   print(res.get("total_points"))

Logs and Packages
-----------------

.. code-block:: python

   # Logs (limit small)
   sys_logs = (InfoBuilder().include_logs(limit=3).build())
   logs = sys_logs.analyze_logs()
   print(len(logs.get("log_entries", [])))

   # Packages (filter optional)
   sys_pkgs = (InfoBuilder().include_packages(name_filter="python").build())
   pkgs = sys_pkgs.analyze_packages()
   print(len(pkgs.get("packages", [])))

Export
------

.. code-block:: python

   sys_exp = (InfoBuilder().include_hardware().export_as("yaml").build())
   y = sys_exp.export(sys_exp.collect(scope="hardware"))
   print(y[:200])

Presets
-------

- ``InfoBuilder.basic_system()``
- ``InfoBuilder.full_system()``
- ``InfoBuilder.monitoring_system(interval=5)``

Notes
-----

- ``include_network(timeout=0)`` disables active scanning; use sudo for scans.
- Package manager and features vary by platform; results may be empty.

