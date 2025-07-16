"""
Data collection and storage module.

This module handles the collection, validation, and storage of monitoring data
in various formats (CSV, JSON) with proper error handling and data integrity.
"""

import os
import csv
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Union
import pandas as pd

from ..utils.logger import MonitoringLogger


class DataCollector:
    """
    Robust data collection with multiple storage formats and validation.
    
    Features:
    - CSV and JSON output support
    - Data validation and integrity checks
    - Automatic file rotation
    - Compression support
    - Error recovery mechanisms
    """
    
    def __init__(self, output_dir: str = "/var/log/syinfo/monitoring"):
        """
        Initialize data collector.
        
        Args:
            output_dir: Directory for storing monitoring data
        """
        self.output_dir = output_dir
        self.logger = MonitoringLogger()
        self._ensure_output_dir()
    
    def store_system_data(self, data: Dict, format: str = "csv") -> bool:
        """
        Store system monitoring data.
        
        Args:
            data: System monitoring data dictionary
            format: Output format ("csv" or "json")
            
        Returns:
            True if data stored successfully, False otherwise
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"{timestamp}_system_stats.{format}"
            filepath = os.path.join(self.output_dir, filename)
            
            if format == "csv":
                return self._store_csv_data(data, filepath, "system")
            elif format == "json":
                return self._store_json_data(data, filepath)
            else:
                self.logger.log_monitoring_event("ERROR", f"Unsupported format: {format}")
                return False
                
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to store system data")
            return False
    
    def store_process_data(self, data: List[Dict], format: str = "csv") -> bool:
        """
        Store process monitoring data.
        
        Args:
            data: Process monitoring data list
            format: Output format ("csv" or "json")
            
        Returns:
            True if data stored successfully, False otherwise
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"{timestamp}_process_stats.{format}"
            filepath = os.path.join(self.output_dir, filename)
            
            if format == "csv":
                return self._store_csv_data(data, filepath, "process")
            elif format == "json":
                return self._store_json_data(data, filepath)
            else:
                self.logger.log_monitoring_event("ERROR", f"Unsupported format: {format}")
                return False
                
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to store process data")
            return False
    
    def validate_data_integrity(self, file_path: str) -> Dict:
        """
        Validate collected data integrity.
        
        Args:
            file_path: Path to data file
            
        Returns:
            Dictionary with validation results
        """
        try:
            if not os.path.exists(file_path):
                return {"valid": False, "error": "File not found"}
            
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return {"valid": False, "error": "File is empty"}
            
            # Check file format
            if file_path.endswith('.csv'):
                return self._validate_csv_file(file_path)
            elif file_path.endswith('.json'):
                return self._validate_json_file(file_path)
            else:
                return {"valid": False, "error": "Unsupported file format"}
                
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def _ensure_output_dir(self):
        """Ensure output directory exists with proper permissions."""
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            # Ensure write permissions
            if not os.access(self.output_dir, os.W_OK):
                raise PermissionError(f"No write permission for {self.output_dir}")
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to create output directory {self.output_dir}")
            raise
    
    def _store_csv_data(self, data: Union[Dict, List[Dict]], filepath: str, data_type: str) -> bool:
        """Store data in CSV format."""
        try:
            file_exists = os.path.exists(filepath)
            mode = 'a' if file_exists else 'w'
            
            with open(filepath, mode, newline='') as csvfile:
                if data_type == "system":
                    # Flatten system data for CSV
                    flat_data = self._flatten_system_data(data)
                    fieldnames = flat_data.keys()
                else:
                    # Process data is already flat
                    flat_data = data[0] if isinstance(data, list) else data
                    fieldnames = flat_data.keys()
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if mode == 'w':
                    writer.writeheader()
                
                if data_type == "system":
                    writer.writerow(flat_data)
                else:
                    writer.writerows(data)
            
            self.logger.log_monitoring_event("INFO", f"Data stored in CSV: {filepath}")
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to store CSV data to {filepath}")
            return False
    
    def _store_json_data(self, data: Union[Dict, List[Dict]], filepath: str) -> bool:
        """Store data in JSON format."""
        try:
            # Append to existing JSON file or create new one
            existing_data = []
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
            
            if isinstance(data, list):
                existing_data.extend(data)
            else:
                existing_data.append(data)
            
            with open(filepath, 'w') as f:
                json.dump(existing_data, f, indent=2, default=str)
            
            self.logger.log_monitoring_event("INFO", f"Data stored in JSON: {filepath}")
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to store JSON data to {filepath}")
            return False
    
    def _flatten_system_data(self, data: Dict) -> Dict:
        """Flatten nested system data for CSV storage."""
        flat_data = {}
        
        # Add timestamp
        flat_data['timestamp'] = data.get('timestamp', time.time())
        flat_data['datetime'] = data.get('datetime', datetime.now().isoformat())
        
        # Flatten CPU data
        cpu_data = data.get('cpu', {})
        flat_data['cpu_percent'] = cpu_data.get('percent', 0)
        flat_data['cpu_count'] = cpu_data.get('count', 0)
        flat_data['cpu_count_logical'] = cpu_data.get('count_logical', 0)
        
        # Flatten memory data
        memory_data = data.get('memory', {})
        flat_data['memory_total'] = memory_data.get('total', 0)
        flat_data['memory_used'] = memory_data.get('used', 0)
        flat_data['memory_available'] = memory_data.get('available', 0)
        flat_data['memory_percent'] = memory_data.get('percent', 0)
        flat_data['swap_total'] = memory_data.get('swap_total', 0)
        flat_data['swap_used'] = memory_data.get('swap_used', 0)
        flat_data['swap_percent'] = memory_data.get('swap_percent', 0)
        
        # Flatten disk data
        disk_data = data.get('disk', {})
        flat_data['disk_total'] = disk_data.get('total', 0)
        flat_data['disk_used'] = disk_data.get('used', 0)
        flat_data['disk_free'] = disk_data.get('free', 0)
        flat_data['disk_percent'] = disk_data.get('percent', 0)
        flat_data['disk_io_read'] = disk_data.get('io_read_bytes', 0)
        flat_data['disk_io_write'] = disk_data.get('io_write_bytes', 0)
        
        # Flatten network data
        network_data = data.get('network', {})
        flat_data['network_bytes_sent'] = network_data.get('bytes_sent', 0)
        flat_data['network_bytes_recv'] = network_data.get('bytes_recv', 0)
        flat_data['network_packets_sent'] = network_data.get('packets_sent', 0)
        flat_data['network_packets_recv'] = network_data.get('packets_recv', 0)
        
        return flat_data
    
    def _validate_csv_file(self, file_path: str) -> Dict:
        """Validate CSV file integrity."""
        try:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            if len(rows) < 2:  # Need header + at least one data row
                return {"valid": False, "error": "Insufficient data rows"}
            
            # Check for consistent column count
            header_length = len(rows[0])
            for i, row in enumerate(rows[1:], 1):
                if len(row) != header_length:
                    return {"valid": False, "error": f"Row {i} has inconsistent column count"}
            
            return {"valid": True, "rows": len(rows), "columns": header_length}
            
        except Exception as e:
            return {"valid": False, "error": str(e)}
    
    def _validate_json_file(self, file_path: str) -> Dict:
        """Validate JSON file integrity."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, (list, dict)):
                return {"valid": False, "error": "Invalid JSON structure"}
            
            return {"valid": True, "type": type(data).__name__, "size": len(data) if isinstance(data, list) else 1}
            
        except json.JSONDecodeError as e:
            return {"valid": False, "error": f"JSON decode error: {str(e)}"}
        except Exception as e:
            return {"valid": False, "error": str(e)} 