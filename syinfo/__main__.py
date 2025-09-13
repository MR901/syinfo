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
from syinfo.core.sys_info import SysInfo
from syinfo.simple_monitoring import SimpleMonitor
from syinfo.exceptions import SyInfoException


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
        monitor = SimpleMonitor(interval=args.interval)
        
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
                if hasattr(info, 'get') and info.get('network_devices') == 'NEED_SUDO':
                    if not args.disable_print:
                        print("\033[1m\033[31mPlease run search_devices_on_network() with sudo access!\033[0m")
                    # Continue with available info (without network devices)
                    
            except ImportError:
                if not args.disable_print:
                    print("Error: Network features not available. Install with: pip install syinfo[network]")
                return 1
                
        elif args.system:
            try:
                instance = SysInfo
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