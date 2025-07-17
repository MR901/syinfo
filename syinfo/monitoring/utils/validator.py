"""
Input validation and sanitization for monitoring system.

This module provides comprehensive input validation including:
- Type checking and conversion
- Path validation and sanitization
- Command injection prevention
- Resource limit validation
- Security constraint enforcement
"""

import os
import re
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


class InputValidator:
    """
    Comprehensive input validation and sanitization.
    
    Features:
    - Type checking and conversion
    - Path validation and sanitization
    - Command injection prevention
    - Resource limit validation
    - Security constraint enforcement
    """
    
    # Security patterns
    DANGEROUS_PATTERNS = [
        r'[;&|`$]',  # Command separators
        r'\.\./',    # Path traversal
        r'<script',  # XSS
        r'javascript:',  # JavaScript injection
    ]
    
    @staticmethod
    def validate_file_path(path: str) -> Dict[str, Any]:
        """
        Validate and sanitize file paths.
        
        Args:
            path: File path to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            if not path or not isinstance(path, str):
                return {"valid": False, "error": "Path must be a non-empty string"}
            
            # Check for dangerous patterns
            for pattern in InputValidator.DANGEROUS_PATTERNS:
                if re.search(pattern, path, re.IGNORECASE):
                    return {"valid": False, "error": f"Path contains dangerous pattern: {pattern}"}
            
            # Normalize path
            normalized_path = os.path.normpath(path)
            
            # Check if path is absolute and within allowed directories
            if os.path.isabs(normalized_path):
                # For security, restrict to specific directories
                allowed_dirs = ['/var/log', '/tmp', '/home']
                if not any(normalized_path.startswith(allowed_dir) for allowed_dir in allowed_dirs):
                    return {"valid": False, "error": "Path outside allowed directories"}
            
            return {
                "valid": True,
                "normalized_path": normalized_path,
                "exists": os.path.exists(normalized_path),
                "is_file": os.path.isfile(normalized_path) if os.path.exists(normalized_path) else False,
                "is_dir": os.path.isdir(normalized_path) if os.path.exists(normalized_path) else False
            }
            
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    @staticmethod
    def validate_monitoring_interval(interval: Any) -> Dict[str, Any]:
        """
        Validate monitoring interval parameters.
        
        Args:
            interval: Interval value to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Convert to integer
            if isinstance(interval, str):
                interval = int(interval)
            elif not isinstance(interval, (int, float)):
                return {"valid": False, "error": "Interval must be a number"}
            
            # Validate range
            if interval < 1:
                return {"valid": False, "error": "Interval must be >= 1 second"}
            elif interval > 86400:  # 24 hours
                return {"valid": False, "error": "Interval must be <= 86400 seconds (24 hours)"}
            
            return {
                "valid": True,
                "interval": int(interval),
                "human_readable": InputValidator._format_duration(interval)
            }
            
        except ValueError:
            return {"valid": False, "error": "Interval must be a valid number"}
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    @staticmethod
    def sanitize_process_name(name: str) -> Dict[str, Any]:
        """
        Sanitize process names for filtering.
        
        Args:
            name: Process name to sanitize
            
        Returns:
            Dictionary with sanitization results
        """
        try:
            if not name or not isinstance(name, str):
                return {"valid": False, "error": "Process name must be a non-empty string"}
            
            # Remove dangerous characters
            sanitized = re.sub(r'[;&|`$<>"\']', '', name)
            
            # Limit length
            if len(sanitized) > 100:
                sanitized = sanitized[:100]
            
            # Check if sanitized name is different
            if sanitized != name:
                return {
                    "valid": True,
                    "sanitized": sanitized,
                    "original": name,
                    "warning": "Process name was sanitized"
                }
            
            return {
                "valid": True,
                "sanitized": sanitized
            }
            
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    @staticmethod
    def validate_config_data(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate configuration data structure.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            errors = []
            warnings = []
            
            if not isinstance(config, dict):
                return {"valid": False, "error": "Configuration must be a dictionary"}
            
            # Validate monitoring section
            monitoring = config.get('monitoring', {})
            if not monitoring:
                errors.append("No monitoring configuration found")
            else:
                # Validate system monitoring
                system = monitoring.get('system', {})
                if system.get('enabled', True):
                    interval_result = InputValidator.validate_monitoring_interval(
                        system.get('interval', 60)
                    )
                    if not interval_result['valid']:
                        errors.append(f"System monitoring: {interval_result['error']}")
                
                # Validate process monitoring
                process = monitoring.get('process', {})
                if process.get('enabled', True):
                    interval_result = InputValidator.validate_monitoring_interval(
                        process.get('interval', 60)
                    )
                    if not interval_result['valid']:
                        errors.append(f"Process monitoring: {interval_result['error']}")
                
                # Validate storage settings
                storage = monitoring.get('storage', {})
                data_dir = storage.get('data_directory', '/var/log/syinfo/monitoring')
                path_result = InputValidator.validate_file_path(data_dir)
                if not path_result['valid']:
                    errors.append(f"Storage directory: {path_result['error']}")
                
                retention_days = storage.get('retention_days', 7)
                if not isinstance(retention_days, int) or retention_days < 1:
                    errors.append("Retention days must be a positive integer")
                
                # Validate logging settings
                logging = monitoring.get('logging', {})
                log_file = logging.get('file', '/var/log/syinfo/monitoring.log')
                path_result = InputValidator.validate_file_path(log_file)
                if not path_result['valid']:
                    errors.append(f"Log file: {path_result['error']}")
                
                log_level = logging.get('level', 'INFO')
                valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
                if log_level.upper() not in valid_levels:
                    errors.append(f"Invalid log level: {log_level}")
            
            return {
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings
            }
            
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    @staticmethod
    def validate_resource_limits(cpu_limit: Optional[float] = None, 
                                memory_limit: Optional[float] = None,
                                disk_limit: Optional[float] = None) -> Dict[str, Any]:
        """
        Validate resource limit parameters.
        
        Args:
            cpu_limit: CPU usage limit (0-100)
            memory_limit: Memory usage limit (0-100)
            disk_limit: Disk usage limit (0-100)
            
        Returns:
            Dictionary with validation results
        """
        try:
            errors = []
            
            # Validate CPU limit
            if cpu_limit is not None:
                if not isinstance(cpu_limit, (int, float)) or cpu_limit < 0 or cpu_limit > 100:
                    errors.append("CPU limit must be between 0 and 100")
            
            # Validate memory limit
            if memory_limit is not None:
                if not isinstance(memory_limit, (int, float)) or memory_limit < 0 or memory_limit > 100:
                    errors.append("Memory limit must be between 0 and 100")
            
            # Validate disk limit
            if disk_limit is not None:
                if not isinstance(disk_limit, (int, float)) or disk_limit < 0 or disk_limit > 100:
                    errors.append("Disk limit must be between 0 and 100")
            
            return {
                "valid": len(errors) == 0,
                "errors": errors,
                "limits": {
                    "cpu": cpu_limit,
                    "memory": memory_limit,
                    "disk": disk_limit
                }
            }
            
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    @staticmethod
    def validate_email_address(email: str) -> Dict[str, Any]:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            if not email or not isinstance(email, str):
                return {"valid": False, "error": "Email must be a non-empty string"}
            
            # Basic email regex pattern
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if not re.match(email_pattern, email):
                return {"valid": False, "error": "Invalid email format"}
            
            return {"valid": True, "email": email}
            
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    @staticmethod
    def validate_url(url: str) -> Dict[str, Any]:
        """
        Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            if not url or not isinstance(url, str):
                return {"valid": False, "error": "URL must be a non-empty string"}
            
            # Basic URL regex pattern
            url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
            
            if not re.match(url_pattern, url):
                return {"valid": False, "error": "Invalid URL format"}
            
            return {"valid": True, "url": url}
            
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    @staticmethod
    def _format_duration(seconds: int) -> str:
        """Format duration in human-readable format."""
        if seconds < 60:
            return f"{seconds} seconds"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} minutes"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours} hours"
        else:
            days = seconds // 86400
            return f"{days} days" 