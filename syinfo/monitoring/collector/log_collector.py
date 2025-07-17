"""
Log collection and parsing module.

This module provides system log collection, parsing, and analysis
with security-focused log processing.
"""

import os
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading

from ..utils.logger import MonitoringLogger
from ..utils.config_manager import MonitoringConfig


class LogCollector:
    """
    System log collector with parsing and analysis capabilities.
    
    Features:
    - System log collection and parsing
    - Error pattern detection and reporting
    - Log rotation handling and real-time analysis
    - Security-focused log processing
    - Configurable log sources and filters
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize log collector.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = MonitoringConfig(config_path)
        self.logger = MonitoringLogger()
        self.collecting = False
        self.collector_thread = None
        self.stop_event = threading.Event()
        self.log_positions = {}  # Track file positions for each log file
        
    def start_collection(self, log_sources: Optional[List[str]] = None, 
                        interval: int = 60) -> bool:
        """
        Start continuous log collection.
        
        Args:
            log_sources: List of log file paths to monitor
            interval: Collection interval in seconds
            
        Returns:
            True if collection started successfully, False otherwise
        """
        try:
            if self.collecting:
                self.logger.log_monitoring_event("WARNING", "Log collection already running")
                return False
            
            if not log_sources:
                log_sources = self.config.get('monitoring.logs.sources', [
                    '/var/log/syslog',
                    '/var/log/auth.log'
                ])
            
            self.logger.log_monitoring_event("INFO", f"Starting log collection from {len(log_sources)} sources")
            self.collecting = True
            self.stop_event.clear()
            
            # Start collection in separate thread
            self.collector_thread = threading.Thread(
                target=self._collection_loop,
                args=(log_sources, interval),
                daemon=True
            )
            self.collector_thread.start()
            
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to start log collection")
            return False
    
    def stop_collection(self) -> bool:
        """
        Stop log collection.
        
        Returns:
            True if collection stopped successfully, False otherwise
        """
        try:
            if not self.collecting:
                return True
                
            self.logger.log_monitoring_event("INFO", "Stopping log collection")
            self.collecting = False
            self.stop_event.set()
            
            if self.collector_thread and self.collector_thread.is_alive():
                self.collector_thread.join(timeout=10)
                
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to stop log collection")
            return False
    
    def collect_log_snapshot(self, log_file: str, lines: int = 100) -> Dict:
        """
        Collect a snapshot of log data.
        
        Args:
            log_file: Path to log file
            lines: Number of recent lines to collect
            
        Returns:
            Dictionary with log analysis results
        """
        try:
            if not os.path.exists(log_file):
                return {"error": f"Log file {log_file} not found"}
            
            with open(log_file, 'r') as f:
                recent_lines = f.readlines()[-lines:]
            
            # Parse log entries
            log_entries = []
            error_count = 0
            warning_count = 0
            critical_count = 0
            
            for line in recent_lines:
                entry = self._parse_log_line(line.strip())
                if entry:
                    log_entries.append(entry)
                    
                    # Count by severity
                    severity = entry.get('severity', '').lower()
                    if 'error' in severity:
                        error_count += 1
                    elif 'warning' in severity:
                        warning_count += 1
                    elif 'critical' in severity:
                        critical_count += 1
            
            return {
                "log_file": log_file,
                "total_lines": len(recent_lines),
                "parsed_entries": len(log_entries),
                "error_count": error_count,
                "warning_count": warning_count,
                "critical_count": critical_count,
                "error_rate": error_count / len(recent_lines) if recent_lines else 0,
                "entries": log_entries[-10:]  # Last 10 entries for preview
            }
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to collect log snapshot from {log_file}")
            return {"error": str(e)}
    
    def analyze_log_patterns(self, log_file: str, time_range: str = "1h") -> Dict:
        """
        Analyze log patterns over a time range.
        
        Args:
            log_file: Path to log file
            time_range: Time range to analyze (e.g., "1h", "24h", "7d")
            
        Returns:
            Dictionary with pattern analysis results
        """
        try:
            if not os.path.exists(log_file):
                return {"error": f"Log file {log_file} not found"}
            
            # Calculate time cutoff
            cutoff_time = self._get_cutoff_time(time_range)
            
            # Read and filter log entries
            matching_entries = []
            with open(log_file, 'r') as f:
                for line in f:
                    entry = self._parse_log_line(line.strip())
                    if entry and entry.get('timestamp', 0) >= cutoff_time:
                        matching_entries.append(entry)
            
            # Analyze patterns
            patterns = self._analyze_patterns(matching_entries)
            
            return {
                "log_file": log_file,
                "time_range": time_range,
                "total_entries": len(matching_entries),
                "patterns": patterns,
                "top_errors": self._get_top_errors(matching_entries),
                "top_sources": self._get_top_sources(matching_entries)
            }
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to analyze log patterns in {log_file}")
            return {"error": str(e)}
    
    def _collection_loop(self, log_sources: List[str], interval: int):
        """Main collection loop."""
        while self.collecting and not self.stop_event.is_set():
            try:
                for log_file in log_sources:
                    if os.path.exists(log_file):
                        # Collect new log entries
                        new_entries = self._collect_new_entries(log_file)
                        
                        if new_entries:
                            # Store new entries (this would integrate with storage module)
                            # self.storage.store_log_entries(log_file, new_entries)
                            
                            # Analyze for immediate alerts
                            alerts = self._check_for_alerts(new_entries)
                            if alerts:
                                self.logger.log_monitoring_event("ALERT", f"Log alerts detected: {alerts}")
                
                # Wait for next interval
                self.stop_event.wait(interval)
                
            except Exception as e:
                self.logger.log_error_with_context(e, "Error in log collection loop")
                time.sleep(5)  # Brief pause before retry
        
        self.collecting = False
    
    def _parse_log_line(self, line: str) -> Optional[Dict]:
        """Parse a single log line."""
        try:
            if not line:
                return None
            
            # Common log patterns
            patterns = [
                # syslog format: Jan 1 12:00:00 hostname program[pid]: message
                r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+([^:]+):\s*(.*)$',
                # ISO format: 2024-01-01T12:00:00.000Z
                r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)\s+(.*)$',
                # Simple timestamp: 2024-01-01 12:00:00
                r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.*)$'
            ]
            
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    timestamp_str = match.group(1)
                    message = match.group(2) if len(match.groups()) == 2 else match.group(4)
                    
                    # Parse timestamp
                    timestamp = self._parse_timestamp(timestamp_str)
                    
                    # Extract severity
                    severity = self._extract_severity(message)
                    
                    # Extract source/program
                    source = match.group(3) if len(match.groups()) >= 3 else "unknown"
                    
                    return {
                        "timestamp": timestamp,
                        "datetime": datetime.fromtimestamp(timestamp).isoformat() if timestamp else None,
                        "source": source,
                        "severity": severity,
                        "message": message,
                        "raw_line": line
                    }
            
            # Fallback: return basic info
            return {
                "timestamp": time.time(),
                "datetime": datetime.now().isoformat(),
                "source": "unknown",
                "severity": "info",
                "message": line,
                "raw_line": line
            }
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to parse log line: {line[:100]}")
            return None
    
    def _parse_timestamp(self, timestamp_str: str) -> float:
        """Parse timestamp string to Unix timestamp."""
        try:
            # Try different timestamp formats
            formats = [
                "%b %d %H:%M:%S",  # Jan 1 12:00:00
                "%Y-%m-%dT%H:%M:%S",  # 2024-01-01T12:00:00
                "%Y-%m-%dT%H:%M:%S.%f",  # 2024-01-01T12:00:00.000
                "%Y-%m-%d %H:%M:%S",  # 2024-01-01 12:00:00
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(timestamp_str, fmt)
                    # Assume current year if not specified
                    if dt.year == 1900:
                        dt = dt.replace(year=datetime.now().year)
                    return dt.timestamp()
                except ValueError:
                    continue
            
            return time.time()  # Fallback to current time
            
        except Exception:
            return time.time()
    
    def _extract_severity(self, message: str) -> str:
        """Extract severity level from log message."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['critical', 'fatal', 'emergency']):
            return 'critical'
        elif any(word in message_lower for word in ['error', 'err']):
            return 'error'
        elif any(word in message_lower for word in ['warning', 'warn']):
            return 'warning'
        elif any(word in message_lower for word in ['info', 'information']):
            return 'info'
        elif any(word in message_lower for word in ['debug']):
            return 'debug'
        else:
            return 'info'
    
    def _get_cutoff_time(self, time_range: str) -> float:
        """Get cutoff time based on time range string."""
        now = time.time()
        
        if time_range.endswith('h'):
            hours = int(time_range[:-1])
            return now - (hours * 3600)
        elif time_range.endswith('d'):
            days = int(time_range[:-1])
            return now - (days * 86400)
        elif time_range.endswith('m'):
            minutes = int(time_range[:-1])
            return now - (minutes * 60)
        else:
            return now - 3600  # Default to 1 hour
    
    def _analyze_patterns(self, entries: List[Dict]) -> Dict:
        """Analyze patterns in log entries."""
        patterns = {
            "severity_distribution": {},
            "source_distribution": {},
            "hourly_distribution": {},
            "common_messages": {}
        }
        
        for entry in entries:
            # Severity distribution
            severity = entry.get('severity', 'unknown')
            patterns["severity_distribution"][severity] = patterns["severity_distribution"].get(severity, 0) + 1
            
            # Source distribution
            source = entry.get('source', 'unknown')
            patterns["source_distribution"][source] = patterns["source_distribution"].get(source, 0) + 1
            
            # Hourly distribution
            if entry.get('timestamp'):
                hour = datetime.fromtimestamp(entry['timestamp']).hour
                patterns["hourly_distribution"][hour] = patterns["hourly_distribution"].get(hour, 0) + 1
            
            # Common messages (first 50 chars)
            message = entry.get('message', '')[:50]
            patterns["common_messages"][message] = patterns["common_messages"].get(message, 0) + 1
        
        return patterns
    
    def _get_top_errors(self, entries: List[Dict], top_n: int = 10) -> List[Dict]:
        """Get top error messages."""
        error_messages = {}
        
        for entry in entries:
            if entry.get('severity') in ['error', 'critical']:
                message = entry.get('message', '')
                error_messages[message] = error_messages.get(message, 0) + 1
        
        # Sort by count and return top N
        sorted_errors = sorted(error_messages.items(), key=lambda x: x[1], reverse=True)
        return [{"message": msg, "count": count} for msg, count in sorted_errors[:top_n]]
    
    def _get_top_sources(self, entries: List[Dict], top_n: int = 10) -> List[Dict]:
        """Get top log sources."""
        source_counts = {}
        
        for entry in entries:
            source = entry.get('source', 'unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Sort by count and return top N
        sorted_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"source": src, "count": count} for src, count in sorted_sources[:top_n]]
    
    def _collect_new_entries(self, log_file: str) -> List[Dict]:
        """Collect new log entries since last collection."""
        try:
            if not os.path.exists(log_file):
                return []
            
            # Get current file size
            current_size = os.path.getsize(log_file)
            last_position = self.log_positions.get(log_file, 0)
            
            if current_size < last_position:
                # File was rotated, start from beginning
                last_position = 0
            
            new_entries = []
            with open(log_file, 'r') as f:
                f.seek(last_position)
                for line in f:
                    entry = self._parse_log_line(line.strip())
                    if entry:
                        new_entries.append(entry)
            
            # Update position
            self.log_positions[log_file] = current_size
            
            return new_entries
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to collect new entries from {log_file}")
            return []
    
    def _check_for_alerts(self, entries: List[Dict]) -> List[str]:
        """Check for immediate alerts in log entries."""
        alerts = []
        
        for entry in entries:
            if entry.get('severity') == 'critical':
                alerts.append(f"Critical log entry: {entry.get('message', '')[:100]}")
            elif entry.get('severity') == 'error' and 'authentication' in entry.get('message', '').lower():
                alerts.append(f"Authentication error: {entry.get('message', '')[:100]}")
        
        return alerts
    
    def get_collection_status(self) -> Dict:
        """
        Get current collection status.
        
        Returns:
            Dictionary with collection status information
        """
        return {
            "collecting": self.collecting,
            "thread_alive": self.collector_thread.is_alive() if self.collector_thread else False,
            "stop_requested": self.stop_event.is_set(),
            "monitored_files": list(self.log_positions.keys())
        } 