"""Tests for monitoring API."""

import pytest
from unittest.mock import Mock, patch
from syinfo.api.monitoring_api import MonitoringAPI


class TestMonitoringAPI:
    """Test MonitoringAPI class."""
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    @patch('syinfo.api.monitoring_api.MonitoringConfig')
    def test_init_with_config(self, mock_config, mock_monitor):
        """Test API initialization with config."""
        api = MonitoringAPI(config_path="test_config.yaml", output_dir="./data")
        
        assert api.config_path == "test_config.yaml"
        assert api.output_dir == "./data"
        assert api.monitor is not None
        mock_monitor.assert_called_once_with(
            config_path="test_config.yaml", output_dir="./data"
        )
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', False)
    def test_init_without_monitoring(self):
        """Test API initialization without monitoring features."""
        api = MonitoringAPI()
        
        assert api.monitor is None
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    def test_start_monitoring_success(self, mock_monitor):
        """Test successful monitoring start."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.start_monitoring.return_value = True
        mock_monitor.return_value = mock_monitor_instance
        
        api = MonitoringAPI()
        result = api.start_monitoring(
            interval=60,
            duration=3600,
            include_processes=True,
            include_logs=False
        )
        
        assert result["success"] is True
        assert "Monitoring started successfully" in result["message"]
        assert result["details"]["interval"] == 60
        assert result["details"]["duration"] == 3600
        assert result["details"]["include_processes"] is True
        assert result["details"]["include_logs"] is False
        
        mock_monitor_instance.start_monitoring.assert_called_once_with(
            interval=60, duration=3600, include_processes=True, include_logs=False
        )
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    def test_start_monitoring_failure(self, mock_monitor):
        """Test monitoring start failure."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.start_monitoring.return_value = False
        mock_monitor.return_value = mock_monitor_instance
        
        api = MonitoringAPI()
        result = api.start_monitoring()
        
        assert result["success"] is False
        assert "Failed to start monitoring" in result["error"]
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    def test_start_monitoring_exception(self, mock_monitor):
        """Test monitoring start with exception."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.start_monitoring.side_effect = Exception("Test error")
        mock_monitor.return_value = mock_monitor_instance
        
        api = MonitoringAPI()
        result = api.start_monitoring()
        
        assert result["success"] is False
        assert "Test error" in result["error"]
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', False)
    def test_start_monitoring_not_available(self):
        """Test monitoring start when features not available."""
        api = MonitoringAPI()
        result = api.start_monitoring()
        
        assert result["success"] is False
        assert "not available" in result["error"]
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    def test_stop_monitoring_success(self, mock_monitor):
        """Test successful monitoring stop."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.stop_monitoring.return_value = True
        mock_monitor.return_value = mock_monitor_instance
        
        api = MonitoringAPI()
        result = api.stop_monitoring()
        
        assert result["success"] is True
        assert "Monitoring stopped successfully" in result["message"]
        mock_monitor_instance.stop_monitoring.assert_called_once()
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    def test_stop_monitoring_failure(self, mock_monitor):
        """Test monitoring stop failure."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.stop_monitoring.return_value = False
        mock_monitor.return_value = mock_monitor_instance
        
        api = MonitoringAPI()
        result = api.stop_monitoring()
        
        assert result["success"] is False
        assert "Failed to stop monitoring" in result["error"]
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    def test_get_current_stats_success(self, mock_monitor):
        """Test successful stats retrieval."""
        mock_stats = {"cpu_percent": 25.5, "memory_percent": 45.2}
        mock_monitor_instance = Mock()
        mock_monitor_instance.get_current_stats.return_value = mock_stats
        mock_monitor.return_value = mock_monitor_instance
        
        api = MonitoringAPI()
        result = api.get_current_stats()
        
        assert result["success"] is True
        assert result["data"] == mock_stats
        assert "Current stats retrieved successfully" in result["message"]
        mock_monitor_instance.get_current_stats.assert_called_once()
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    def test_get_current_stats_failure(self, mock_monitor):
        """Test stats retrieval failure."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.get_current_stats.return_value = None
        mock_monitor.return_value = mock_monitor_instance
        
        api = MonitoringAPI()
        result = api.get_current_stats()
        
        assert result["success"] is False
        assert "Unable to get current stats" in result["error"]
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    def test_collect_snapshot_success(self, mock_monitor):
        """Test successful snapshot collection."""
        mock_data = {"system": {"cpu": 25.5}, "processes": []}
        mock_monitor_instance = Mock()
        mock_monitor_instance.collect_snapshot.return_value = mock_data
        mock_monitor.return_value = mock_monitor_instance
        
        api = MonitoringAPI()
        result = api.collect_snapshot(
            include_processes=True,
            include_logs=False,
            output_format="json"
        )
        
        assert result["success"] is True
        assert result["data"] == mock_data
        assert "Snapshot collected successfully" in result["message"]
        mock_monitor_instance.collect_snapshot.assert_called_once_with(
            include_processes=True, include_logs=False
        )
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    def test_collect_snapshot_failure(self, mock_monitor):
        """Test snapshot collection failure."""
        mock_monitor_instance = Mock()
        mock_monitor_instance.collect_snapshot.return_value = None
        mock_monitor.return_value = mock_monitor_instance
        
        api = MonitoringAPI()
        result = api.collect_snapshot()
        
        assert result["success"] is False
        assert "Failed to collect snapshot" in result["error"]
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    def test_get_monitoring_status_success(self, mock_monitor):
        """Test successful status retrieval."""
        mock_status = {"running": True, "start_time": "2024-01-01 10:00:00"}
        mock_monitor_instance = Mock()
        mock_monitor_instance.get_status.return_value = mock_status
        mock_monitor.return_value = mock_monitor_instance
        
        api = MonitoringAPI()
        result = api.get_monitoring_status()
        
        assert result["success"] is True
        assert result["data"] == mock_status
        assert "Status retrieved successfully" in result["message"]
        mock_monitor_instance.get_status.assert_called_once()
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    @patch('syinfo.api.monitoring_api.os')
    def test_get_data_files_success(self, mock_os, mock_monitor):
        """Test successful data files retrieval."""
        mock_os.path.exists.return_value = True
        mock_os.listdir.return_value = ["data1.csv", "data2.json", "other.txt"]
        mock_os.path.join.side_effect = lambda *args: "/".join(args)
        mock_os.path.getsize.return_value = 1024
        mock_os.path.getmtime.return_value = 1640995200.0
        
        api = MonitoringAPI(output_dir="./data")
        result = api.get_data_files()
        
        assert result["success"] is True
        assert len(result["data"]) == 2  # Only CSV and JSON files
        assert "Found 2 data files" in result["message"]
        
        # Check file info
        file1 = result["data"][0]
        assert file1["name"] == "data1.csv"
        assert file1["size"] == 1024
        assert file1["modified"] == 1640995200.0
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    @patch('syinfo.api.monitoring_api.os')
    def test_get_data_files_no_directory(self, mock_os, mock_monitor):
        """Test data files retrieval with non-existent directory."""
        mock_os.path.exists.return_value = False
        
        api = MonitoringAPI()
        result = api.get_data_files()
        
        assert result["success"] is True
        assert result["data"] == []
        assert "No data directory found" in result["message"]
    
    @patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True)
    @patch('syinfo.api.monitoring_api.SystemMonitor')
    @patch('syinfo.api.monitoring_api.os')
    def test_get_data_files_with_custom_dir(self, mock_os, mock_monitor):
        """Test data files retrieval with custom directory."""
        mock_os.path.exists.return_value = True
        mock_os.listdir.return_value = ["data.csv"]
        mock_os.path.join.side_effect = lambda *args: "/".join(args)
        mock_os.path.getsize.return_value = 1024
        mock_os.path.getmtime.return_value = 1640995200.0
        
        api = MonitoringAPI()
        result = api.get_data_files(data_dir="./custom_data")
        
        assert result["success"] is True
        assert len(result["data"]) == 1
        mock_os.path.exists.assert_called_with("./custom_data")
    
    def test_default_parameters(self):
        """Test default parameter values."""
        with patch('syinfo.api.monitoring_api.MONITORING_AVAILABLE', True), \
             patch('syinfo.api.monitoring_api.SystemMonitor') as mock_monitor:
            
            mock_monitor_instance = Mock()
            mock_monitor_instance.start_monitoring.return_value = True
            mock_monitor.return_value = mock_monitor_instance
            
            api = MonitoringAPI()
            result = api.start_monitoring()
            
            assert result["success"] is True
            # Should use default values
            mock_monitor_instance.start_monitoring.assert_called_once_with(
                interval=60, duration=None, include_processes=True, include_logs=False
            ) 