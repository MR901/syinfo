"""Tests for info commands."""

import pytest
from unittest.mock import Mock, patch
from syinfo.cli.commands.info_commands import InfoCommands


class TestInfoCommands:
    """Test InfoCommands class."""
    
    @patch('syinfo.cli.commands.info_commands.DeviceInfo')
    def test_handle_device_info_success(self, mock_device_info):
        """Test successful device info handling."""
        # Mock DeviceInfo
        mock_device_info.get_all.return_value = {"hostname": "test-host"}
        
        result = InfoCommands.handle_device_info(disable_print=False, return_json=False)
        
        assert result["success"] is True
        assert "hostname" in result["data"]
        mock_device_info.get_all.assert_called_once()
    
    @patch('syinfo.cli.commands.info_commands.DeviceInfo')
    def test_handle_device_info_with_json(self, mock_device_info, capsys):
        """Test device info handling with JSON output."""
        mock_device_info.get_all.return_value = {"hostname": "test-host"}
        
        result = InfoCommands.handle_device_info(disable_print=False, return_json=True)
        
        assert result["success"] is True
        captured = capsys.readouterr()
        assert "hostname" in captured.out
    
    @patch('syinfo.cli.commands.info_commands.DeviceInfo')
    def test_handle_device_info_disable_print(self, mock_device_info):
        """Test device info handling with print disabled."""
        mock_device_info.get_all.return_value = {"hostname": "test-host"}
        
        result = InfoCommands.handle_device_info(disable_print=True, return_json=False)
        
        assert result["success"] is True
        # Should not call print method
        mock_device_info.print.assert_not_called()
    
    @patch('syinfo.cli.commands.info_commands.DeviceInfo')
    def test_handle_device_info_error(self, mock_device_info):
        """Test device info handling with error."""
        mock_device_info.get_all.side_effect = Exception("Test error")
        
        result = InfoCommands.handle_device_info()
        
        assert result["success"] is False
        assert "Test error" in result["error"]
    
    @patch('syinfo.cli.commands.info_commands.NetworkInfo')
    def test_handle_network_info_success(self, mock_network_info):
        """Test successful network info handling."""
        mock_network_info.get_all.return_value = {"interfaces": {"eth0": {"ip": "192.168.1.1"}}}
        
        result = InfoCommands.handle_network_info(
            search_period=10,
            search_device_vendor_too=True,
            disable_print=False,
            return_json=False
        )
        
        assert result["success"] is True
        assert "interfaces" in result["data"]
        mock_network_info.get_all.assert_called_once_with(
            search_period=10,
            search_device_vendor_too=True
        )
    
    @patch('syinfo.cli.commands.info_commands.NetworkInfo')
    def test_handle_network_info_with_custom_params(self, mock_network_info):
        """Test network info handling with custom parameters."""
        mock_network_info.get_all.return_value = {"interfaces": {}}
        
        result = InfoCommands.handle_network_info(
            search_period=30,
            search_device_vendor_too=False,
            disable_print=True,
            return_json=True
        )
        
        assert result["success"] is True
        mock_network_info.get_all.assert_called_once_with(
            search_period=30,
            search_device_vendor_too=False
        )
    
    @patch('syinfo.cli.commands.info_commands.NetworkInfo')
    def test_handle_network_info_error(self, mock_network_info):
        """Test network info handling with error."""
        mock_network_info.get_all.side_effect = Exception("Network error")
        
        result = InfoCommands.handle_network_info()
        
        assert result["success"] is False
        assert "Network error" in result["error"]
    
    @patch('syinfo.cli.commands.info_commands.SysInfo')
    def test_handle_system_info_success(self, mock_sys_info):
        """Test successful system info handling."""
        mock_sys_info.get_all.return_value = {
            "device": {"hostname": "test-host"},
            "network": {"interfaces": {}}
        }
        
        result = InfoCommands.handle_system_info(
            search_period=15,
            search_device_vendor_too=True,
            disable_print=False,
            return_json=False
        )
        
        assert result["success"] is True
        assert "device" in result["data"]
        assert "network" in result["data"]
        mock_sys_info.get_all.assert_called_once_with(
            search_period=15,
            search_device_vendor_too=True
        )
    
    @patch('syinfo.cli.commands.info_commands.SysInfo')
    def test_handle_system_info_with_custom_params(self, mock_sys_info):
        """Test system info handling with custom parameters."""
        mock_sys_info.get_all.return_value = {"device": {}, "network": {}}
        
        result = InfoCommands.handle_system_info(
            search_period=60,
            search_device_vendor_too=False,
            disable_print=True,
            return_json=True
        )
        
        assert result["success"] is True
        mock_sys_info.get_all.assert_called_once_with(
            search_period=60,
            search_device_vendor_too=False
        )
    
    @patch('syinfo.cli.commands.info_commands.SysInfo')
    def test_handle_system_info_error(self, mock_sys_info):
        """Test system info handling with error."""
        mock_sys_info.get_all.side_effect = Exception("System error")
        
        result = InfoCommands.handle_system_info()
        
        assert result["success"] is False
        assert "System error" in result["error"]
    
    @patch('syinfo.cli.commands.info_commands.DeviceInfo')
    @patch('syinfo.cli.commands.info_commands.NetworkInfo')
    @patch('syinfo.cli.commands.info_commands.SysInfo')
    def test_import_error_handling(self, mock_sys_info, mock_network_info, mock_device_info):
        """Test handling of import errors."""
        # Simulate import error by making the modules raise ImportError
        mock_device_info.get_all.side_effect = ImportError("Module not found")
        
        result = InfoCommands.handle_device_info()
        
        assert result["success"] is False
        assert "Module not found" in result["error"]
    
    def test_default_parameters(self):
        """Test default parameter values."""
        # Test that methods can be called with default parameters
        with patch('syinfo.cli.commands.info_commands.DeviceInfo') as mock_device:
            mock_device.get_all.return_value = {"test": "data"}
            
            result = InfoCommands.handle_device_info()
            
            assert result["success"] is True
            assert result["data"] == {"test": "data"}
    
    @patch('syinfo.cli.commands.info_commands.DeviceInfo')
    def test_print_called_when_not_disabled(self, mock_device_info):
        """Test that print is called when not disabled."""
        mock_device_info.get_all.return_value = {"test": "data"}
        
        InfoCommands.handle_device_info(disable_print=False)
        
        mock_device_info.print.assert_called_once_with({"test": "data"})
    
    @patch('syinfo.cli.commands.info_commands.DeviceInfo')
    def test_print_not_called_when_disabled(self, mock_device_info):
        """Test that print is not called when disabled."""
        mock_device_info.get_all.return_value = {"test": "data"}
        
        InfoCommands.handle_device_info(disable_print=True)
        
        mock_device_info.print.assert_not_called() 