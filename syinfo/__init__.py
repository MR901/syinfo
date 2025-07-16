
# from __future__ import absolute_import
from ._version import __version__

# Legacy imports (unchanged for backward compatibility)
from .device_info import DeviceInfo
from .network_info import NetworkInfo
from .sys_info import SysInfo, print_brief_sys_info

# New monitoring imports
try:
    from .monitoring.core import SystemMonitor, ProcessMonitor, LogAnalyzer, StorageAnalyzer
    from .monitoring.data import DataCollector, DataAnalyzer, DataVisualizer
    from .monitoring.scheduler import CronManager, RecoveryManager
    from .monitoring.utils import MonitoringConfig, MonitoringLogger
    
    MONITORING_AVAILABLE = True
except ImportError:
    # Monitoring modules not available (e.g., missing dependencies)
    MONITORING_AVAILABLE = False
    
    # Create dummy classes for backward compatibility
    class SystemMonitor:
        def __init__(self, *args, **kwargs):
            raise ImportError("Monitoring features not available. Install required dependencies.")
    
    class ProcessMonitor:
        def __init__(self, *args, **kwargs):
            raise ImportError("Monitoring features not available. Install required dependencies.")
    
    class LogAnalyzer:
        def __init__(self, *args, **kwargs):
            raise ImportError("Monitoring features not available. Install required dependencies.")
    
    class StorageAnalyzer:
        def __init__(self, *args, **kwargs):
            raise ImportError("Monitoring features not available. Install required dependencies.")
    
    class DataCollector:
        def __init__(self, *args, **kwargs):
            raise ImportError("Monitoring features not available. Install required dependencies.")
    
    class DataAnalyzer:
        def __init__(self, *args, **kwargs):
            raise ImportError("Monitoring features not available. Install required dependencies.")
    
    class DataVisualizer:
        def __init__(self, *args, **kwargs):
            raise ImportError("Monitoring features not available. Install required dependencies.")
    
    class CronManager:
        def __init__(self, *args, **kwargs):
            raise ImportError("Monitoring features not available. Install required dependencies.")
    
    class RecoveryManager:
        def __init__(self, *args, **kwargs):
            raise ImportError("Monitoring features not available. Install required dependencies.")
    
    class MonitoringConfig:
        def __init__(self, *args, **kwargs):
            raise ImportError("Monitoring features not available. Install required dependencies.")
    
    class MonitoringLogger:
        def __init__(self, *args, **kwargs):
            raise ImportError("Monitoring features not available. Install required dependencies.")

__all__ = [
    # Legacy exports (unchanged)
    "__version__",
    "DeviceInfo",
    "NetworkInfo", 
    "SysInfo",
    "print_brief_sys_info",
    
    # New monitoring exports
    "SystemMonitor",
    "ProcessMonitor",
    "LogAnalyzer", 
    "StorageAnalyzer",
    "DataCollector",
    "DataAnalyzer",
    "DataVisualizer",
    "CronManager",
    "RecoveryManager",
    "MonitoringConfig",
    "MonitoringLogger",
    
    # Feature availability flag
    "MONITORING_AVAILABLE"
]
