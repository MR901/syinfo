"""Tests for CLI output formatter."""

import pytest
from syinfo.cli.utils.formatter import OutputFormatter


class TestOutputFormatter:
    """Test OutputFormatter class."""
    
    def test_colorize(self):
        """Test colorize method."""
        # Test with valid color
        result = OutputFormatter.colorize("test", "GREEN")
        assert "test" in result
        assert "\033[92m" in result  # Green color code
        assert "\033[0m" in result   # Reset color code
        
        # Test with invalid color
        result = OutputFormatter.colorize("test", "INVALID")
        assert result == "test"
    
    def test_success_message(self):
        """Test success message formatting."""
        result = OutputFormatter.success("Operation completed")
        assert "✅" in result
        assert "Operation completed" in result
        assert "\033[92m" in result  # Green color
    
    def test_error_message(self):
        """Test error message formatting."""
        result = OutputFormatter.error("Operation failed")
        assert "❌" in result
        assert "Operation failed" in result
        assert "\033[91m" in result  # Red color
    
    def test_warning_message(self):
        """Test warning message formatting."""
        result = OutputFormatter.warning("Warning message")
        assert "⚠️" in result
        assert "Warning message" in result
        assert "\033[93m" in result  # Yellow color
    
    def test_info_message(self):
        """Test info message formatting."""
        result = OutputFormatter.info("Info message")
        assert "ℹ️" in result
        assert "Info message" in result
        assert "\033[94m" in result  # Blue color
    
    def test_header_formatting(self):
        """Test header formatting."""
        result = OutputFormatter.header("Test Header")
        assert "Test Header" in result
        assert "\033[1m" in result  # Bold
    
    def test_section_formatting(self):
        """Test section formatting."""
        result = OutputFormatter.section("Test Section")
        assert "Test Section:" in result
        assert "\033[96m" in result  # Cyan color
    
    def test_format_json(self):
        """Test JSON formatting."""
        data = {"key": "value", "number": 42}
        result = OutputFormatter.format_json(data)
        
        # Should be valid JSON
        import json
        parsed = json.loads(result)
        assert parsed["key"] == "value"
        assert parsed["number"] == 42
    
    def test_format_table(self):
        """Test table formatting."""
        headers = ["Name", "Age", "City"]
        rows = [
            ["Alice", "25", "New York"],
            ["Bob", "30", "London"],
            ["Charlie", "35", "Paris"]
        ]
        
        result = OutputFormatter.format_table(headers, rows)
        
        # Check structure
        lines = result.split('\n')
        assert len(lines) >= 5  # Header + separator + 3 data rows
        
        # Check header
        assert "Name" in lines[0]
        assert "Age" in lines[0]
        assert "City" in lines[0]
        
        # Check separator
        assert "-" in lines[1]
        
        # Check data rows
        assert "Alice" in lines[2]
        assert "Bob" in lines[3]
        assert "Charlie" in lines[4]
    
    def test_format_table_empty(self):
        """Test table formatting with empty data."""
        result = OutputFormatter.format_table([], [])
        assert result == ""
        
        result = OutputFormatter.format_table(["Header"], [])
        assert result == ""
    
    def test_print_result_success(self, capsys):
        """Test print_result with success."""
        result = {
            "success": True,
            "message": "Operation completed",
            "data": {"key": "value"}
        }
        
        OutputFormatter.print_result(result)
        captured = capsys.readouterr()
        
        assert "✅" in captured.out
        assert "Operation completed" in captured.out
        assert "Data" in captured.out
    
    def test_print_result_error(self, capsys):
        """Test print_result with error."""
        result = {
            "success": False,
            "error": "Operation failed"
        }
        
        OutputFormatter.print_result(result)
        captured = capsys.readouterr()
        
        assert "❌" in captured.out
        assert "Operation failed" in captured.out
    
    def test_print_result_json_format(self, capsys):
        """Test print_result with JSON format."""
        result = {
            "success": True,
            "message": "Test message",
            "data": {"key": "value"}
        }
        
        OutputFormatter.print_result(result, format="json")
        captured = capsys.readouterr()
        
        # Should be valid JSON
        import json
        parsed = json.loads(captured.out)
        assert parsed["success"] is True
        assert parsed["message"] == "Test message"
    
    def test_print_result_with_template(self, capsys):
        """Test print_result with template data."""
        result = {
            "success": True,
            "message": "Cron template generated",
            "data": {"template": "* * * * * /usr/bin/syinfo monitor --collect"},
            "instructions": "Add to crontab manually"
        }
        
        OutputFormatter.print_result(result)
        captured = capsys.readouterr()
        
        assert "✅" in captured.out
        assert "Cron template generated" in captured.out
        assert "Cron Template" in captured.out
        assert "* * * * *" in captured.out
        assert "⚠️" in captured.out
        assert "Add to crontab manually" in captured.out
    
    def test_print_contact(self):
        """Test print_contact method."""
        result = OutputFormatter.print_contact()
        
        assert "Contact Information:" in result
        assert "mohitrajput901@gmail.com" in result
        assert "https://github.com/MR901/syinfo" in result
        assert "\033[1m" in result  # Bold formatting
        assert "\033[94m" in result  # Blue color 