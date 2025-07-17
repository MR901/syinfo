"""
Cron job management for monitoring system.

This module provides cron job template generation, validation, and management
with proper error handling and safety checks.
"""

import os
import subprocess
import tempfile
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import re

from ..utils.logger import MonitoringLogger
from ..utils.validation import InputValidator


class CronManager:
    """
    Cron job management with validation and safety checks.
    
    Features:
    - Cron job template generation
    - Job validation and testing
    - Conflict detection
    - Backup and restore functionality
    - User-friendly setup scripts
    """
    
    def __init__(self):
        """Initialize cron manager."""
        self.logger = MonitoringLogger()
    
    def generate_cron_template(self, interval_minutes: int = 1, 
                             data_dir: Optional[str] = None,
                             config_path: Optional[str] = None) -> str:
        """
        Generate cron job template for monitoring.
        
        Args:
            interval_minutes: Monitoring interval in minutes
            data_dir: Data directory path
            config_path: Configuration file path
            
        Returns:
            Cron job template string
        """
        try:
            # Validate inputs
            if interval_minutes < 1 or interval_minutes > 60:
                raise ValueError("Interval must be between 1 and 60 minutes")
            
            # Default values
            data_dir = data_dir or "/var/log/syinfo/monitoring"
            config_path = config_path or "/etc/syinfo/monitoring_config.yaml"
            
            # Generate cron template
            template = f"""# SyInfo Monitoring Cron Jobs
# Generated on: {self._get_current_time()}
# Interval: {interval_minutes} minutes

# System monitoring job
*/{interval_minutes} * * * * cd {data_dir} && python3 -m syinfo.monitoring.core.monitor --system --config {config_path} --output-dir {data_dir} >> {data_dir}/monitoring.log 2>&1

# Process monitoring job  
*/{interval_minutes} * * * * cd {data_dir} && python3 -m syinfo.monitoring.core.monitor --process --config {config_path} --output-dir {data_dir} >> {data_dir}/monitoring.log 2>&1

# Cleanup old data (daily at 2 AM)
0 2 * * * find {data_dir} -name "*.csv" -mtime +7 -delete >> {data_dir}/cleanup.log 2>&1

# Log rotation (weekly on Sunday at 3 AM)
0 3 * * 0 logrotate /etc/logrotate.d/syinfo-monitoring >> {data_dir}/logrotate.log 2>&1
"""
            
            self.logger.log_monitoring_event(
                "CRON_TEMPLATE_GENERATED",
                f"Generated cron template for {interval_minutes} minute interval",
                "INFO"
            )
            
            return template
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to generate cron template")
            return ""
    
    def validate_cron_setup(self) -> Dict[str, Any]:
        """
        Validate current cron job configuration.
        
        Returns:
            Dictionary with validation results
        """
        try:
            # Get current crontab
            current_crontab = self._get_current_crontab()
            
            # Check for SyInfo monitoring jobs
            syinfo_jobs = []
            for line in current_crontab.split('\n'):
                if 'syinfo' in line.lower() and not line.strip().startswith('#'):
                    syinfo_jobs.append(line.strip())
            
            # Validate job format
            valid_jobs = []
            invalid_jobs = []
            
            for job in syinfo_jobs:
                if self._validate_cron_job(job):
                    valid_jobs.append(job)
                else:
                    invalid_jobs.append(job)
            
            return {
                "valid": len(invalid_jobs) == 0,
                "total_jobs": len(syinfo_jobs),
                "valid_jobs": len(valid_jobs),
                "invalid_jobs": len(invalid_jobs),
                "invalid_job_details": invalid_jobs
            }
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to validate cron setup")
            return {"valid": False, "error": str(e)}
    
    def setup_monitoring_jobs(self, config: Dict[str, Any]) -> bool:
        """
        Setup monitoring cron jobs with proper configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate configuration
            config_validation = InputValidator.validate_config_data(config)
            if not config_validation['valid']:
                self.logger.log_monitoring_event(
                    "CRON_SETUP_FAILED",
                    f"Invalid configuration: {config_validation['errors']}",
                    "ERROR"
                )
                return False
            
            # Get monitoring settings
            monitoring = config.get('monitoring', {})
            system = monitoring.get('system', {})
            interval_minutes = max(1, system.get('interval', 60) // 60)
            
            # Generate cron template
            template = self.generate_cron_template(
                interval_minutes=interval_minutes,
                data_dir=monitoring.get('storage', {}).get('data_directory'),
                config_path=config.get('config_path')
            )
            
            if not template:
                return False
            
            # Install cron jobs
            return self._install_cron_jobs(template)
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to setup monitoring jobs")
            return False
    
    def remove_monitoring_jobs(self) -> bool:
        """
        Remove SyInfo monitoring cron jobs.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current crontab
            current_crontab = self._get_current_crontab()
            
            # Filter out SyInfo jobs
            lines = current_crontab.split('\n')
            filtered_lines = []
            
            skip_next = False
            for line in lines:
                if 'syinfo' in line.lower():
                    skip_next = True
                    continue
                elif skip_next and line.strip().startswith('#'):
                    skip_next = False
                    continue
                elif skip_next and not line.strip():
                    skip_next = False
                    continue
                
                if not skip_next:
                    filtered_lines.append(line)
            
            # Install filtered crontab
            new_crontab = '\n'.join(filtered_lines)
            return self._install_crontab(new_crontab)
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to remove monitoring jobs")
            return False
    
    def backup_crontab(self, backup_path: Optional[str] = None) -> str:
        """
        Backup current crontab.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            Path to backup file
        """
        try:
            if not backup_path:
                backup_path = f"/tmp/crontab_backup_{self._get_current_time()}.txt"
            
            current_crontab = self._get_current_crontab()
            
            with open(backup_path, 'w') as f:
                f.write(current_crontab)
            
            self.logger.log_monitoring_event(
                "CRONTAB_BACKUP",
                f"Crontab backed up to {backup_path}",
                "INFO"
            )
            
            return backup_path
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to backup crontab")
            return ""
    
    def restore_crontab(self, backup_path: str) -> bool:
        """
        Restore crontab from backup.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(backup_path):
                self.logger.log_monitoring_event(
                    "CRONTAB_RESTORE_FAILED",
                    f"Backup file not found: {backup_path}",
                    "ERROR"
                )
                return False
            
            with open(backup_path, 'r') as f:
                crontab_content = f.read()
            
            return self._install_crontab(crontab_content)
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to restore crontab")
            return False
    
    def _get_current_crontab(self) -> str:
        """Get current crontab content."""
        try:
            result = subprocess.run(['crontab', '-l'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return result.stdout
            else:
                return ""
        except subprocess.TimeoutExpired:
            self.logger.log_monitoring_event("CRONTAB_TIMEOUT", "Timeout getting crontab", "WARNING")
            return ""
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to get current crontab")
            return ""
    
    def _install_crontab(self, crontab_content: str) -> bool:
        """Install crontab content."""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(crontab_content)
                temp_file = f.name
            
            # Install crontab
            result = subprocess.run(['crontab', temp_file], 
                                  capture_output=True, text=True, timeout=10)
            
            # Clean up
            os.unlink(temp_file)
            
            if result.returncode == 0:
                self.logger.log_monitoring_event("CRONTAB_INSTALLED", "Crontab installed successfully", "INFO")
                return True
            else:
                self.logger.log_monitoring_event(
                    "CRONTAB_INSTALL_FAILED",
                    f"Failed to install crontab: {result.stderr}",
                    "ERROR"
                )
                return False
                
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to install crontab")
            return False
    
    def _install_cron_jobs(self, template: str) -> bool:
        """Install cron jobs from template."""
        try:
            # Get current crontab
            current_crontab = self._get_current_crontab()
            
            # Append template to current crontab
            new_crontab = current_crontab.rstrip() + "\n\n" + template
            
            return self._install_crontab(new_crontab)
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to install cron jobs")
            return False
    
    def _validate_cron_job(self, job_line: str) -> bool:
        """Validate cron job format."""
        try:
            # Basic cron job format validation
            parts = job_line.split()
            if len(parts) < 6:
                return False
            
            # Check if it's a valid cron expression
            cron_parts = parts[:5]
            for part in cron_parts:
                if not self._is_valid_cron_part(part):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _is_valid_cron_part(self, part: str) -> bool:
        """Check if cron part is valid."""
        try:
            # Allow common cron patterns
            valid_patterns = [
                r'^\*$',           # *
                r'^\d+$',          # number
                r'^\d+-\d+$',      # range
                r'^\d+/\d+$',      # step
                r'^\d+(,\d+)*$',   # list
                r'^\*/\d+$'        # */number
            ]
            
            for pattern in valid_patterns:
                if re.match(pattern, part):
                    return True
            
            return False
            
        except Exception:
            return False
    
    def _get_current_time(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S") 