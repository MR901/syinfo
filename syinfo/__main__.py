"""SyInfo CLI - Powerful Flag-Based Interface

Restored the original powerful CLI with flag-based commands for easy scripting and JSON processing.
"""

import argparse
import json
import sys
import textwrap
import time
import warnings
from typing import Optional

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

from syinfo._version import __version__
from syinfo.core.device_info import DeviceInfo
from syinfo.core.network_info import NetworkInfo  
from syinfo.core.system_info import SystemInfo
from syinfo.resource_monitor.system_monitor import SystemMonitor
from syinfo.exceptions import SyInfoException
from syinfo.analysis.logs import LogAnalyzer, LogAnalysisConfig
from syinfo.analysis.system import SystemAnalyzer
from syinfo.analysis.packages import PackageManager, PackageManagerType


def contact(msg: bool = True) -> str:
    """Contact links."""
    _msg = "\n  --  Email: \033[4m\033[94mmohitrajput901@gmail.com\033[0m"
    _msg += "\n  -- GitHub: \033[4m\033[94mhttps://github.com/MR901/syinfo\033[0m"
    if msg:
        print(_msg)
    return _msg


def _handle_monitoring(args) -> int:
    """Handle monitoring mode with -m flag.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        if not args.disable_print:
            print(f"\033[95mStarting system monitoring...\033[0m")
            print(f"Interval: {args.interval} seconds")
            print(f"Duration: {args.time} seconds")
            print(f"Press Ctrl+C to stop early\n")
        
        # Create monitor
        monitor = SystemMonitor(interval=args.interval)
        
        # Start monitoring
        monitor.start(duration=args.time)
        
        # Wait for monitoring to complete (with user interrupt handling)
        try:
            time.sleep(args.time + 1)  # Wait a bit longer than monitoring duration
            
            # Get results (monitor may have stopped automatically)
            if monitor.is_running:
                results = monitor.stop()
            else:
                # Monitoring completed automatically, get the data that was collected
                results = {
                    "total_points": len(monitor.data_points),
                    "data_points": monitor.data_points,
                    "summary": monitor._calculate_summary() if monitor.data_points else {}
                }
                
        except KeyboardInterrupt:
            if not args.disable_print:
                print("\n\033[93mMonitoring stopped by user\033[0m")
            # Try to get partial results
            results = monitor.stop() if monitor.is_running else {"error": "Monitoring interrupted", "data_points": monitor.data_points}
        
        # Handle output based on flags
        if not args.disable_print:
            if 'summary' in results and results['summary']:
                _print_monitoring_summary(results['summary'])
            else:
                print(f"Monitoring completed. Collected {results.get('total_points', 0)} data points.")
                
        # Print JSON output if requested
        if args.return_json:
            print(json.dumps(results, default=str, indent=None))
        
        return 0
        
    except Exception as e:
        print(f"Monitoring error: {e}")
        return 1


def _print_monitoring_summary(summary: dict) -> None:
    """Print monitoring summary in a nice format."""
    print(f"\033[95m{'━' * 60}\033[0m")
    print(f"\033[95m{'System Monitoring Summary':^60}\033[0m")  
    print(f"\033[95m{'━' * 60}\033[0m")
    
    print(f"Duration: {summary.get('duration_seconds', 0)} seconds")
    print(f"Start Time: {summary.get('start_time', 'N/A')}")
    print(f"End Time: {summary.get('end_time', 'N/A')}")
    print()
    
    print("Performance Metrics:")
    print(f"  CPU Usage     - Avg: {summary.get('cpu_avg', 0):.1f}%  Max: {summary.get('cpu_max', 0):.1f}%")
    print(f"  Memory Usage  - Avg: {summary.get('memory_avg', 0):.1f}%  Peak: {summary.get('memory_peak', 0):.1f}%")
    print(f"  Disk Usage    - Avg: {summary.get('disk_avg', 0):.1f}%")
    
    print(f"\033[95m{'━' * 60}\033[0m")


def main() -> int:
    """Main CLI entry point with flag-based interface.
    
    Returns:
        Exit code (0 for success, 1 for error, 130 for interrupted)
    """
    wrapper = textwrap.TextWrapper(width=50)
    description = wrapper.fill(text="SyInfo - System Information Library")

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=description,
        epilog=textwrap.dedent(contact(msg=False))
    )

    # Contact and version
    parser.add_argument(
        "-c", "--contact", 
        action="store_true", 
        help="show contact information"
    )
    parser.add_argument(
        "-v", "--version", 
        action="version", 
        version=__version__, 
        help="show current version"
    )
    
    # Information type flags
    parser.add_argument(
        "-d", "--device", 
        action="store_true",
        help="\033[93m" + "show information about your device." + "\033[0m"
    )
    parser.add_argument(
        "-n", "--network", 
        action="store_true",
        help="\033[94m" + "show information about your network." + "\033[0m"
    )
    parser.add_argument(
        "-s", "--system", 
        action="store_true",
        help="\033[92m" + "show combined information about your device and network." + "\033[0m"
    )
    parser.add_argument(
        "-m", "--monitor", 
        action="store_true",
        help="\033[95m" + "start system monitoring." + "\033[0m"
    )
    parser.add_argument(
        "-l", "--logs",
        action="store_true",
        help="\033[96m" + "query system logs (use --text/--level/--process/--regex)." + "\033[0m"
    )
    parser.add_argument(
        "-P", "--packages",
        action="store_true",
        help="\033[96m" + "list installed packages (use --manager/--name)." + "\033[0m"
    )
    parser.add_argument(
        "-H", "--health",
        action="store_true",
        help="\033[96m" + "show quick system health report (last 24h)." + "\033[0m"
    )
    parser.add_argument(
        "-S", "--search",
        type=str,
        metavar="",
        required=False,
        help="cross-surface search term (logs + packages)"
    )
    
    # Network scanning and monitoring time options
    parser.add_argument(
        "-t", "--time", 
        type=int, 
        metavar="", 
        required=False, 
        default=10,
        help="int supplement for `-n` or `-s` command (scanning `-t` seconds) or `-m` (monitoring duration)"
    )
    parser.add_argument(
        "-i", "--interval", 
        type=int, 
        metavar="", 
        required=False, 
        default=5,
        help="int supplement for `-m` command (monitoring interval in seconds, default: 5)"
    )
    parser.add_argument(
        "-o", "--disable-vendor-search", 
        action="store_false",
        help="supplement for `-n` or `-s` command to stop searching for vendor for the device (mac)"
    )

    # Log query options
    parser.add_argument("--text", type=str, metavar="", required=False, default="", help="text filter for logs")
    parser.add_argument("--level", type=str, metavar="", required=False, default="", help="comma-separated log levels (e.g., ERROR,WARNING)")
    parser.add_argument("--process", type=str, metavar="", required=False, default="", help="process name filter for logs")
    parser.add_argument("--hours", type=int, metavar="", required=False, default=24, help="hours back for log time range (default: 24)")
    parser.add_argument("--limit", type=int, metavar="", required=False, default=100, help="maximum log entries to return")
    parser.add_argument("--regex", type=str, metavar="", required=False, default="", help="regular expression pattern for logs")
    # Package query options
    parser.add_argument("--manager", type=str, metavar="", required=False, default="", help="package manager (apt|yum|dnf|pip|conda|npm|snap)")
    parser.add_argument("--name", type=str, metavar="", required=False, default="", help="package name filter substring")

    # Output control flags
    parser.add_argument(
        "-p", "--disable-print", 
        action="store_true", 
        help="disable printing of the information."
    )
    parser.add_argument(
        "-j", "--return-json", 
        action="store_true", 
        help="return output as json"
    )

    try:
        args = parser.parse_args()
        
        # Handle contact
        if args.contact:
            contact(msg=True)
            return 0
            
        # Handle no arguments
        if len(sys.argv) == 1:
            parser.print_help()
            return 0

        # Determine what information to gather
        instance = None
        info = None
        
        if args.device:
            instance = DeviceInfo
            info = instance.get_all()
            
        elif args.network:
            try:
                instance = NetworkInfo
                info = instance.get_all(
                    search_period=args.time,
                    search_device_vendor_too=args.disable_vendor_search
                )
                
                # Check if network scan failed due to sudo requirements
                if hasattr(info, "get") and (
                    info.get("network_devices") == "NEED_SUDO" or
                    (isinstance(info.get("network_info", {}), dict) and info["network_info"].get("devices_on_network") == "NEED_SUDO")
                ):
                    if not args.disable_print:
                        print("\033[1m\033[31mPlease run search_devices_on_network() with sudo access!\033[0m")
                    # Continue with available info (without network devices)
                    
            except ImportError:
                if not args.disable_print:
                    print("Error: Network features not available. Install with: pip install syinfo[network]")
                return 1
                
        elif args.system:
            try:
                instance = SystemInfo
                info = instance.get_all(
                    search_period=args.time,
                    search_device_vendor_too=args.disable_vendor_search
                )
            except ImportError:
                if not args.disable_print:
                    print("Error: Network features not available. Install with: pip install syinfo[network]")
                    # Fall back to device info only
                    print("Falling back to device information only...")
                instance = DeviceInfo
                info = instance.get_all()
                
        elif args.monitor:
            # Handle monitoring mode
            return _handle_monitoring(args)
        elif args.logs:
            # Log query handler
            analyzer = LogAnalyzer(LogAnalysisConfig())
            levels = None
            if args.level:
                levels = [lvl.strip().upper() for lvl in args.level.split(",") if lvl.strip()]
            start_time = None
            end_time = None
            if args.hours and args.hours > 0:
                from datetime import datetime, timedelta

                end_time = datetime.now()
                start_time = end_time - timedelta(hours=args.hours)
            entries = analyzer.query_logs(
                text_filter=args.text or "",
                level_filter=levels,
                time_range=(start_time, end_time) if start_time and end_time else None,
                process_filter=args.process or "",
                regex_pattern=args.regex or None,
                limit=args.limit or 100,
            )
            # Output
            if args.return_json:
                print(
                    json.dumps(
                        [
                            {
                                "timestamp": e.timestamp,
                                "level": e.level,
                                "process": e.process,
                                "message": e.message,
                                "file": e.file_path,
                                "line": e.line_number,
                            }
                            for e in entries
                        ],
                        default=str,
                        indent=None,
                    )
                )
            elif not args.disable_print:
                print(f"Found {len(entries)} log entries")
                for e in entries[: min(10, len(entries))]:
                    ts = e.timestamp.isoformat() if e.timestamp else ""
                    print(f"{ts} | {e.level or '-'} | {e.process or '-'} | {e.message}")
            return 0
        elif args.packages:
            # Package listing handler
            pm = PackageManager()
            selected = None
            if args.manager:
                try:
                    selected = PackageManagerType(args.manager)
                except ValueError:
                    selected = None
            packages = pm.list_packages(manager=selected, name_filter=args.name or "")
            if args.return_json:
                print(
                    json.dumps(
                        [
                            {
                                "name": p.name,
                                "version": p.version,
                                "architecture": p.architecture,
                                "description": p.description,
                                "manager": p.manager,
                            }
                            for p in packages
                        ],
                        indent=None,
                        default=str,
                    )
                )
            elif not args.disable_print:
                print(f"Total installed packages: {len(packages)}")
                # Show by manager summary
                counts = {}
                for p in packages:
                    counts[p.manager] = counts.get(p.manager, 0) + 1
                for mgr, count in sorted(counts.items()):
                    print(f"{mgr}: {count}")
            return 0
        elif args.health:
            sa = SystemAnalyzer()
            report = sa.quick_system_health_check()
            if args.return_json:
                print(json.dumps(report, default=str, indent=None))
            elif not args.disable_print:
                print("=== System Health Report (24h) ===")
                print(f"Platform: {report['system_info']['platform']}")
                print(f"Recent Errors: {len(report.get('recent_errors', []))}")
                print(f"Recent Warnings: {len(report.get('warnings', []))}")
            return 0
        elif args.search:
            sa = SystemAnalyzer()
            result = sa.search_system(args.search, include_logs=True, include_packages=True)
            if args.return_json:
                print(json.dumps(result, default=str, indent=None))
            elif not args.disable_print:
                print(f"Term: {result['search_term']}")
                print(f"Log entries: {len(result.get('log_entries', []))}")
                print(f"Packages: {len(result.get('packages', []))}")
            return 0
                
        else:
            # No valid flag provided
            parser.print_help()
            return 0

        # Handle output
        if instance and info:
            # Print formatted output (unless disabled)
            if not args.disable_print:
                try:
                    instance.print(info)
                except Exception as e:
                    print(f"Error displaying information: {e}")
                    return 1

            # Print JSON output (if requested)
            if args.return_json:
                try:
                    print(json.dumps(info, default=str, indent=None))
                except Exception as e:
                    print(f"Error generating JSON: {e}")
                    return 1

        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 130
        
    except SyInfoException as e:
        print(f"Error: {e}")
        return 1
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())