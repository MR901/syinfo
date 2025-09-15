"""System analyzer examples: health report and cross-surface search."""

from syinfo.analysis.system import SystemAnalyzer


def show_health():
    sa = SystemAnalyzer()
    report = sa.quick_system_health_check()
    print("=== System Health (24h) ===")
    print(f"Platform: {report['system_info']['platform']}")
    print(f"Recent Errors: {len(report.get('recent_errors', []))}")
    print(f"Recent Warnings: {len(report.get('warnings', []))}")


def search_everywhere(term: str):
    sa = SystemAnalyzer()
    result = sa.search_system(term, include_logs=True, include_packages=True)
    print(f"Search term: {term}")
    print(f"Log entries: {len(result.get('log_entries', []))}")
    print(f"Packages: {len(result.get('packages', []))}")


if __name__ == "__main__":
    show_health()
    print()
    search_everywhere("nginx")


