"""Analysis: System-level helpers combining logs and package inventory."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import logging
import platform
from dataclasses import dataclass
from pathlib import Path

from .logs import LogAnalyzer, LogAnalysisConfig
from .packages import PackageManager, PackageInfo


logger = logging.getLogger("syinfo.analysis.system")


@dataclass
class HealthReport:
    timestamp: datetime
    system_info: Dict[str, Any]
    log_analysis: Dict[str, Any]
    recent_errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    error: Optional[str] = None


class SystemAnalyzer:
    def __init__(self, log_config: Optional[LogAnalysisConfig] = None) -> None:
        self.log_analyzer = LogAnalyzer(log_config)
        self.package_manager = PackageManager()

    def quick_system_health_check(self) -> Dict[str, Any]:
        report: Dict[str, Any] = {
            "timestamp": datetime.now(),
            "system_info": {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "available_package_managers": [m.value for m in self.package_manager.supported_managers],
            },
            "log_analysis": {},
            "recent_errors": [],
            "warnings": [],
        }

        try:
            recent_time = datetime.now() - timedelta(hours=24)
            errors = self.log_analyzer.query_logs(
                level_filter=["ERROR", "CRITICAL", "ALERT", "EMERGENCY"],
                time_range=(recent_time, datetime.now()),
                limit=50,
            )
            report["recent_errors"] = [
                {
                    "timestamp": e.timestamp,
                    "level": e.level,
                    "process": e.process,
                    "message": (e.message[:200] + "...") if len(e.message) > 200 else e.message,
                }
                for e in errors[:10]
            ]

            warnings = self.log_analyzer.query_logs(
                level_filter=["WARNING"],
                time_range=(recent_time, datetime.now()),
                limit=20,
            )
            report["warnings"] = [
                {
                    "timestamp": e.timestamp,
                    "process": e.process,
                    "message": (e.message[:100] + "...") if len(e.message) > 100 else e.message,
                }
                for e in warnings[:5]
            ]

            all_recent = errors + warnings
            if all_recent:
                report["log_analysis"] = self.log_analyzer.get_log_statistics(all_recent)
        except Exception as exc:
            logger.debug("Error during health check: %s", exc)
            report["error"] = str(exc)

        return report

    def search_system(
        self,
        search_term: str,
        include_logs: bool = True,
        include_packages: bool = True,
        time_range_hours: int = 168,
    ) -> Dict[str, Any]:
        results: Dict[str, Any] = {
            "search_term": search_term,
            "timestamp": datetime.now(),
            "log_entries": [],
            "packages": [],
        }

        if include_logs:
            try:
                start_time = datetime.now() - timedelta(hours=time_range_hours)
                entries = self.log_analyzer.query_logs(
                    text_filter=search_term,
                    time_range=(start_time, datetime.now()),
                    limit=100,
                )
                results["log_entries"] = [
                    {
                        "timestamp": e.timestamp,
                        "level": e.level,
                        "process": e.process,
                        "message": e.message,
                        "file": Path(e.file_path).name if e.file_path else "",
                    }
                    for e in entries
                ]
            except Exception as exc:
                results["log_search_error"] = str(exc)

        if include_packages:
            try:
                packages = self.package_manager.list_packages(name_filter=search_term)
                results["packages"] = [
                    {
                        "name": p.name,
                        "version": p.version,
                        "manager": p.manager,
                        "description": p.description,
                    }
                    for p in packages
                ]
            except Exception as exc:
                results["package_search_error"] = str(exc)

        return results


