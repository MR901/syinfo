"""Tests for monitoring collectors."""

import pytest
from unittest.mock import Mock, patch
from syinfo.monitoring.collector.system_collector import SystemCollector
from syinfo.monitoring.collector.process_collector import ProcessCollector
from syinfo.monitoring.collector.log_collector import LogCollector
from syinfo.monitoring.collector.storage_collector import StorageCollector


class TestSystemCollector:
    """Test SystemCollector class."""
    
    @patch('syinfo.monitoring.collector.system_collector.psutil')
    def test_collect_system_metrics(self, mock_psutil):
        """Test system metrics collection."""
        # Mock psutil methods
        mock_psutil.cpu_percent.return_value = 25.5
        mock_psutil.virtual_memory.return_value = Mock(percent=45.2, total=16777216, available=8388608)
        mock_psutil.disk_usage.return_value = Mock(percent=60.1, total=1000000000, free=400000000)
        mock_psutil.net_io_counters.return_value = Mock(bytes_sent=1000, bytes_recv=2000)
        
        collector = SystemCollector()
        metrics = collector.collect_metrics()
        
        assert "cpu_percent" in metrics
        assert "memory_percent" in metrics
        assert "disk_percent" in metrics
        assert "network_io" in metrics
        assert "timestamp" in metrics
        
        assert metrics["cpu_percent"] == 25.5
        assert metrics["memory_percent"] == 45.2
        assert metrics["disk_percent"] == 60.1
        assert metrics["network_io"]["bytes_sent"] == 1000
        assert metrics["network_io"]["bytes_recv"] == 2000
    
    @patch('syinfo.monitoring.collector.system_collector.psutil')
    def test_collect_system_metrics_with_error(self, mock_psutil):
        """Test system metrics collection with error."""
        mock_psutil.cpu_percent.side_effect = Exception("CPU error")
        
        collector = SystemCollector()
        metrics = collector.collect_metrics()
        
        # Should handle error gracefully
        assert "cpu_percent" in metrics
        assert metrics["cpu_percent"] is None
        assert "error" in metrics
    
    def test_get_metric_names(self):
        """Test getting metric names."""
        collector = SystemCollector()
        names = collector.get_metric_names()
        
        expected_names = ["cpu_percent", "memory_percent", "disk_percent", "network_io"]
        for name in expected_names:
            assert name in names


class TestProcessCollector:
    """Test ProcessCollector class."""
    
    @patch('syinfo.monitoring.collector.process_collector.psutil')
    def test_collect_process_metrics(self, mock_psutil):
        """Test process metrics collection."""
        # Mock process
        mock_process = Mock()
        mock_process.pid = 1234
        mock_process.name.return_value = "python"
        mock_process.cpu_percent.return_value = 5.2
        mock_process.memory_percent.return_value = 2.1
        mock_process.status.return_value = "running"
        
        mock_psutil.process_iter.return_value = [mock_process]
        
        collector = ProcessCollector()
        processes = collector.collect_metrics(max_processes=10)
        
        assert len(processes) == 1
        process = processes[0]
        
        assert process["pid"] == 1234
        assert process["name"] == "python"
        assert process["cpu_percent"] == 5.2
        assert process["memory_percent"] == 2.1
        assert process["status"] == "running"
    
    @patch('syinfo.monitoring.collector.process_collector.psutil')
    def test_collect_process_metrics_with_filter(self, mock_psutil):
        """Test process metrics collection with filter."""
        # Mock processes
        mock_process1 = Mock()
        mock_process1.pid = 1234
        mock_process1.name.return_value = "python"
        mock_process1.cpu_percent.return_value = 5.2
        mock_process1.memory_percent.return_value = 2.1
        mock_process1.status.return_value = "running"
        
        mock_process2 = Mock()
        mock_process2.pid = 5678
        mock_process2.name.return_value = "bash"
        mock_process2.cpu_percent.return_value = 0.1
        mock_process2.memory_percent.return_value = 0.5
        mock_process2.status.return_value = "sleeping"
        
        mock_psutil.process_iter.return_value = [mock_process1, mock_process2]
        
        collector = ProcessCollector()
        processes = collector.collect_metrics(
            max_processes=10,
            name_filter="python"
        )
        
        assert len(processes) == 1
        assert processes[0]["name"] == "python"
    
    @patch('syinfo.monitoring.collector.process_collector.psutil')
    def test_collect_process_metrics_with_error(self, mock_psutil):
        """Test process metrics collection with error."""
        mock_psutil.process_iter.side_effect = Exception("Process error")
        
        collector = ProcessCollector()
        processes = collector.collect_metrics()
        
        # Should handle error gracefully
        assert processes == []
    
    def test_get_metric_names(self):
        """Test getting metric names."""
        collector = ProcessCollector()
        names = collector.get_metric_names()
        
        expected_names = ["pid", "name", "cpu_percent", "memory_percent", "status"]
        for name in expected_names:
            assert name in names


