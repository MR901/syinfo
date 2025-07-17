#!/usr/bin/env python3
"""Test runner for SyInfo project."""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_unit_tests(verbose=False, coverage=False):
    """Run unit tests."""
    cmd = [sys.executable, "-m", "pytest", "tests/unit/"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=syinfo", "--cov-report=html", "--cov-report=term"])
    
    print("Running unit tests...")
    result = subprocess.run(cmd)
    return result.returncode


def run_integration_tests(verbose=False):
    """Run integration tests."""
    cmd = [sys.executable, "-m", "pytest", "tests/integration/"]
    
    if verbose:
        cmd.append("-v")
    
    print("Running integration tests...")
    result = subprocess.run(cmd)
    return result.returncode


def run_performance_tests(verbose=False):
    """Run performance tests."""
    cmd = [sys.executable, "-m", "pytest", "tests/performance/"]
    
    if verbose:
        cmd.append("-v")
    
    print("Running performance tests...")
    result = subprocess.run(cmd)
    return result.returncode


def run_all_tests(verbose=False, coverage=False):
    """Run all tests."""
    cmd = [sys.executable, "-m", "pytest", "tests/"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=syinfo", "--cov-report=html", "--cov-report=term"])
    
    print("Running all tests...")
    result = subprocess.run(cmd)
    return result.returncode


def check_test_dependencies():
    """Check if test dependencies are installed."""
    required_packages = ["pytest", "pytest-cov"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing test dependencies: {', '.join(missing_packages)}")
        print("Install with: pip install pytest pytest-cov")
        return False
    
    return True


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="SyInfo Test Runner")
    parser.add_argument(
        "--unit", action="store_true",
        help="Run unit tests only"
    )
    parser.add_argument(
        "--integration", action="store_true",
        help="Run integration tests only"
    )
    parser.add_argument(
        "--performance", action="store_true",
        help="Run performance tests only"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--coverage", action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "--check-deps", action="store_true",
        help="Check test dependencies"
    )
    
    args = parser.parse_args()
    
    # Check dependencies if requested
    if args.check_deps:
        if check_test_dependencies():
            print("All test dependencies are installed.")
            return 0
        else:
            return 1
    
    # Check dependencies before running tests
    if not check_test_dependencies():
        return 1
    
    # Determine which tests to run
    if args.unit:
        return run_unit_tests(args.verbose, args.coverage)
    elif args.integration:
        return run_integration_tests(args.verbose)
    elif args.performance:
        return run_performance_tests(args.verbose)
    else:
        # Run all tests by default
        return run_all_tests(args.verbose, args.coverage)


if __name__ == "__main__":
    sys.exit(main()) 