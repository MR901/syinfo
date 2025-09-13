"""Core functionality tests for SyInfo."""

import pytest

import syinfo
from syinfo.exceptions import SyInfoException


def test_import():
    """Test that syinfo imports correctly."""
    assert hasattr(syinfo, "get_system_info")
    assert hasattr(syinfo, "get_hardware_info")


def test_get_available_features():
    """Test feature detection."""
    features = syinfo.get_available_features()
    assert isinstance(features, dict)
    assert "core" in features
    assert features["core"] is True


def test_get_system_info_structure():
    """Test system info returns expected structure."""
    info = syinfo.get_complete_info(include_network=False)
    assert isinstance(info, dict)
    # Basic structure validation
    expected_keys = ["dev_info", "cpu_info", "memory_info", "time"]
    for key in expected_keys:
        assert key in info, f"Missing key: {key}"


def test_get_hardware_info():
    """Test hardware info collection."""
    hardware = syinfo.get_hardware_info()
    assert isinstance(hardware, dict)
    assert "cpu" in hardware
    assert "memory" in hardware


def test_export_system_info():
    """Test export functionality."""
    # Test JSON export
    result = syinfo.export_system_info("json")
    assert isinstance(result, str)
    assert len(result) > 0

    # Test invalid format
    with pytest.raises(SyInfoException):
        syinfo.export_system_info("invalid_format")


def test_simple_monitoring():
    """Test simple monitoring creation."""
    monitor = syinfo.create_simple_monitor(interval=1)
    assert monitor is not None
    assert hasattr(monitor, "start")
    assert hasattr(monitor, "stop")
