"""SyInfo Test Suite

Comprehensive test suite for SyInfo system information and monitoring tool.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestConfig:
    """Test configuration and utilities."""
    
    @staticmethod
    def get_test_data_dir():
        """Get test data directory."""
        return Path(__file__).parent / "fixtures" / "sample_data"
    
    @staticmethod
    def get_test_config_dir():
        """Get test config directory."""
        return Path(__file__).parent / "fixtures" / "configs"
    
    @staticmethod
    def create_temp_dir():
        """Create temporary directory for tests."""
        return tempfile.mkdtemp(prefix="syinfo_test_")
    
    @staticmethod
    def cleanup_temp_dir(temp_dir):
        """Clean up temporary directory."""
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    
    @staticmethod
    def create_sample_csv_data():
        """Create sample CSV data for testing."""
        return """timestamp,cpu_percent,memory_percent,disk_percent
2024-01-01 10:00:00,25.5,45.2,60.1
2024-01-01 10:01:00,30.2,47.8,61.3
2024-01-01 10:02:00,28.7,46.1,60.8
2024-01-01 10:03:00,35.1,49.2,62.1
2024-01-01 10:04:00,22.3,44.7,59.9"""
    
    @staticmethod
    def create_sample_json_data():
        """Create sample JSON data for testing."""
        return {
            "system_info": {
                "cpu_percent": 25.5,
                "memory_percent": 45.2,
                "disk_percent": 60.1,
                "timestamp": "2024-01-01 10:00:00"
            },
            "processes": [
                {
                    "pid": 1234,
                    "name": "python",
                    "cpu_percent": 5.2,
                    "memory_percent": 2.1
                }
            ]
        } 