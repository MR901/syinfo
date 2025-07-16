"""Main file

Enhanced SyInfo CLI with subcommand support for both legacy info mode and new monitoring mode.
"""

import warnings
warnings.filterwarnings("ignore")

import sys
import json
import argparse
import textwrap
import platform
from typing import Dict, Any

from syinfo._version import __version__
from syinfo.cli.utils.formatter import OutputFormatter
from syinfo.cli.utils.validator import CLIValidator


def contact(msg=True):
    """Contact links."""
    if msg:
        print(OutputFormatter.print_contact())
    return OutputFormatter.print_contact()


def handle_info_command(args):
    """Handle info subcommand."""
    try:
        from syinfo.cli.commands.info_commands import InfoCommands
        
        commands = InfoCommands()
        
        if args.device:
            result = commands.handle_device_info(
                disable_print=args.disable_print,
                return_json=args.return_json
            )
        elif args.network:
            result = commands.handle_network_info(
                search_period=args.time,
                search_device_vendor_too=args.disable_vendor_search,
                disable_print=args.disable_print,
                return_json=args.return_json
            )
        elif args.system:
            result = commands.handle_system_info(
                search_period=args.time,
                search_device_vendor_too=args.disable_vendor_search,
                disable_print=args.disable_print,
                return_json=args.return_json
            )
        else:
            print("❌ No info type specified. Use --device, --network, or --system")
            sys.exit(1)
        
        if not result["success"]:
            print(OutputFormatter.error(result["error"]))
            sys.exit(1)
            
    except ImportError as e:
        print(OutputFormatter.error(f"Info features not available: {e}"))
        sys.exit(1)


def handle_monitor_command(args):
    """Handle monitor subcommand."""
    try:
        from syinfo.cli.commands.monitor_commands import MonitorCommands
        
        commands = MonitorCommands()
        
        # Validate arguments
        validation_args = {
            'interval': args.interval,
            'duration': args.duration,
            'output_dir': args.output_dir,
            'config_path': args.config
        }
        valid, errors = CLIValidator.validate_monitoring_args(validation_args)
        if not valid:
            CLIValidator.print_validation_errors(errors)
            sys.exit(1)
        
        if args.start:
            result = commands.start_monitoring(
                config_path=args.config,
                output_dir=args.output_dir,
                interval=args.interval,
                duration=args.duration,
                format=args.format
            )
        elif args.stop:
            result = commands.stop_monitoring()
        elif args.status:
            result = commands.get_status()
        elif args.collect:
            result = commands.collect_data(
                output_dir=args.output_dir,
                format=args.format,
                include_processes=args.include_processes,
                include_logs=args.include_logs
            )
        else:
            print("❌ No monitor action specified. Use --start, --stop, --status, or --collect")
            sys.exit(1)
        
        OutputFormatter.print_result(result, format=args.output_format)
        if not result["success"]:
            sys.exit(1)
            
    except ImportError as e:
        print(OutputFormatter.error(f"Monitoring features not available: {e}"))
        sys.exit(1)


def handle_analyze_command(args):
    """Handle analyze subcommand."""
    try:
        from syinfo.cli.commands.analyze_commands import AnalyzeCommands
        
        commands = AnalyzeCommands()
        
        # Validate arguments
        validation_args = {
            'data_file': args.data_file,
            'output_path': args.output,
            'chart_type': args.chart_type
        }
        valid, errors = CLIValidator.validate_analysis_args(validation_args)
        if not valid:
            CLIValidator.print_validation_errors(errors)
            sys.exit(1)
        
        if args.trends:
            result = commands.analyze_trends(args.data_file)
        elif args.anomalies:
            result = commands.detect_anomalies(args.data_file)
        elif args.report:
            result = commands.generate_report(args.data_file, args.output)
        elif args.dashboard:
            result = commands.create_dashboard(
                args.data_file,
                args.output,
                args.chart_types
            )
        elif args.chart:
            if not args.chart_type:
                print("❌ Chart type is required for --chart option")
                sys.exit(1)
            result = commands.create_chart(
                args.data_file,
                args.chart_type,
                args.output
            )
        else:
            print("❌ No analysis action specified. Use --trends, --anomalies, --report, --dashboard, or --chart")
            sys.exit(1)
        
        OutputFormatter.print_result(result, format=args.output_format)
        if not result["success"]:
            sys.exit(1)
            
    except ImportError as e:
        print(OutputFormatter.error(f"Analysis features not available: {e}"))
        sys.exit(1)


def handle_setup_command(args):
    """Handle setup subcommand."""
    try:
        from syinfo.cli.commands.setup_commands import SetupCommands
        
        commands = SetupCommands()
        
        # Validate arguments
        validation_args = {
            'interval_minutes': args.interval_minutes,
            'config_path': args.config_path,
            'output_path': args.output_path
        }
        valid, errors = CLIValidator.validate_setup_args(validation_args)
        if not valid:
            CLIValidator.print_validation_errors(errors)
            sys.exit(1)
        
        if args.install_cron:
            result = commands.install_cron_jobs(
                interval_minutes=args.interval_minutes,
                config_path=args.config_path
            )
        elif args.remove_cron:
            result = commands.remove_cron_jobs()
        elif args.create_config:
            result = commands.create_config(
                output_path=args.output_path,
                template_type=args.template_type
            )
        elif args.validate_config:
            result = commands.validate_config(args.config_path)
        elif args.setup_dirs:
            result = commands.setup_directories(args.base_path)
        else:
            print("❌ No setup action specified. Use --install-cron, --remove-cron, --create-config, --validate-config, or --setup-dirs")
            sys.exit(1)
        
        OutputFormatter.print_result(result, format=args.output_format)
        if not result["success"]:
            sys.exit(1)
            
    except ImportError as e:
        print(OutputFormatter.error(f"Setup features not available: {e}"))
        sys.exit(1)


