"""Comprehensive log analysis examples using syinfo.analysis.logs."""

from datetime import datetime, timedelta

from syinfo.analysis.logs import LogAnalyzer, LogAnalysisConfig


def basic_errors_last_24h():
    analyzer = LogAnalyzer()
    entries = analyzer.query_logs(
        text_filter="failed",
        level_filter=["ERROR", "CRITICAL"],
        time_range=(datetime.now() - timedelta(hours=24), datetime.now()),
        limit=50,
    )
    print(f"Found {len(entries)} error entries in last 24h")
    for e in entries[:5]:
        ts = e.timestamp.isoformat() if e.timestamp else ""
        print(f"{ts} | {e.level or '-'} | {e.process or '-'} | {e.message}")


def advanced_custom_paths_and_regex():
    config = LogAnalysisConfig(
        log_paths=[
            "/var/log/syslog*",
            "/var/log/auth.log*",
            "/var/log/nginx/*.log*",
        ],
        include_rotated=True,
        max_files_per_pattern=20,
        default_limit=500,
    )
    analyzer = LogAnalyzer(config)
    suspicious = analyzer.query_logs(
        regex_pattern=r"(\d{1,3}\.){3}\d{1,3}.*(failed|auth|timeout)",
        level_filter=["WARNING", "ERROR"],
        limit=100,
    )
    print(f"Suspicious matches: {len(suspicious)}")


def security_audit_last_day():
    analyzer = LogAnalyzer()
    indicators = [
        "failed login",
        "authentication failure",
        "invalid user",
        "permission denied",
        "unauthorized",
    ]
    start = datetime.now() - timedelta(days=1)
    counts = {}
    for term in indicators:
        entries = analyzer.query_logs(text_filter=term, time_range=(start, datetime.now()), limit=50)
        if entries:
            counts[term] = len(entries)
    print("Security indicators last 24h:")
    for k, v in counts.items():
        print(f"  {k}: {v}")


def performance_patterns_last_24h():
    analyzer = LogAnalyzer()
    entries = analyzer.query_logs(
        regex_pattern=r"(slow|timeout|memory|cpu|disk|performance)",
        time_range=(datetime.now() - timedelta(hours=24), datetime.now()),
        limit=200,
    )
    stats = analyzer.get_log_statistics(entries)
    hourly = stats.get("hourly_distribution", {})
    peak = max(hourly.items(), key=lambda x: x[1]) if hourly else None
    print(f"Performance entries: {len(entries)}")
    if peak:
        print(f"Peak hour: {peak[0]}:00 with {peak[1]} events")


if __name__ == "__main__":
    print("-- Basic Errors (24h) --")
    basic_errors_last_24h()
    print("\n-- Advanced + Regex --")
    advanced_custom_paths_and_regex()
    print("\n-- Security Audit (24h) --")
    security_audit_last_day()
    print("\n-- Performance (24h) --")
    performance_patterns_last_24h()


