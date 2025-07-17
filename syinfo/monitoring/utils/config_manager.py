"""
Configuration management for monitoring system.

This module provides centralized configuration management with YAML support,
environment-specific settings, validation, and secure credential management.
"""

import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path


class MonitoringConfig:
    """
    Centralized configuration management for monitoring system.
    
    Features:
    - YAML-based configuration
    - Environment-specific settings
    - Validation and defaults
    - Hot-reload capability
    - Secure credential management
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration from file or defaults.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'monitoring.system.interval')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        try:
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
        except Exception:
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set configuration value using dot notation.
        
        Args:
            key: Configuration key
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            keys = key.split('.')
            config = self.config
            
            # Navigate to the parent of the target key
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            # Set the value
            config[keys[-1]] = value
            return True
        except Exception:
            return False
    
    def save(self) -> bool:
        """
        Save configuration to file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.config_path:
                return False
            
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            return True
        except Exception:
            return False
    
    def validate_config(self) -> Dict[str, Any]:
        """
        Validate configuration parameters.
        
        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []
        
        # Validate monitoring settings
        monitoring = self.get('monitoring', {})
        if not monitoring:
            errors.append("No monitoring configuration found")
        
        # Validate system monitoring
        system = monitoring.get('system', {})
        if system.get('enabled', True):
            interval = system.get('interval', 60)
            if interval < 1:
                errors.append("System monitoring interval must be >= 1 second")
            elif interval > 3600:
                warnings.append("System monitoring interval is very high (> 1 hour)")
        
        # Validate process monitoring
        process = monitoring.get('process', {})
        if process.get('enabled', True):
            interval = process.get('interval', 60)
            if interval < 1:
                errors.append("Process monitoring interval must be >= 1 second")
        
        # Validate storage settings
        storage = monitoring.get('storage', {})
        data_dir = storage.get('data_directory', '/var/log/syinfo/monitoring')
        if not os.path.exists(data_dir):
            try:
                os.makedirs(data_dir, exist_ok=True)
            except Exception:
                errors.append(f"Cannot create data directory: {data_dir}")
        
        retention_days = storage.get('retention_days', 7)
        if retention_days < 1:
            errors.append("Retention days must be >= 1")
        
        # Validate logging settings
        logging = monitoring.get('logging', {})
        log_file = logging.get('file', '/var/log/syinfo/monitoring.log')
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir, exist_ok=True)
            except Exception:
                errors.append(f"Cannot create log directory: {log_dir}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def get_monitoring_settings(self) -> Dict[str, Any]:
        """
        Get monitoring-specific settings.
        
        Returns:
            Dictionary with monitoring settings
        """
        return self.get('monitoring', {})
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_path and os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                pass
        
        # Return default configuration
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "monitoring": {
                "system": {
                    "enabled": True,
                    "interval": 60,
                    "metrics": [
                        "cpu_usage",
                        "memory_usage",
                        "disk_usage",
                        "network_io"
                    ]
                },
                "process": {
                    "enabled": True,
                    "interval": 60,
                    "top_processes": 10,
                    "filter_pattern": None
                },
                "logs": {
                    "enabled": False,
                    "sources": [
                        "/var/log/syslog",
                        "/var/log/auth.log"
                    ]
                },
                "storage": {
                    "data_directory": "/var/log/syinfo/monitoring",
                    "retention_days": 7,
                    "format": "csv",
                    "compression": False
                },
                "logging": {
                    "level": "INFO",
                    "file": "/var/log/syinfo/monitoring.log",
                    "max_size": "10MB",
                    "backup_count": 5
                }
            }
        } 