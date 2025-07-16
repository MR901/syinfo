"""Pytest configuration and fixtures for SyInfo tests."""

import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import Mock, patch

from tests import TestConfig


@pytest.fixture(scope="session")
def test_data_dir():
    """Provide test data directory."""
    return TestConfig.get_test_data_dir()


@pytest.fixture(scope="session")
def test_config_dir():
    """Provide test config directory."""
    return TestConfig.get_test_config_dir()


@pytest.fixture
def temp_dir():
    """Provide temporary directory for tests."""
    temp_dir = TestConfig.create_temp_dir()
    yield temp_dir
    TestConfig.cleanup_temp_dir(temp_dir)


@pytest.fixture
def sample_csv_file(temp_dir):
    """Provide sample CSV file for testing."""
    csv_data = TestConfig.create_sample_csv_data()
    csv_file = Path(temp_dir) / "sample_data.csv"
    csv_file.write_text(csv_data)
    return str(csv_file)


@pytest.fixture
def sample_json_file(temp_dir):
    """Provide sample JSON file for testing."""
    import json
    json_data = TestConfig.create_sample_json_data()
    json_file = Path(temp_dir) / "sample_data.json"
    json_file.write_text(json.dumps(json_data, indent=2))
    return str(json_file)


@pytest.fixture
def mock_psutil():
    """Mock psutil for testing."""
    with patch('psutil.cpu_percent', return_value=25.5), \
         patch('psutil.virtual_memory', return_value=Mock(percent=45.2)), \
         patch('psutil.disk_usage', return_value=Mock(percent=60.1)), \
         patch('psutil.process_iter', return_value=[]), \
         patch('psutil.net_io_counters', return_value=Mock(bytes_sent=1000, bytes_recv=2000)):
        yield


@pytest.fixture
def mock_matplotlib():
    """Mock matplotlib for testing."""
    with patch('matplotlib.pyplot.savefig'), \
         patch('matplotlib.pyplot.close'), \
         patch('matplotlib.pyplot.figure'):
        yield


@pytest.fixture
def mock_pandas():
    """Mock pandas for testing."""
    with patch('pandas.read_csv'), \
         patch('pandas.DataFrame'):
        yield


@pytest.fixture
def sample_config_file(temp_dir):
    """Provide sample configuration file for testing."""
    config_content = """
monitoring:
  interval: 60
  output_dir: ./monitoring_data
  include_processes: true
  include_logs: false

collectors:
  system:
    enabled: true
    metrics: [cpu, memory, disk, network]
  process:
    enabled: true
    max_processes: 100
  log:
    enabled: false
    log_files: []
  storage:
    enabled: true

analysis:
  trends:
    enabled: true
    window_size: 10
  anomalies:
    enabled: true
    threshold: 2.0

visualization:
  enabled: true
  output_format: png
  chart_types: [cpu_usage, memory_usage, disk_usage]
"""
    config_file = Path(temp_dir) / "test_config.yaml"
    config_file.write_text(config_content)
    return str(config_file)


@pytest.fixture
def mock_system_info():
    """Mock system information for testing."""
    return {
        "cpu_percent": 25.5,
        "memory_percent": 45.2,
        "disk_percent": 60.1,
        "network_io": {
            "bytes_sent": 1000,
            "bytes_recv": 2000
        },
        "timestamp": "2024-01-01 10:00:00"
    }


@pytest.fixture
def mock_process_info():
    """Mock process information for testing."""
    return [
        {
            "pid": 1234,
            "name": "python",
            "cpu_percent": 5.2,
            "memory_percent": 2.1,
            "status": "running"
        },
        {
            "pid": 5678,
            "name": "bash",
            "cpu_percent": 0.1,
            "memory_percent": 0.5,
            "status": "sleeping"
        }
    ]


@pytest.fixture
def mock_network_info():
    """Mock network information for testing."""
    return {
        "interfaces": {
            "eth0": {
                "ip": "192.168.1.100",
                "mac": "00:11:22:33:44:55",
                "status": "up"
            }
        },
        "connections": [
            {
                "local_address": "127.0.0.1:8080",
                "remote_address": "127.0.0.1:12345",
                "status": "ESTABLISHED"
            }
        ]
    }


@pytest.fixture
def mock_device_info():
    """Mock device information for testing."""
    return {
        "hostname": "test-host",
        "platform": "Linux",
        "architecture": "x86_64",
        "processor": "Intel(R) Core(TM) i7-8700K",
        "memory_total": 16777216,
        "disk_total": 1000000000
    } 