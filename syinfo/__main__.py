"""SyInfo CLI - Simplified Main Entry Point

Simple command-line interface for system information gathering.
"""

import argparse
import sys
from typing import List

from syinfo._version import __version__
from syinfo.cli import handle_export_command, handle_info_command, show_help
from syinfo.exceptions import SyInfoException


def main(args: List[str] = None) -> int:
    """Main CLI entry point.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, 1 for error)
    """
    if args is None:
        args = sys.argv[1:]

    # If no arguments, show help
    if not args:
        show_help()
        return 0

    parser = argparse.ArgumentParser(
        prog="syinfo", description="SyInfo - System Information Library", add_help=False,
    )

    parser.add_argument(
        "--version", "-V", action="version", version=f"SyInfo {__version__}",
    )

    parser.add_argument(
        "--help", "-h", action="store_true", help="Show help information",
    )

    parser.add_argument("--json", action="store_true", help="Output as JSON")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Info command
    info_parser = subparsers.add_parser("info", help="Show system information")
    info_parser.add_argument(
        "type",
        choices=["system", "device", "network", "brief"],
        help="Type of information to show",
    )

    # Export command
    export_parser = subparsers.add_parser("export", help="Export system information")
    export_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "yaml", "csv"],
        default="json",
        help="Export format (default: json)",
    )
    export_parser.add_argument("--output", "-o", help="Output file path")

    try:
        # Parse arguments
        parsed_args = parser.parse_args(args)

        # Handle help
        if parsed_args.help or (not parsed_args.command):
            show_help()
            return 0

        # Handle commands
        if parsed_args.command == "info":
            result = handle_info_command(parsed_args.type, output_json=parsed_args.json)
            return 0 if result["success"] else 1

        elif parsed_args.command == "export":
            result = handle_export_command(parsed_args.format, parsed_args.output)
            return 0 if result["success"] else 1

        else:
            print(f"Unknown command: {parsed_args.command}")
            show_help()
            return 1

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
