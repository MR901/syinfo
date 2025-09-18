"""Core functionality tests for SyInfo (updated for new API)."""

import json
import subprocess
import sys

import pytest

from syinfo import (
    DeviceInfo,
    SystemInfo,
    SystemMonitor,
    ProcessMonitor,
    Logger,
    LoggerConfig,
    InfoBuilder,
)
from syinfo.exceptions import ValidationError


def test_public_api_available():
    """Core classes and builder are exposed at package root."""
    assert DeviceInfo is not None
    assert SystemInfo is not None
    assert SystemMonitor is not None
    assert ProcessMonitor is not None
    assert Logger is not None and LoggerConfig is not None
    assert InfoBuilder is not None


def test_device_info_structure():
    """DeviceInfo.get_all returns expected top-level keys."""
    info = DeviceInfo.get_all()
    assert isinstance(info, dict)
    for key in ("dev_info", "cpu_info", "memory_info", "time"):
        assert key in info


def test_system_info_structure_without_network_scan():
    """SystemInfo.get_all includes network_info when requested, without scanning."""
    info = SystemInfo.get_all(search_period=0, search_device_vendor_too=False)
    assert isinstance(info, dict)
    assert "network_info" in info
    # Still retains device info keys
    for key in ("dev_info", "cpu_info", "memory_info"):
        assert key in info


def test_export_device_info_and_invalid_format():
    """Export returns string and invalid format raises ValidationError."""
    exported = DeviceInfo.export("json")
    assert isinstance(exported, str) and exported.strip().startswith("{")

    with pytest.raises(ValidationError):
        DeviceInfo.export("invalid_format")


def test_monitor_classes_instantiable():
    """SystemMonitor/ProcessMonitor can be created and have start/stop."""
    sm = SystemMonitor(interval=1)
    pm = ProcessMonitor(interval=1)
    for m in (sm, pm):
        assert hasattr(m, "start") and hasattr(m, "stop")


def test_cli_device_json_is_pure_json():
    """CLI device JSON should be valid JSON on stdout with no noise."""
    proc = subprocess.run(
        [sys.executable, "-m", "syinfo", "-d", "--json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=True,
    )
    # stderr should be empty in JSON mode (warnings/errors go to stderr only when needed)
    assert proc.stderr.strip() == ""
    # stdout must be valid JSON
    data = json.loads(proc.stdout)
    assert isinstance(data, dict)
    assert "dev_info" in data
