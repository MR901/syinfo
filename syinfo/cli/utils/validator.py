"""CLI Input Validator

Handles validation of CLI input parameters.
"""

import os
import sys
from typing import Dict, Any, List, Optional, Tuple


class CLIValidator:
    """Validate CLI input parameters."""
    
    @staticmethod
    def validate_file_path(file_path: str, must_exist: bool = True) -> Tuple[bool, str]:
        """Validate file path."""
        if not file_path:
            return False, "File path cannot be empty"
        
        if must_exist and not os.path.exists(file_path):
            return False, f"File does not exist: {file_path}"
        
        # Check if directory exists for new files
        if not must_exist:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                return False, f"Directory does not exist: {directory}"
        
        return True, ""
    
    @staticmethod
    def validate_directory_path(dir_path: str, must_exist: bool = True) -> Tuple[bool, str]:
        """Validate directory path."""
        if not dir_path:
            return False, "Directory path cannot be empty"
        
        if must_exist and not os.path.exists(dir_path):
            return False, f"Directory does not exist: {dir_path}"
        
        if must_exist and not os.path.isdir(dir_path):
            return False, f"Path is not a directory: {dir_path}"
        
        return True, ""
    
    @staticmethod
    def validate_interval(interval: int) -> Tuple[bool, str]:
        """Validate monitoring interval."""
        if interval < 1:
            return False, "Interval must be at least 1 second"
        
        if interval > 3600:  # 1 hour
            return False, "Interval cannot exceed 3600 seconds (1 hour)"
        
        return True, ""
    
    @staticmethod
    def validate_duration(duration: Optional[int]) -> Tuple[bool, str]:
        """Validate monitoring duration."""
        if duration is None:
            return True, ""  # Continuous monitoring
        
        if duration < 1:
            return False, "Duration must be at least 1 second"
        
        if duration > 86400 * 30:  # 30 days
            return False, "Duration cannot exceed 30 days"
        
        return True, ""
    
    @staticmethod
    def validate_format(format: str) -> Tuple[bool, str]:
        """Validate output format."""
        valid_formats = ['csv', 'json', 'yaml']
        if format.lower() not in valid_formats:
            return False, f"Format must be one of: {', '.join(valid_formats)}"
        
        return True, ""
    
    @staticmethod
    def validate_chart_type(chart_type: str) -> Tuple[bool, str]:
        """Validate chart type."""
        valid_types = [
            'cpu_usage', 'memory_usage', 'disk_usage', 'network_io',
            'process_count', 'system_load', 'temperature', 'custom'
        ]
        if chart_type.lower() not in valid_types:
            return False, f"Chart type must be one of: {', '.join(valid_types)}"
        
        return True, ""
    
    @staticmethod
    def validate_config_path(config_path: Optional[str]) -> Tuple[bool, str]:
        """Validate configuration file path."""
        if config_path is None:
            return True, ""  # Optional
        
        return CLIValidator.validate_file_path(config_path, must_exist=True)
    
    @staticmethod
    def validate_output_path(output_path: Optional[str]) -> Tuple[bool, str]:
        """Validate output file path."""
        if output_path is None:
            return True, ""  # Optional
        
        return CLIValidator.validate_file_path(output_path, must_exist=False)
    
    @staticmethod
    def validate_monitoring_args(args: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate monitoring command arguments."""
        errors = []
        
        # Validate interval
        if 'interval' in args:
            valid, error = CLIValidator.validate_interval(args['interval'])
            if not valid:
                errors.append(error)
        
        # Validate duration
        if 'duration' in args:
            valid, error = CLIValidator.validate_duration(args['duration'])
            if not valid:
                errors.append(error)
        
        # Validate output directory
        if 'output_dir' in args and args['output_dir']:
            valid, error = CLIValidator.validate_directory_path(args['output_dir'], must_exist=False)
            if not valid:
                errors.append(error)
        
        # Validate config path
        if 'config_path' in args:
            valid, error = CLIValidator.validate_config_path(args['config_path'])
            if not valid:
                errors.append(error)
        
        # Validate format
        if 'format' in args:
            valid, error = CLIValidator.validate_format(args['format'])
            if not valid:
                errors.append(error)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_analysis_args(args: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate analysis command arguments."""
        errors = []
        
        # Validate data file
        if 'data_file' in args:
            valid, error = CLIValidator.validate_file_path(args['data_file'])
            if not valid:
                errors.append(error)
        
        # Validate output path
        if 'output_path' in args:
            valid, error = CLIValidator.validate_output_path(args['output_path'])
            if not valid:
                errors.append(error)
        
        # Validate chart type
        if 'chart_type' in args:
            valid, error = CLIValidator.validate_chart_type(args['chart_type'])
            if not valid:
                errors.append(error)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_setup_args(args: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate setup command arguments."""
        errors = []
        
        # Validate interval for cron jobs
        if 'interval_minutes' in args:
            if args['interval_minutes'] < 1:
                errors.append("Cron interval must be at least 1 minute")
            elif args['interval_minutes'] > 60:
                errors.append("Cron interval cannot exceed 60 minutes")
        
        # Validate config path
        if 'config_path' in args:
            valid, error = CLIValidator.validate_config_path(args['config_path'])
            if not valid:
                errors.append(error)
        
        # Validate output path for config creation
        if 'output_path' in args:
            valid, error = CLIValidator.validate_output_path(args['output_path'])
            if not valid:
                errors.append(error)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def print_validation_errors(errors: List[str]) -> None:
        """Print validation errors in a formatted way."""
        if not errors:
            return
        
        print("❌ Validation errors:")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
        print() 