"""Tests for CLI input validator."""

import pytest
import os
import tempfile
from pathlib import Path
from syinfo.cli.utils.validator import CLIValidator


class TestCLIValidator:
    """Test CLIValidator class."""
    
    def test_validate_file_path_existing(self, temp_dir):
        """Test file path validation with existing file."""
        # Create a test file
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("test content")
        
        valid, error = CLIValidator.validate_file_path(str(test_file), must_exist=True)
        assert valid is True
        assert error == ""
    
    def test_validate_file_path_nonexistent(self):
        """Test file path validation with non-existent file."""
        valid, error = CLIValidator.validate_file_path("/nonexistent/file.txt", must_exist=True)
        assert valid is False
        assert "does not exist" in error
    
    def test_validate_file_path_new_file(self, temp_dir):
        """Test file path validation for new file."""
        new_file = Path(temp_dir) / "new_file.txt"
        valid, error = CLIValidator.validate_file_path(str(new_file), must_exist=False)
        assert valid is True
        assert error == ""
    
    def test_validate_file_path_empty(self):
        """Test file path validation with empty path."""
        valid, error = CLIValidator.validate_file_path("", must_exist=True)
        assert valid is False
        assert "cannot be empty" in error
    
    def test_validate_directory_path_existing(self, temp_dir):
        """Test directory path validation with existing directory."""
        valid, error = CLIValidator.validate_directory_path(temp_dir, must_exist=True)
        assert valid is True
        assert error == ""
    
    def test_validate_directory_path_nonexistent(self):
        """Test directory path validation with non-existent directory."""
        valid, error = CLIValidator.validate_directory_path("/nonexistent/dir", must_exist=True)
        assert valid is False
        assert "does not exist" in error
    
    def test_validate_directory_path_file(self, temp_dir):
        """Test directory path validation with file path."""
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("test content")
        
        valid, error = CLIValidator.validate_directory_path(str(test_file), must_exist=True)
        assert valid is False
        assert "not a directory" in error
    
    def test_validate_interval_valid(self):
        """Test interval validation with valid values."""
        valid, error = CLIValidator.validate_interval(1)
        assert valid is True
        assert error == ""
        
        valid, error = CLIValidator.validate_interval(3600)
        assert valid is True
        assert error == ""
    
    def test_validate_interval_invalid(self):
        """Test interval validation with invalid values."""
        valid, error = CLIValidator.validate_interval(0)
        assert valid is False
        assert "at least 1 second" in error
        
        valid, error = CLIValidator.validate_interval(3601)
        assert valid is False
        assert "cannot exceed 3600 seconds" in error
    
    def test_validate_duration_valid(self):
        """Test duration validation with valid values."""
        valid, error = CLIValidator.validate_duration(None)
        assert valid is True
        assert error == ""
        
        valid, error = CLIValidator.validate_duration(1)
        assert valid is True
        assert error == ""
        
        valid, error = CLIValidator.validate_duration(86400 * 30)  # 30 days
        assert valid is True
        assert error == ""
    
    def test_validate_duration_invalid(self):
        """Test duration validation with invalid values."""
        valid, error = CLIValidator.validate_duration(0)
        assert valid is False
        assert "at least 1 second" in error
        
        valid, error = CLIValidator.validate_duration(86400 * 31)  # 31 days
        assert valid is False
        assert "cannot exceed 30 days" in error
    
    def test_validate_format_valid(self):
        """Test format validation with valid formats."""
        for format_name in ['csv', 'json', 'yaml']:
            valid, error = CLIValidator.validate_format(format_name)
            assert valid is True
            assert error == ""
    
    def test_validate_format_invalid(self):
        """Test format validation with invalid format."""
        valid, error = CLIValidator.validate_format("invalid")
        assert valid is False
        assert "must be one of" in error
    
    def test_validate_chart_type_valid(self):
        """Test chart type validation with valid types."""
        valid_types = [
            'cpu_usage', 'memory_usage', 'disk_usage', 'network_io',
            'process_count', 'system_load', 'temperature', 'custom'
        ]
        
        for chart_type in valid_types:
            valid, error = CLIValidator.validate_chart_type(chart_type)
            assert valid is True
            assert error == ""
    
    def test_validate_chart_type_invalid(self):
        """Test chart type validation with invalid type."""
        valid, error = CLIValidator.validate_chart_type("invalid_type")
        assert valid is False
        assert "must be one of" in error
    
    def test_validate_config_path_none(self):
        """Test config path validation with None."""
        valid, error = CLIValidator.validate_config_path(None)
        assert valid is True
        assert error == ""
    
    def test_validate_config_path_valid(self, temp_dir):
        """Test config path validation with valid path."""
        config_file = Path(temp_dir) / "config.yaml"
        config_file.write_text("test config")
        
        valid, error = CLIValidator.validate_config_path(str(config_file))
        assert valid is True
        assert error == ""
    
    def test_validate_output_path_none(self):
        """Test output path validation with None."""
        valid, error = CLIValidator.validate_output_path(None)
        assert valid is True
        assert error == ""
    
    def test_validate_output_path_valid(self, temp_dir):
        """Test output path validation with valid path."""
        output_file = Path(temp_dir) / "output.txt"
        valid, error = CLIValidator.validate_output_path(str(output_file))
        assert valid is True
        assert error == ""
    
    def test_validate_monitoring_args_valid(self):
        """Test monitoring arguments validation with valid args."""
        args = {
            'interval': 60,
            'duration': 3600,
            'output_dir': None,
            'config_path': None,
            'format': 'csv'
        }
        
        valid, errors = CLIValidator.validate_monitoring_args(args)
        assert valid is True
        assert len(errors) == 0
    
    def test_validate_monitoring_args_invalid(self):
        """Test monitoring arguments validation with invalid args."""
        args = {
            'interval': 0,  # Invalid
            'duration': 86400 * 31,  # Invalid
            'output_dir': None,
            'config_path': None,
            'format': 'invalid'  # Invalid
        }
        
        valid, errors = CLIValidator.validate_monitoring_args(args)
        assert valid is False
        assert len(errors) == 3
    
    def test_validate_analysis_args_valid(self, temp_dir):
        """Test analysis arguments validation with valid args."""
        data_file = Path(temp_dir) / "data.csv"
        data_file.write_text("test data")
        
        args = {
            'data_file': str(data_file),
            'output_path': None,
            'chart_type': 'cpu_usage'
        }
        
        valid, errors = CLIValidator.validate_analysis_args(args)
        assert valid is True
        assert len(errors) == 0
    
    def test_validate_analysis_args_invalid(self):
        """Test analysis arguments validation with invalid args."""
        args = {
            'data_file': '/nonexistent/file.csv',  # Invalid
            'output_path': None,
            'chart_type': 'invalid_type'  # Invalid
        }
        
        valid, errors = CLIValidator.validate_analysis_args(args)
        assert valid is False
        assert len(errors) == 2
    
    def test_validate_setup_args_valid(self):
        """Test setup arguments validation with valid args."""
        args = {
            'interval_minutes': 5,
            'config_path': None,
            'output_path': None
        }
        
        valid, errors = CLIValidator.validate_setup_args(args)
        assert valid is True
        assert len(errors) == 0
    
    def test_validate_setup_args_invalid(self):
        """Test setup arguments validation with invalid args."""
        args = {
            'interval_minutes': 0,  # Invalid
            'config_path': None,
            'output_path': None
        }
        
        valid, errors = CLIValidator.validate_setup_args(args)
        assert valid is False
        assert len(errors) == 1
    
    def test_print_validation_errors(self, capsys):
        """Test printing validation errors."""
        errors = [
            "Error 1: Invalid interval",
            "Error 2: File not found",
            "Error 3: Invalid format"
        ]
        
        CLIValidator.print_validation_errors(errors)
        captured = capsys.readouterr()
        
        assert "❌ Validation errors:" in captured.out
        assert "1. Error 1: Invalid interval" in captured.out
        assert "2. Error 2: File not found" in captured.out
        assert "3. Error 3: Invalid format" in captured.out
    
    def test_print_validation_errors_empty(self, capsys):
        """Test printing empty validation errors."""
        CLIValidator.print_validation_errors([])
        captured = capsys.readouterr()
        
        assert captured.out == "" 