def main():
    """Enhanced main function with subcommand support."""
    description = "SyInfo - System Information & Monitoring Tool"
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=description,
        epilog=textwrap.dedent(contact(msg=False))
    )
    
    # Global arguments
    parser.add_argument(
        "-v", "--version", action="version", version=__version__, help="show current version"
    )
    parser.add_argument(
        "-c", "--contact", action="store_true", help="show contact information"
    )
    parser.add_argument(
        "--output-format", choices=['auto', 'json'], default='auto',
        help="output format (default: auto)"
    )
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='available commands')
    
    # Info subcommand (legacy compatibility)
    info_parser = subparsers.add_parser('info', help='system information commands')
    info_parser.add_argument(
        "-d", "--device", action="store_true", help="show device information"
    )
    info_parser.add_argument(
        "-n", "--network", action="store_true", help="show network information"
    )
    info_parser.add_argument(
        "-s", "--system", action="store_true", help="show combined system information"
    )
    info_parser.add_argument(
        "-t", "--time", type=int, default=10, help="scanning period in seconds (default: 10)"
    )
    info_parser.add_argument(
        "-o", "--disable-vendor-search", action="store_false",
        help="disable vendor search for devices"
    )
    info_parser.add_argument(
        "-p", "--disable-print", action="store_true", help="disable printing of information"
    )
    info_parser.add_argument(
        "-j", "--return-json", action="store_true", help="return output as JSON"
    )
    
    # Monitor subcommand
    monitor_parser = subparsers.add_parser('monitor', help='system monitoring commands')
    monitor_parser.add_argument(
        "--start", action="store_true", help="start monitoring"
    )
    monitor_parser.add_argument(
        "--stop", action="store_true", help="stop monitoring"
    )
    monitor_parser.add_argument(
        "--status", action="store_true", help="get monitoring status"
    )
    monitor_parser.add_argument(
        "--collect", action="store_true", help="collect one-time data snapshot"
    )
    monitor_parser.add_argument(
        "--interval", type=int, default=60, help="monitoring interval in seconds (default: 60)"
    )
    monitor_parser.add_argument(
        "--duration", type=int, help="monitoring duration in seconds (default: continuous)"
    )
    monitor_parser.add_argument(
        "--config", help="configuration file path"
    )
    monitor_parser.add_argument(
        "--output-dir", help="output directory for monitoring data"
    )
    monitor_parser.add_argument(
        "--format", choices=['csv', 'json'], default='csv', help="output format"
    )
    monitor_parser.add_argument(
        "--include-processes", action="store_true", default=True, help="include process data"
    )
    monitor_parser.add_argument(
        "--include-logs", action="store_true", help="include log data"
    )
    
    # Analyze subcommand
    analyze_parser = subparsers.add_parser('analyze', help='data analysis commands')
    analyze_parser.add_argument(
        "--data-file", required=True, help="input data file path"
    )
    analyze_parser.add_argument(
        "--trends", action="store_true", help="analyze system trends"
    )
    analyze_parser.add_argument(
        "--anomalies", action="store_true", help="detect anomalies"
    )
    analyze_parser.add_argument(
        "--report", action="store_true", help="generate analysis report"
    )
    analyze_parser.add_argument(
        "--dashboard", action="store_true", help="create visualization dashboard"
    )
    analyze_parser.add_argument(
        "--chart", action="store_true", help="create specific chart"
    )
    analyze_parser.add_argument(
        "--chart-type", help="chart type for --chart option"
    )
    analyze_parser.add_argument(
        "--chart-types", nargs='+', help="chart types for dashboard"
    )
    analyze_parser.add_argument(
        "--output", help="output file path"
    )
    
    # Setup subcommand
    setup_parser = subparsers.add_parser('setup', help='system setup commands')
    setup_parser.add_argument(
        "--install-cron", action="store_true", help="install monitoring cron jobs"
    )
    setup_parser.add_argument(
        "--remove-cron", action="store_true", help="remove monitoring cron jobs"
    )
    setup_parser.add_argument(
        "--create-config", action="store_true", help="create configuration file"
    )
    setup_parser.add_argument(
        "--validate-config", action="store_true", help="validate configuration file"
    )
    setup_parser.add_argument(
        "--setup-dirs", action="store_true", help="setup monitoring directories"
    )
    setup_parser.add_argument(
        "--interval-minutes", type=int, default=1, help="cron interval in minutes (default: 1)"
    )
    setup_parser.add_argument(
        "--config-path", help="configuration file path"
    )
    setup_parser.add_argument(
        "--output-path", default="monitoring_config.yaml", help="output file path"
    )
    setup_parser.add_argument(
        "--template-type", default="default", help="configuration template type"
    )
    setup_parser.add_argument(
        "--base-path", default="./monitoring_data", help="base path for directories"
    )
    
    args = parser.parse_args()
    
    # Handle contact and version
    if args.contact:
        contact(msg=True)
        return
    elif args.version:
        print(__version__)
        return
    
    # Handle subcommands
    if args.command == 'info':
        handle_info_command(args)
    elif args.command == 'monitor':
        handle_monitor_command(args)
    elif args.command == 'analyze':
        handle_analyze_command(args)
    elif args.command == 'setup':
        handle_setup_command(args)
    elif len(sys.argv) == 1:
        # No arguments provided, show help
        parser.print_help()
    else:
        # Invalid command
        print("❌ Invalid command. Use --help for available commands.")
        sys.exit(1)


if __name__ == "__main__":
    main()
