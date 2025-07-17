"""
Structured logging for monitoring system.

This module provides structured logging with severity levels, rotation,
and performance impact minimization.
"""

import os
import logging
import logging.handlers
from datetime import datetime
from typing import Optional, Dict, Any


class MonitoringLogger:
    """
    Structured logging with severity levels and rotation.
    
    Features:
    - Multiple severity levels
    - Structured log format
    - Automatic log rotation
    - Performance impact minimization
    - Audit trail maintenance
    """
    
    def __init__(self, log_file: Optional[str] = None, level: str = "INFO"):
        """
        Initialize logger with configuration.
        
        Args:
            log_file: Path to log file
            level: Logging level
        """
        self.logger = logging.getLogger('syinfo_monitoring')
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers(log_file)
    
    def log_monitoring_event(self, event_type: str, details: str, severity: str = "INFO", 
                           context: Optional[Dict[str, Any]] = None):
        """
        Log monitoring events with structured format.
        
        Args:
            event_type: Type of event (e.g., "START", "STOP", "ERROR")
            details: Event details
            severity: Log severity level
            context: Additional context data
        """
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "details": details,
                "severity": severity
            }
            
            if context:
                log_entry["context"] = context
            
            message = f"[{severity}] {event_type}: {details}"
            if context:
                message += f" | Context: {context}"
            
            log_level = getattr(logging, severity.upper(), logging.INFO)
            self.logger.log(log_level, message)
            
        except Exception as e:
            # Fallback to basic logging if structured logging fails
            self.logger.error(f"Logging error: {e} | Original message: {details}")
    
    def log_error_with_context(self, error: Exception, context: Optional[str] = None):
        """
        Log errors with full context information.
        
        Args:
            error: Exception object
            context: Additional context string
        """
        try:
            error_context = {
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context
            }
            
            self.log_monitoring_event(
                "ERROR",
                f"Exception occurred: {error}",
                "ERROR",
                error_context
            )
            
        except Exception as e:
            # Fallback logging
            self.logger.error(f"Error logging failed: {e} | Original error: {error}")
    
    def log_performance_metric(self, metric_name: str, value: float, unit: str = ""):
        """
        Log performance metrics.
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            unit: Unit of measurement
        """
        try:
            context = {
                "metric_name": metric_name,
                "value": value,
                "unit": unit
            }
            
            self.log_monitoring_event(
                "METRIC",
                f"{metric_name}: {value}{unit}",
                "INFO",
                context
            )
            
        except Exception as e:
            self.logger.error(f"Failed to log performance metric: {e}")
    
    def log_configuration_change(self, key: str, old_value: Any, new_value: Any):
        """
        Log configuration changes.
        
        Args:
            key: Configuration key
            old_value: Previous value
            new_value: New value
        """
        try:
            context = {
                "config_key": key,
                "old_value": str(old_value),
                "new_value": str(new_value)
            }
            
            self.log_monitoring_event(
                "CONFIG_CHANGE",
                f"Configuration updated: {key}",
                "INFO",
                context
            )
            
        except Exception as e:
            self.logger.error(f"Failed to log configuration change: {e}")
    
    def _setup_handlers(self, log_file: Optional[str]):
        """Setup logging handlers."""
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (if log_file specified)
        if log_file:
            try:
                # Ensure log directory exists
                log_dir = os.path.dirname(log_file)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)
                
                # Rotating file handler
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file,
                    maxBytes=10*1024*1024,  # 10MB
                    backupCount=5
                )
                file_handler.setLevel(logging.DEBUG)
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)
                
            except Exception as e:
                # Fallback to basic file handler
                try:
                    file_handler = logging.FileHandler(log_file)
                    file_handler.setLevel(logging.DEBUG)
                    file_formatter = logging.Formatter(
                        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
                    file_handler.setFormatter(file_formatter)
                    self.logger.addHandler(file_handler)
                except Exception:
                    self.logger.warning(f"Could not setup file logging to {log_file}")
    
    def get_log_level(self) -> str:
        """Get current log level."""
        return logging.getLevelName(self.logger.level)
    
    def set_log_level(self, level: str):
        """Set log level."""
        try:
            self.logger.setLevel(getattr(logging, level.upper()))
            self.log_monitoring_event("LOG_LEVEL_CHANGE", f"Log level set to {level}", "INFO")
        except Exception as e:
            self.logger.error(f"Failed to set log level: {e}")
    
    def cleanup_old_logs(self, log_file: str, max_age_days: int = 30):
        """
        Clean up old log files.
        
        Args:
            log_file: Path to log file
            max_age_days: Maximum age in days
        """
        try:
            if not os.path.exists(log_file):
                return
            
            log_dir = os.path.dirname(log_file)
            log_base = os.path.basename(log_file)
            
            current_time = datetime.now()
            removed_count = 0
            
            for filename in os.listdir(log_dir):
                if filename.startswith(log_base):
                    file_path = os.path.join(log_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if (current_time - file_time).days > max_age_days:
                        try:
                            os.remove(file_path)
                            removed_count += 1
                        except Exception:
                            pass
            
            if removed_count > 0:
                self.log_monitoring_event(
                    "LOG_CLEANUP",
                    f"Removed {removed_count} old log files",
                    "INFO"
                )
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup old logs: {e}") 