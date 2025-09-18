Monitoring with SyInfo
======================

Overview
--------

This guide shows how to implement robust system and process monitoring using SyInfo,
inspired by the external reference scripts (system/process stats, CSV export,
and offline analysis), while adding resilience, persistence, and visualization.

What you can build with SyInfo
------------------------------

- Periodic system metrics collection (CPU, memory, disk, net)
- Optional process-level top-N snapshot with grep filtering
- Crash-safe persistence (JSONL) with rotation
- Summary files for quick insight
- Visualization (Matplotlib/Plotly)
- CLI integration and environment configuration

Quick start: System monitoring
------------------------------

.. code-block:: python

   from syinfo import SystemMonitor
   from syinfo.resource_monitor.visualization import create_monitoring_plot

   # Create system monitor with 2-second intervals
   mon = SystemMonitor(interval=2)
   mon.start(duration=60)  # collect for 60 seconds
   import time; time.sleep(61)
   results = mon.stop()  # returns monitoring data

   # Visualize the collected data
   create_monitoring_plot(results['data_points'], show=True)

Process snapshots (top-N, grep)
--------------------------------

SyInfo currently focuses on system metrics. To mimic the reference process stats,
you can create a small helper using psutil:

.. code-block:: python

   import time
   import psutil

   def top_processes(sort_by="memory", top_n=10, grep=None):
       # Prime CPU counters
       for p in psutil.process_iter():
           try: p.cpu_percent(interval=None)
           except (psutil.NoSuchProcess, psutil.AccessDenied):
               continue
       time.sleep(1.0)

       rows = []
       cpu_count = psutil.cpu_count() or 1
       for p in psutil.process_iter(attrs=["pid","ppid","username","name","create_time","cmdline","memory_percent","memory_info","io_counters","num_threads","nice"]):
           try:
               info = p.info
               cmd = " ".join(info.get("cmdline") or [])
               if grep and (grep.lower() not in (info.get("name") or "").lower()) and (grep.lower() not in cmd.lower()):
                   continue
               cpu_pct = p.cpu_percent(interval=None) / cpu_count
               mem = info.get("memory_info")
               io = info.get("io_counters")
               rows.append({
                   "pid": info.get("pid"),
                   "ppid": info.get("ppid"),
                   "username": info.get("username"),
                   "name": info.get("name"),
                   "command": cmd,
                   "cpu_percent": cpu_pct,
                   "memory_percent": info.get("memory_percent"),
                   "memory_rss_bytes": getattr(mem, "rss", None),
                   "memory_vms_bytes": getattr(mem, "vms", None),
                   "io_read_bytes": getattr(io, "read_bytes", None),
                   "io_write_bytes": getattr(io, "write_bytes", None),
                   "num_threads": info.get("num_threads"),
                   "nice": info.get("nice"),
                   "create_ts": info.get("create_time"),
               })
           except (psutil.NoSuchProcess, psutil.AccessDenied):
               continue

       key = "memory_rss_bytes" if sort_by == "memory" else "cpu_percent"
       rows.sort(key=lambda r: (r.get(key) or 0), reverse=True)
       return rows[:top_n] if top_n else rows

CSV export
----------

The reference uses CSV (append/overwrite with header check). With SyInfo you may
prefer JSONL for crash safety, but CSV is simple to add:

.. code-block:: python

   import csv, os

   def append_csv(dicts, path):
       if not dicts: return
       fieldnames = list(dicts[0].keys())
       exists = os.path.isfile(path)
       mode = "a" if exists else "w"
       with open(path, mode, newline="") as f:
           w = csv.DictWriter(f, fieldnames=fieldnames)
           if not exists:
               w.writeheader()
           w.writerows(dicts)

   # Example
   append_csv(top_processes(grep="python"), "process_top.csv")

Visualization
-------------

- Matplotlib: ``syinfo.resource_monitor.visualization.create_monitoring_plot(path)``

Tips & additions
----------------

- For long-running monitoring, set rotation thresholds and a directory as output_path.
- For lower RAM use, set ``keep_in_memory=False``; you can analyze results from JSONL later.
- To include system info context in summaries, call ``syinfo.get_system_info()`` and store
  alongside or inside the summary JSON.
- For alerts, add simple thresholds in the callback you pass to ``SystemMonitor.start``.


