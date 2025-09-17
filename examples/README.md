# SyInfo Examples

Organized, runnable examples covering the full functionality:

- core/: quick-start usage (device, system, network)
- resource_monitor/: system and process monitoring
- analysis/: log analysis, package inventory
- general/: export, logger demos
- cli/: command-line invocations and JSON outputs

## How to run

Run from project root using module execution so imports resolve correctly:

```bash
python -m examples.core.device
python -m examples.core.system
python -m examples.core.network

python -m examples.resource_monitor.system_monitor
python -m examples.resource_monitor.process_monitor

python -m examples.analysis.logs_examples
python -m examples.analysis.packages_examples

python -m examples.general.export
python -m examples.basic.logger_demo
```

## Requirements

Some examples rely on optional extras or system tools (e.g., network scanning,
APT/YUM/NPM presence, access to /var/log). If a feature is unavailable, the
example will degrade gracefully or print a note.
