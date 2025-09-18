# SyInfo Examples

Organized, runnable examples covering the full functionality:

- basic/: quick-start usage (device, system, network)
- resource_monitor/: system and process monitoring
- analysis/: log analysis, package inventory
- cli/: command-line invocations and JSON outputs

## How to run

Run from project root using module execution so imports resolve correctly:

```bash
python -m examples.basic.device
python -m examples.basic.system
python -m examples.basic.network
python -m examples.basic.export
python -m examples.basic.logger_demo
python -m examples.basic.process_monitor

python -m examples.resource_monitor.system_monitor
python -m examples.resource_monitor.process_monitor

python -m examples.analysis.logs
python -m examples.analysis.packages

``` 
```

## Requirements

Some examples rely on optional extras or system tools (e.g., network scanning,
APT/YUM/NPM presence, access to /var/log). If a feature is unavailable, the
example will degrade gracefully or print a note.
