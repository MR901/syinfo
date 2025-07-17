"""Tests for monitor commands."""

import pytest
from unittest.mock import Mock, patch
from syinfo.cli.commands.monitor_commands import MonitorCommands


class TestMonitorCommands:
    """Test MonitorCommands class."""
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    @patch('syinfo.cli.commands.monitor_commands.MonitoringConfig')
    def test_start_monitoring_success(self, mock_config, mock_monitor):
        """Test successful monitoring start."""
        # Mock SystemMonitor
        mock_monitor_instance = Mock()
        mock_monitor_instance.start_monitoring.return_value = True
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.start_monitoring(
            config_path="config.yaml",
            output_dir="./data",
            interval=60,
            duration=3600,
            format="csv"
        )
        
        assert result["success"] is True
        assert "Monitoring started successfully" in result["message"]
        assert result["details"]["interval"] == 60
        assert result["details"]["duration"] == 3600
        mock_monitor_instance.start_monitoring.assert_called_once_with(
            interval=60, duration=3600
        )
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_start_monitoring_failure(self, mock_monitor):
        """Test monitoring start failure."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.start_monitoring.return_value = False
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.start_monitoring()
        
        assert result["success"] is False
        assert "Failed to start monitoring" in result["error"]
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_start_monitoring_exception(self, mock_monitor):
        """Test monitoring start with exception."""
        mock_monitor.side_effect = Exception("Test error")
        
        result = MonitorCommands.start_monitoring()
        
        assert result["success"] is False
        assert "Test error" in result["error"]
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', False)
    def test_start_monitoring_not_available(self):
        """Test monitoring start when features not available."""
        result = MonitorCommands.start_monitoring()
        
        assert result["success"] is False
        assert "not available" in result["error"]
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_stop_monitoring_success(self, mock_monitor):
        """Test successful monitoring stop."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.stop_monitoring.return_value = True
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.stop_monitoring()
        
        assert result["success"] is True
        assert "Monitoring stopped successfully" in result["message"]
        mock_monitor_instance.stop_monitoring.assert_called_once()
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_stop_monitoring_failure(self, mock_monitor):
        """Test monitoring stop failure."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.stop_monitoring.return_value = False
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.stop_monitoring()
        
        assert result["success"] is False
        assert "Failed to stop monitoring" in result["error"]
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_get_status_success(self, mock_monitor):
        """Test successful status retrieval."""
        mock_stats = {"cpu_percent": 25.5, "memory_percent": 45.2}
        mock_monitor_instance = Mock()
        mock_monitor_instance.get_current_stats.return_value = mock_stats
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.get_status()
        
        assert result["success"] is True
        assert result["data"] == mock_stats
        assert "Current system status" in result["message"]
        mock_monitor_instance.get_current_stats.assert_called_once()
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_get_status_failure(self, mock_monitor):
        """Test status retrieval failure."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.get_current_stats.return_value = None
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.get_status()
        
        assert result["success"] is False
        assert "Unable to get system status" in result["error"]
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_collect_data_success(self, mock_monitor):
        """Test successful data collection."""
        mock_data = {"system": {"cpu": 25.5}, "processes": []}
        mock_monitor_instance = Mock()
        mock_monitor_instance.collect_snapshot.return_value = mock_data
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.collect_data(
            output_dir="./data",
            format="csv",
            include_processes=True,
            include_logs=False
        )
        
        assert result["success"] is True
        assert result["data"] == mock_data
        assert "Data collection completed" in result["message"]
        mock_monitor_instance.collect_snapshot.assert_called_once_with(
            include_processes=True, include_logs=False
        )
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_collect_data_failure(self, mock_monitor):
        """Test data collection failure."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.collect_snapshot.return_value = None
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.collect_data()
        
        assert result["success"] is False
        assert "Failed to collect data" in result["error"]
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_collect_data_exception(self, mock_monitor):
        """Test data collection with exception."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.collect_snapshot.side_effect = Exception("Collection error")
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.collect_data()
        
        assert result["success"] is False
        assert "Collection error" in result["error"]
    
    def test_default_parameters(self):
        """Test default parameter values."""
        with patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True), \
             patch('syinfo.cli.commands.monitor_commands.SystemMonitor') as mock_monitor:
            
            mock_monitor_instance = Mock()
            mock_monitor_instance.start_monitoring.return_value = True
            mock_monitor.return_value = mock_monitor_instance
            
            result = MonitorCommands.start_monitoring()
            
            assert result["success"] is True
            # Should use default values
            mock_monitor_instance.start_monitoring.assert_called_once_with(
                interval=60, duration=None
            )
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_monitor_with_config_path(self, mock_monitor):
        """Test monitoring with config path."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.start_monitoring.return_value = True
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.start_monitoring(config_path="test_config.yaml")
        
        assert result["success"] is True
        # Should pass config_path to SystemMonitor constructor
        mock_monitor.assert_called_once_with(
            config_path="test_config.yaml", output_dir=None
        )
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_monitor_with_output_dir(self, mock_monitor):
        """Test monitoring with output directory."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.start_monitoring.return_value = True
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.start_monitoring(output_dir="./monitoring_data")
        
        assert result["success"] is True
        # Should pass output_dir to SystemMonitor constructor
        mock_monitor.assert_called_once_with(
            config_path=None, output_dir="./monitoring_data"
        )
    
    @patch('syinfo.cli.commands.monitor_commands.MONITORING_AVAILABLE', True)
    @patch('syinfo.cli.commands.monitor_commands.SystemMonitor')
    def test_collect_data_with_custom_params(self, mock_monitor):
        """Test data collection with custom parameters."""
        mock_data = {"test": "data"}
        mock_monitor_instance = Mock()
        mock_monitor_instance.collect_snapshot.return_value = mock_data
        mock_monitor.return_value = mock_monitor_instance
        
        result = MonitorCommands.collect_data(
            output_dir="./custom_data",
            format="json",
            include_processes=False,
            include_logs=True
        )
        
        assert result["success"] is True
        assert result["data"] == mock_data
        mock_monitor_instance.collect_snapshot.assert_called_once_with(
            include_processes=False, include_logs=True
        ) 