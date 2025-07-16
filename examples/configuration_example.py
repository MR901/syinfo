#!/usr/bin/env python3
"""
Configuration Examples

This example demonstrates how to configure and customize SyInfo
monitoring settings using configuration files and programmatic configuration.
"""

import sys
import yaml
import json
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from syinfo.monitoring.utils import MonitoringConfig
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False
    print("Warning: Monitoring features not available. Install required dependencies.")


def create_basic_config():
    """Create a basic monitoring configuration."""
    config = {
        'monitoring': {
            'system': {
                'enabled': True,
                'interval': 60,  # seconds
                'metrics': [
                    'cpu_usage',
                    'memory_usage',
                    'disk_usage',
                    'network_io'
                ]
            },
            'process': {
                'enabled': True,
                'interval': 60,  # seconds
                'top_processes': 10,
                'filter_pattern': None
            },
            'logs': {
                'enabled': False,  # Disabled for security
                'sources': [
                    '/var/log/syslog',
                    '/var/log/auth.log'
                ],
                'max_lines': 1000
            },
            'storage': {
                'data_directory': '/tmp/syinfo/monitoring',
                'retention_days': 7,
                'format': 'csv',
                'compression': False,
                'max_file_size': '100MB'
            },
            'logging': {
                'level': 'INFO',
                'file': '/tmp/syinfo/monitoring.log',
                'max_size': '10MB',
                'backup_count': 5,
                'console_output': True
            },
            'alerts': {
                'enabled': False,
                'thresholds': {
                    'cpu_percent': 80,
                    'memory_percent': 80,
                    'disk_percent': 90
                }
            },
            'performance': {
                'max_memory_usage': '512MB',
                'max_cpu_percent': 10,
                'timeout_seconds': 30
            },
            'security': {
                'allowed_directories': [
                    '/var/log',
                    '/tmp',
                    '/home'
                ],
                'restricted_commands': [],
                'require_sudo': False
            }
        }
    }
    
    return config


def create_advanced_config():
    """Create an advanced monitoring configuration."""
    config = {
        'monitoring': {
            'system': {
                'enabled': True,
                'interval': 30,  # More frequent monitoring
                'metrics': [
                    'cpu_usage',
                    'memory_usage',
                    'disk_usage',
                    'network_io',
                    'load_average',
                    'temperature'
                ],
                'cpu': {
                    'per_core_monitoring': True,
                    'frequency_monitoring': True
                },
                'memory': {
                    'swap_monitoring': True,
                    'detailed_memory_info': True
                },
                'disk': {
                    'io_monitoring': True,
                    'smart_monitoring': False
                }
            },
            'process': {
                'enabled': True,
                'interval': 30,
                'top_processes': 20,
                'filter_pattern': 'python|java|node',
                'detailed_process_info': True,
                'process_tree': True,
                'io_monitoring': True
            },
            'logs': {
                'enabled': True,
                'sources': [
                    '/var/log/syslog',
                    '/var/log/auth.log',
                    '/var/log/kern.log'
                ],
                'max_lines': 5000,
                'real_time_monitoring': True,
                'pattern_matching': True,
                'alert_on_errors': True
            },
            'storage': {
                'data_directory': '/var/log/syinfo/monitoring',
                'retention_days': 30,
                'format': 'json',
                'compression': True,
                'max_file_size': '500MB',
                'backup_enabled': True,
                'backup_retention': 90
            },
            'logging': {
                'level': 'DEBUG',
                'file': '/var/log/syinfo/monitoring.log',
                'max_size': '50MB',
                'backup_count': 10,
                'console_output': True,
                'syslog_output': True
            },
            'alerts': {
                'enabled': True,
                'thresholds': {
                    'cpu_percent': 70,
                    'memory_percent': 75,
                    'disk_percent': 85,
                    'load_average': 2.0
                },
                'email': {
                    'enabled': False,
                    'smtp_server': 'localhost',
                    'smtp_port': 587,
                    'username': '',
                    'password': '',
                    'recipients': []
                },
                'webhook': {
                    'enabled': False,
                    'url': '',
                    'headers': {}
                }
            },
            'performance': {
                'max_memory_usage': '1GB',
                'max_cpu_percent': 5,
                'timeout_seconds': 60,
                'thread_pool_size': 4
            },
            'security': {
                'allowed_directories': [
                    '/var/log',
                    '/tmp',
                    '/home',
                    '/proc'
                ],
                'restricted_commands': [
                    'rm',
                    'dd',
                    'mkfs'
                ],
                'require_sudo': False,
                'encrypt_data': False
            },
            'scheduling': {
                'cron_enabled': True,
                'cron_expression': '*/5 * * * *',  # Every 5 minutes
                'auto_restart': True,
                'restart_on_failure': True
            }
        }
    }
    
    return config


