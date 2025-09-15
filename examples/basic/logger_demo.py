#!/usr/bin/env python3
"""Example: Advanced logging configuration with SyInfo.

This example demonstrates how to use SyInfo's sophisticated logger
with various configurations including file logging, incident counting,
and different verbosity levels.
"""

import sys
import tempfile
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import syinfo
from syinfo.utils import LoggerConfig


def demo_basic_logging():
    """Demonstrate basic logging functionality."""
    print("🔧 Basic Logging Demo")
    print("=" * 50)
    
    # Get default logger
    logger = syinfo.Logger.get_logger()
    
    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message") 
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    print("✅ Basic logging completed\n")


def demo_configured_logging():
    """Demonstrate advanced logger configuration."""
    print("⚙️ Advanced Configuration Demo")
    print("=" * 50)
    
    # Create temporary log file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
        log_file = f.name
    
    try:
        # Advanced configuration
        config = LoggerConfig(
            log_level=10,  # DEBUG level
            log_files=[log_file],
            truncate_log_files=True,
            output_to_stdout=True,
            verbose_logs=True,  # Include function names and line numbers
            enable_incident_counting=True,  # Number warnings/errors
            enable_traceback=True,  # Include tracebacks
        )
        
        # Get configured logger
        logger = syinfo.Logger.get_logger(config)
        
        # Test logging with configuration
        logger.debug("Debug message with verbose logging")
        logger.info("Info message with configuration")
        logger.warning("First warning - should be numbered")
        logger.warning("Second warning - should be numbered")
        
        # Test error with traceback
        try:
            raise ValueError("Demo error for traceback")
        except ValueError:
            logger.error("Error with traceback demonstration")
        
        # Show log file contents
        log_content = Path(log_file).read_text()
        print(f"\n📄 Log file contents ({log_file}):")
        print("-" * 40)
        print(log_content)
        print("-" * 40)
        
    finally:
        # Cleanup
        Path(log_file).unlink(missing_ok=True)
    
    print("✅ Advanced logging completed\n")


def demo_logger_stats():
    """Demonstrate logger statistics and management."""
    print("📊 Logger Statistics Demo")
    print("=" * 50)
    
    # Get logger instance for advanced operations
    logger_instance = syinfo.Logger.get_instance()
    
    if logger_instance:
        # Show initial stats
        stats = logger_instance.get_stats()
        print("Initial stats:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Generate some incidents
        logger = syinfo.Logger.get_logger()
        logger.warning("Test warning 1")
        logger.warning("Test warning 2") 
        logger.error("Test error 1")
        
        # Show updated stats
        stats = logger_instance.get_stats()
        print("\nUpdated stats after incidents:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Reset counters
        logger_instance.reset_incident_counters()
        stats = logger_instance.get_stats()
        print("\nStats after reset:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    print("✅ Statistics demo completed\n")


def demo_syinfo_with_logging():
    """Demonstrate SyInfo functionality with logging enabled."""
    print("🖥️ SyInfo with Logging Demo")
    print("=" * 50)
    
    # Configure logger to show debug info
    config = LoggerConfig(
        log_level=10,  # DEBUG
        output_to_stdout=True,
        verbose_logs=False,  # Keep it clean
        enable_incident_counting=False,  # No numbering for this demo
    )
    
    logger = syinfo.Logger.get_logger(config)
    
    # Use SyInfo functionality - this will generate log messages
    logger.info("Starting system information collection...")
    
    try:
        # Get basic system info (will generate debug logs internally)
        system_info = syinfo.get_system_info()
        logger.info(f"Collected system info: {system_info.get('system_name', 'Unknown')}")
        
        # Get hardware info
        hardware = syinfo.get_hardware_info()  
        logger.info(f"CPU cores: {hardware.get('cpu', {}).get('cores', 'Unknown')}")
        
    except Exception as e:
        logger.error(f"Error during system info collection: {e}")
    
    logger.info("System information collection completed")
    print("✅ SyInfo with logging completed\n")


if __name__ == "__main__":
    print("🚀 SyInfo Logger Demonstration")
    print("=" * 60)
    print()
    
    try:
        demo_basic_logging()
        demo_configured_logging() 
        demo_logger_stats()
        demo_syinfo_with_logging()
        
        print("🎉 All logger demonstrations completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
