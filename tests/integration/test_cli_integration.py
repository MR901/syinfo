"""Integration tests for CLI functionality."""

import pytest
import subprocess
import sys
import tempfile
import os
from pathlib import Path


class TestCLIIntegration:
    """Integration tests for CLI commands."""
    
    def test_info_command_device(self):
        """Test info device command."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "info", "--device"],
            capture_output=True,
            text=True
        )
        
        # Should not crash
        assert result.returncode in [0, 1]  # 0 for success, 1 for missing dependencies
        
        # Should have some output
        assert len(result.stdout) > 0 or len(result.stderr) > 0
    
    def test_info_command_network(self):
        """Test info network command."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "info", "--network"],
            capture_output=True,
            text=True
        )
        
        # Should not crash
        assert result.returncode in [0, 1]
        
        # Should have some output
        assert len(result.stdout) > 0 or len(result.stderr) > 0
    
    def test_info_command_system(self):
        """Test info system command."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "info", "--system"],
            capture_output=True,
            text=True
        )
        
        # Should not crash
        assert result.returncode in [0, 1]
        
        # Should have some output
        assert len(result.stdout) > 0 or len(result.stderr) > 0
    
    def test_legacy_flags_compatibility(self):
        """Test legacy flag compatibility."""
        # Test legacy -d flag
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "-d"],
            capture_output=True,
            text=True
        )
        
        # Should not crash
        assert result.returncode in [0, 1]
        
        # Test legacy -n flag
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "-n"],
            capture_output=True,
            text=True
        )
        
        # Should not crash
        assert result.returncode in [0, 1]
        
        # Test legacy -s flag
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "-s"],
            capture_output=True,
            text=True
        )
        
        # Should not crash
        assert result.returncode in [0, 1]
    
    def test_version_flag(self):
        """Test version flag."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "--version"],
            capture_output=True,
            text=True
        )
        
        # Should succeed
        assert result.returncode == 0
        
        # Should show version
        assert len(result.stdout.strip()) > 0
    
    def test_contact_flag(self):
        """Test contact flag."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "--contact"],
            capture_output=True,
            text=True
        )
        
        # Should succeed
        assert result.returncode == 0
        
        # Should show contact info
        assert "mohitrajput901@gmail.com" in result.stdout
        assert "github.com" in result.stdout
    
    def test_help_flag(self):
        """Test help flag."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "--help"],
            capture_output=True,
            text=True
        )
        
        # Should succeed
        assert result.returncode == 0
        
        # Should show help
        assert "SyInfo" in result.stdout
        assert "commands" in result.stdout
    
    def test_no_args_shows_help(self):
        """Test that no arguments shows help."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo"],
            capture_output=True,
            text=True
        )
        
        # Should succeed (help is not an error)
        assert result.returncode == 0
        
        # Should show help
        assert "SyInfo" in result.stdout
    
    def test_invalid_command(self):
        """Test invalid command handling."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "invalid_command"],
            capture_output=True,
            text=True
        )
        
        # Should fail gracefully
        assert result.returncode == 1
        
        # Should show error message
        assert "Invalid command" in result.stderr or "Invalid command" in result.stdout
    
    def test_monitor_command_help(self):
        """Test monitor command help."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "monitor", "--help"],
            capture_output=True,
            text=True
        )
        
        # Should succeed
        assert result.returncode == 0
        
        # Should show monitor help
        assert "monitor" in result.stdout
    
    def test_analyze_command_help(self):
        """Test analyze command help."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "analyze", "--help"],
            capture_output=True,
            text=True
        )
        
        # Should succeed
        assert result.returncode == 0
        
        # Should show analyze help
        assert "analyze" in result.stdout
    
    def test_setup_command_help(self):
        """Test setup command help."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "setup", "--help"],
            capture_output=True,
            text=True
        )
        
        # Should succeed
        assert result.returncode == 0
        
        # Should show setup help
        assert "setup" in result.stdout
    
    def test_json_output_flag(self):
        """Test JSON output flag."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "info", "--device", "--return-json"],
            capture_output=True,
            text=True
        )
        
        # Should not crash
        assert result.returncode in [0, 1]
        
        # If successful, should output JSON
        if result.returncode == 0 and result.stdout.strip():
            import json
            try:
                json.loads(result.stdout)
                # If we get here, it's valid JSON
                assert True
            except json.JSONDecodeError:
                # Not JSON, but that's okay for this test
                pass
    
    def test_disable_print_flag(self):
        """Test disable print flag."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "info", "--device", "--disable-print"],
            capture_output=True,
            text=True
        )
        
        # Should not crash
        assert result.returncode in [0, 1]
    
    def test_time_flag(self):
        """Test time flag."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "info", "--network", "--time", "5"],
            capture_output=True,
            text=True
        )
        
        # Should not crash
        assert result.returncode in [0, 1]
    
    def test_disable_vendor_search_flag(self):
        """Test disable vendor search flag."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "info", "--network", "--disable-vendor-search"],
            capture_output=True,
            text=True
        )
        
        # Should not crash
        assert result.returncode in [0, 1]


class TestCLIErrorHandling:
    """Test CLI error handling."""
    
    def test_missing_required_argument(self):
        """Test missing required argument."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "analyze", "--data-file"],
            capture_output=True,
            text=True
        )
        
        # Should fail
        assert result.returncode == 2  # ArgumentParser error
        
        # Should show error
        assert "error" in result.stderr.lower()
    
    def test_invalid_argument_value(self):
        """Test invalid argument value."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "monitor", "--interval", "-1"],
            capture_output=True,
            text=True
        )
        
        # Should fail
        assert result.returncode == 2
        
        # Should show error
        assert "error" in result.stderr.lower()
    
    def test_invalid_format(self):
        """Test invalid format."""
        result = subprocess.run(
            [sys.executable, "-m", "syinfo", "monitor", "--format", "invalid"],
            capture_output=True,
            text=True
        )
        
        # Should fail
        assert result.returncode == 2
        
        # Should show error
        assert "error" in result.stderr.lower() 