class TestLogCollector:
    """Test LogCollector class."""
    
    @patch('syinfo.monitoring.collector.log_collector.os.path')
    @patch('builtins.open', create=True)
    def test_collect_log_metrics(self, mock_open, mock_path):
        """Test log metrics collection."""
        # Mock file operations
        mock_path.exists.return_value = True
        mock_open.return_value.__enter__.return_value.readlines.return_value = [
            "2024-01-01 10:00:00 INFO: Test log entry 1\n",
            "2024-01-01 10:01:00 ERROR: Test log entry 2\n",
            "2024-01-01 10:02:00 WARNING: Test log entry 3\n"
        ]
        
        collector = LogCollector()
        logs = collector.collect_metrics(log_files=["/var/log/test.log"])
        
        assert len(logs) == 1
        log_file = logs[0]
        
        assert "file_path" in log_file
        assert "entries" in log_file
        assert "error_count" in log_file
        assert "warning_count" in log_file
        assert "info_count" in log_file
        
        assert log_file["file_path"] == "/var/log/test.log"
        assert log_file["error_count"] == 1
        assert log_file["warning_count"] == 1
        assert log_file["info_count"] == 1
    
    @patch('syinfo.monitoring.collector.log_collector.os.path')
    def test_collect_log_metrics_file_not_found(self, mock_path):
        """Test log metrics collection with non-existent file."""
        mock_path.exists.return_value = False
        
        collector = LogCollector()
        logs = collector.collect_metrics(log_files=["/nonexistent/log.log"])
        
        assert len(logs) == 1
        log_file = logs[0]
        assert "error" in log_file
        assert "not found" in log_file["error"]
    
    def test_parse_log_entry(self):
        """Test log entry parsing."""
        collector = LogCollector()
        
        # Test valid log entry
        entry = "2024-01-01 10:00:00 INFO: Test message"
        parsed = collector._parse_log_entry(entry)
        
        assert parsed["timestamp"] == "2024-01-01 10:00:00"
        assert parsed["level"] == "INFO"
        assert parsed["message"] == "Test message"
        
        # Test invalid log entry
        entry = "Invalid log entry"
        parsed = collector._parse_log_entry(entry)
        
        assert parsed["timestamp"] is None
        assert parsed["level"] == "UNKNOWN"
        assert parsed["message"] == "Invalid log entry"
    
    def test_get_metric_names(self):
        """Test getting metric names."""
        collector = LogCollector()
        names = collector.get_metric_names()
        
        expected_names = ["file_path", "entries", "error_count", "warning_count", "info_count"]
        for name in expected_names:
            assert name in names


class TestStorageCollector:
    """Test StorageCollector class."""
    
    @patch('syinfo.monitoring.collector.storage_collector.psutil')
    def test_collect_storage_metrics(self, mock_psutil):
        """Test storage metrics collection."""
        # Mock disk partitions and usage
        mock_partition = Mock()
        mock_partition.device = "/dev/sda1"
        mock_partition.mountpoint = "/"
        mock_partition.fstype = "ext4"
        
        mock_psutil.disk_partitions.return_value = [mock_partition]
        mock_psutil.disk_usage.return_value = Mock(
            total=1000000000,
            used=600000000,
            free=400000000,
            percent=60.0
        )
        
        collector = StorageCollector()
        storage = collector.collect_metrics()
        
        assert len(storage) == 1
        partition = storage[0]
        
        assert partition["device"] == "/dev/sda1"
        assert partition["mountpoint"] == "/"
        assert partition["fstype"] == "ext4"
        assert partition["total"] == 1000000000
        assert partition["used"] == 600000000
        assert partition["free"] == 400000000
        assert partition["percent"] == 60.0
    
    @patch('syinfo.monitoring.collector.storage_collector.psutil')
    def test_collect_storage_metrics_with_error(self, mock_psutil):
        """Test storage metrics collection with error."""
        mock_psutil.disk_partitions.side_effect = Exception("Storage error")
        
        collector = StorageCollector()
        storage = collector.collect_metrics()
        
        # Should handle error gracefully
        assert storage == []
    
    def test_get_metric_names(self):
        """Test getting metric names."""
        collector = StorageCollector()
        names = collector.get_metric_names()
        
        expected_names = ["device", "mountpoint", "fstype", "total", "used", "free", "percent"]
        for name in expected_names:
            assert name in names
    
    def test_format_bytes(self):
        """Test byte formatting."""
        collector = StorageCollector()
        
        assert collector._format_bytes(1024) == "1.0 KB"
        assert collector._format_bytes(1024 * 1024) == "1.0 MB"
        assert collector._format_bytes(1024 * 1024 * 1024) == "1.0 GB"
        assert collector._format_bytes(1024 * 1024 * 1024 * 1024) == "1.0 TB" 