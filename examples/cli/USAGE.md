# CLI Usage Examples

```bash
# Device info
syinfo -d

# Network info (no device vendor lookup)
syinfo -n -o

# System info (device + network)
syinfo -s -t 5

# Monitor for 10s at 2s interval, JSON output
syinfo -m -t 10 -i 2 -j

# Logs: errors about sshd in last 24h, JSON
syinfo --logs --text "failed" --process sshd --level ERROR --hours 24 -j

# Packages: list pip django*
syinfo --packages --manager pip --name django -j

# Health report
syinfo --health

# Cross search
syinfo --search nginx -j
```
