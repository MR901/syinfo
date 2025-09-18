"""Analysis example: Minimal log query demo."""

from datetime import datetime, timedelta

from syinfo.analysis.logs import LogAnalyzer, LogAnalysisConfig


def main() -> None:
    # Minimal config (use defaults)
    config = LogAnalysisConfig()
    analyzer = LogAnalyzer(config)

    # Query last 12 hours for generic issues (limit small for demo)
    start = datetime.now() - timedelta(hours=12)
    entries = analyzer.query_logs(time_range=(start, datetime.now()), limit=10)
    print(f"Entries found: {len(entries)}")
    for e in entries[:3]:
        ts = e.timestamp.isoformat() if e.timestamp else ""
        print(f"{ts} | {e.level or '-'} | {e.message[:80]}")


if __name__ == "__main__":
    main()