def create_custom_config():
    """Create a custom configuration for specific use cases."""
    config = {
        'monitoring': {
            'system': {
                'enabled': True,
                'interval': 120,  # 2 minutes
                'metrics': ['cpu_usage', 'memory_usage', 'disk_usage']
            },
            'process': {
                'enabled': True,
                'interval': 300,  # 5 minutes
                'top_processes': 5,
                'filter_pattern': 'nginx|apache|mysql'
            },
            'storage': {
                'data_directory': './monitoring_data',
                'retention_days': 3,
                'format': 'csv'
            },
            'logging': {
                'level': 'WARNING',
                'console_output': True
            }
        }
    }
    
    return config


def save_config_file(config, filename):
    """Save configuration to a YAML file."""
    config_path = Path(__file__).parent / filename
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)
    
    print(f"Configuration saved to: {config_path}")
    return config_path


def load_config_file(config_path):
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print(f"Configuration loaded from: {config_path}")
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None


def programmatic_config_example():
    """Demonstrate programmatic configuration."""
    print("=" * 60)
    print("SyInfo - Programmatic Configuration Example")
    print("=" * 60)
    
    if not MONITORING_AVAILABLE:
        print("Monitoring features not available. Skipping programmatic config example.")
        return
    
    # Create configuration programmatically
    config = MonitoringConfig()
    
    # Set system monitoring settings
    config.set('monitoring.system.enabled', True)
    config.set('monitoring.system.interval', 45)
    config.set('monitoring.system.metrics', ['cpu_usage', 'memory_usage'])
    
    # Set process monitoring settings
    config.set('monitoring.process.enabled', True)
    config.set('monitoring.process.interval', 60)
    config.set('monitoring.process.top_processes', 15)
    
    # Set storage settings
    config.set('monitoring.storage.data_directory', './custom_monitoring')
    config.set('monitoring.storage.retention_days', 5)
    config.set('monitoring.storage.format', 'json')
    
    # Set logging settings
    config.set('monitoring.logging.level', 'INFO')
    config.set('monitoring.logging.console_output', True)
    
    # Get configuration values
    print("Programmatic Configuration:")
    print(f"  System Interval: {config.get('monitoring.system.interval')}")
    print(f"  Process Interval: {config.get('monitoring.process.interval')}")
    print(f"  Data Directory: {config.get('monitoring.storage.data_directory')}")
    print(f"  Log Level: {config.get('monitoring.logging.level')}")
    
    # Save configuration to file
    config.save('./custom_config.yaml')
    print("Configuration saved to: ./custom_config.yaml")


def configuration_comparison():
    """Compare different configuration types."""
    print("\n" + "=" * 60)
    print("Configuration Comparison")
    print("=" * 60)
    
    # Create different configurations
    basic_config = create_basic_config()
    advanced_config = create_advanced_config()
    custom_config = create_custom_config()
    
    # Save configurations
    basic_path = save_config_file(basic_config, 'basic_config.yaml')
    advanced_path = save_config_file(advanced_config, 'advanced_config.yaml')
    custom_path = save_config_file(custom_config, 'custom_config.yaml')
    
    # Compare configurations
    print("\nConfiguration Comparison:")
    print("-" * 30)
    
    print("Basic Configuration:")
    print(f"  System Interval: {basic_config['monitoring']['system']['interval']}s")
    print(f"  Process Top N: {basic_config['monitoring']['process']['top_processes']}")
    print(f"  Retention Days: {basic_config['monitoring']['storage']['retention_days']}")
    
    print("\nAdvanced Configuration:")
    print(f"  System Interval: {advanced_config['monitoring']['system']['interval']}s")
    print(f"  Process Top N: {advanced_config['monitoring']['process']['top_processes']}")
    print(f"  Retention Days: {advanced_config['monitoring']['storage']['retention_days']}")
    print(f"  Alerts Enabled: {advanced_config['monitoring']['alerts']['enabled']}")
    
    print("\nCustom Configuration:")
    print(f"  System Interval: {custom_config['monitoring']['system']['interval']}s")
    print(f"  Process Top N: {custom_config['monitoring']['process']['top_processes']}")
    print(f"  Retention Days: {custom_config['monitoring']['storage']['retention_days']}")


def main():
    """Run all configuration examples."""
    # Create and save configuration files
    configuration_comparison()
    
    # Demonstrate programmatic configuration
    programmatic_config_example()
    
    print("\n" + "=" * 60)
    print("Configuration examples completed!")
    print("=" * 60)
    print("\nGenerated configuration files:")
    print("  - examples/basic_config.yaml")
    print("  - examples/advanced_config.yaml")
    print("  - examples/custom_config.yaml")
    print("  - examples/custom_config.yaml (programmatic)")


if __name__ == "__main__":
    main() 