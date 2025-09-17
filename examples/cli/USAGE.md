# CLI Usage Examples

```bash
# Device info (JSON)
syinfo -d --json | jq '.cpu_info.cores'

# Network info (disable vendor lookup)
syinfo -n --disable-vendor-search

# System info (device + network summary)
syinfo -s -t 5

# System monitor (10s at 2s interval)
syinfo --system-monitor -t 10 -i 2

# Process monitor, filter python, JSON
syinfo --process-monitor --filter python --json | jq '.data_points[0].processes'

# Logs: regex for errors
syinfo -l --pattern 'error|fail' --json | jq '.[0]'

# Packages: list pip django*
syinfo -p --manager pip --name django --json

# Network scan (sudo)
sudo syinfo -N --json | jq 'to_entries[] | {ip: .key, mac: .value.mac_address, vendor: .value.vendor}'
```
