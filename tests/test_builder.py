"""Tests for the Builder Pattern API (InfoBuilder/SyInfoSystem)."""

import asyncio
import json

from syinfo import InfoBuilder


def test_builder_basic_collect_hardware_only():
    builder = InfoBuilder().include_hardware().enable_caching()
    system = builder.build()
    data = system.collect(scope="hardware")
    assert isinstance(data, dict)
    # Expect core hardware keys to be present
    for key in ("dev_info", "cpu_info", "memory_info"):
        assert key in data


def test_builder_async_network_no_scan():
    # timeout=0 to avoid scanning (no sudo needed)
    builder = InfoBuilder().include_hardware().include_network(timeout=0, include_vendor_info=False)
    system = builder.build()

    data = asyncio.run(system.collect_async(scope="network"))
    assert isinstance(data, dict)
    assert "network_info" in data


def test_builder_create_monitors():
    builder = InfoBuilder().include_hardware().include_monitoring(interval=1)
    system = builder.build()
    mon = system.create_monitor()
    assert hasattr(mon, "start") and hasattr(mon, "stop")

    builder2 = InfoBuilder().include_process_monitoring(filters=["python"], interval=1)
    system2 = builder2.build()
    pmon = system2.create_process_monitor()
    assert hasattr(pmon, "start") and hasattr(pmon, "stop")


def test_builder_logs_and_packages_analysis():
    # Logs (limit small; entries may be empty depending on system)
    builder_logs = InfoBuilder().include_logs(limit=1)
    sys_logs = builder_logs.build()
    logs = sys_logs.analyze_logs()
    assert isinstance(logs, dict) and isinstance(logs.get("log_entries", []), list)

    # Packages (filter optional; result may be empty)
    builder_pkgs = InfoBuilder().include_packages(name_filter="python")
    sys_pkgs = builder_pkgs.build()
    pkgs = sys_pkgs.analyze_packages()
    assert isinstance(pkgs, dict) and isinstance(pkgs.get("packages", []), list)


def test_builder_export_and_summary():
    system = InfoBuilder().include_hardware().enable_caching().build()
    data = system.collect(scope="hardware")
    export_str = system.export(data)
    # Must be valid JSON string by default
    obj = json.loads(export_str)
    assert isinstance(obj, dict)

    # Summary contains feature names
    summary = system.summary()
    assert isinstance(summary, str)
    assert "SyInfo System" in summary


def test_builder_presets_summary_only():
    # basic_system preset
    sys_basic = InfoBuilder.basic_system().build()
    assert "SyInfo System" in sys_basic.summary()

    # full_system preset (do not collect to avoid scans), just check summary flags
    sys_full = InfoBuilder.full_system().build()
    summary_full = sys_full.summary()
    assert "SyInfo System" in summary_full
    assert ("Network" in summary_full) or ("Basic" in summary_full)  # depending on availability

    # monitoring_system preset
    sys_mon = InfoBuilder.monitoring_system(interval=1).build()
    assert "SyInfo System" in sys_mon.summary()


def test_builder_export_yaml_and_csv():
    # YAML
    sys_yaml = (InfoBuilder()
                .include_hardware()
                .export_as("yaml")
                .build())
    y = sys_yaml.export(sys_yaml.collect(scope="hardware"))
    assert isinstance(y, str) and len(y) > 0

    # CSV
    sys_csv = (InfoBuilder()
               .include_hardware()
               .export_as("csv")
               .build())
    c = sys_csv.export(sys_csv.collect(scope="hardware"))
    assert isinstance(c, str) and "Property" in c and "Value" in c


def test_builder_caching_returns_same_content():
    sys_cached = (InfoBuilder()
                  .include_hardware()
                  .enable_caching(ttl=600)
                  .build())
    d1 = sys_cached.collect(scope="hardware")
    d2 = sys_cached.collect(scope="hardware")
    # With caching enabled, subsequent calls should return equal content
    assert d1 == d2


def test_builder_packages_with_manager_type():
    # Request a specific manager; ensure call succeeds
    sys_pkgs_mgr = (InfoBuilder()
                    .include_packages(manager_types=["pip"], name_filter="pip")
                    .build())
    pkgs = sys_pkgs_mgr.analyze_packages()
    assert isinstance(pkgs, dict)
    assert "packages" in pkgs


