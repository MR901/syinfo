"""
Data analysis module for monitoring data.

This module provides comprehensive analysis capabilities including:
- Time series analysis
- Anomaly detection
- Performance trend analysis
- Statistical calculations
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt

from ..utils.logger import MonitoringLogger


class DataAnalyzer:
    """
    Advanced data analysis with trend detection and anomaly identification.
    
    Features:
    - Time series analysis
    - Anomaly detection
    - Performance trend analysis
    - Statistical calculations
    - Data aggregation and filtering
    """
    
    def __init__(self):
        """Initialize data analyzer."""
        self.logger = MonitoringLogger()
    
    def analyze_system_trends(self, data_file: str, time_range: Optional[str] = None) -> Dict:
        """
        Analyze system performance trends over time.
        
        Args:
            data_file: Path to monitoring data file
            time_range: Time range filter (e.g., "1h", "24h", "7d")
            
        Returns:
            Dictionary with trend analysis results
        """
        try:
            if not os.path.exists(data_file):
                return {"error": f"Data file not found: {data_file}"}
            
            # Load data
            df = self._load_data(data_file)
            if df is None or df.empty:
                return {"error": "No data available for analysis"}
            
            # Apply time filter if specified
            if time_range:
                df = self._filter_by_time_range(df, time_range)
            
            # Calculate trends
            trends = {
                "cpu_trend": self._calculate_trend(df, 'cpu_percent'),
                "memory_trend": self._calculate_trend(df, 'memory_percent'),
                "disk_trend": self._calculate_trend(df, 'disk_percent'),
                "network_trend": self._calculate_network_trend(df),
                "summary_stats": self._calculate_summary_stats(df)
            }
            
            return trends
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to analyze trends for {data_file}")
            return {"error": str(e)}
    
    def detect_anomalies(self, data_file: str, threshold: float = 2.0) -> Dict:
        """
        Detect performance anomalies in monitoring data.
        
        Args:
            data_file: Path to monitoring data file
            threshold: Standard deviation threshold for anomaly detection
            
        Returns:
            Dictionary with anomaly detection results
        """
        try:
            if not os.path.exists(data_file):
                return {"error": f"Data file not found: {data_file}"}
            
            # Load data
            df = self._load_data(data_file)
            if df is None or df.empty:
                return {"error": "No data available for analysis"}
            
            anomalies = {
                "cpu_anomalies": self._detect_column_anomalies(df, 'cpu_percent', threshold),
                "memory_anomalies": self._detect_column_anomalies(df, 'memory_percent', threshold),
                "disk_anomalies": self._detect_column_anomalies(df, 'disk_percent', threshold),
                "network_anomalies": self._detect_network_anomalies(df, threshold)
            }
            
            return anomalies
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to detect anomalies in {data_file}")
            return {"error": str(e)}
    
    def calculate_performance_metrics(self, data_file: str) -> Dict:
        """
        Calculate comprehensive performance metrics.
        
        Args:
            data_file: Path to monitoring data file
            
        Returns:
            Dictionary with performance metrics
        """
        try:
            if not os.path.exists(data_file):
                return {"error": f"Data file not found: {data_file}"}
            
            # Load data
            df = self._load_data(data_file)
            if df is None or df.empty:
                return {"error": "No data available for analysis"}
            
            metrics = {
                "cpu_metrics": self._calculate_cpu_metrics(df),
                "memory_metrics": self._calculate_memory_metrics(df),
                "disk_metrics": self._calculate_disk_metrics(df),
                "network_metrics": self._calculate_network_metrics(df),
                "overall_performance_score": self._calculate_performance_score(df)
            }
            
            return metrics
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to calculate metrics for {data_file}")
            return {"error": str(e)}
    
    def _load_data(self, data_file: str) -> Optional[pd.DataFrame]:
        """Load data from file based on format."""
        try:
            if data_file.endswith('.csv'):
                df = pd.read_csv(data_file)
            elif data_file.endswith('.json'):
                with open(data_file, 'r') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
            else:
                self.logger.log_monitoring_event("ERROR", f"Unsupported file format: {data_file}")
                return None
            
            # Convert timestamp to datetime if present
            if 'timestamp' in df.columns:
                df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            elif 'datetime' in df.columns:
                df['datetime'] = pd.to_datetime(df['datetime'])
            
            return df
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to load data from {data_file}")
            return None
    
    def _filter_by_time_range(self, df: pd.DataFrame, time_range: str) -> pd.DataFrame:
        """Filter dataframe by time range."""
        try:
            if 'datetime' not in df.columns:
                return df
            
            # Parse time range
            if time_range.endswith('h'):
                hours = int(time_range[:-1])
                cutoff_time = datetime.now() - timedelta(hours=hours)
            elif time_range.endswith('d'):
                days = int(time_range[:-1])
                cutoff_time = datetime.now() - timedelta(days=days)
            else:
                return df
            
            return df[df['datetime'] >= cutoff_time]
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to filter by time range: {time_range}")
            return df
    
    def _calculate_trend(self, df: pd.DataFrame, column: str) -> Dict:
        """Calculate trend for a specific column."""
        try:
            if column not in df.columns:
                return {"error": f"Column {column} not found"}
            
            values = df[column].dropna()
            if len(values) < 2:
                return {"error": "Insufficient data for trend calculation"}
            
            # Calculate linear trend
            x = np.arange(len(values))
            slope, intercept = np.polyfit(x, values, 1)
            
            # Calculate trend direction
            if slope > 0.01:
                direction = "increasing"
            elif slope < -0.01:
                direction = "decreasing"
            else:
                direction = "stable"
            
            return {
                "slope": slope,
                "intercept": intercept,
                "direction": direction,
                "mean": values.mean(),
                "std": values.std(),
                "min": values.min(),
                "max": values.max()
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_network_trend(self, df: pd.DataFrame) -> Dict:
        """Calculate network usage trend."""
        try:
            if 'network_bytes_sent' not in df.columns or 'network_bytes_recv' not in df.columns:
                return {"error": "Network columns not found"}
            
            # Calculate total network usage
            df['network_total'] = df['network_bytes_sent'] + df['network_bytes_recv']
            
            return self._calculate_trend(df, 'network_total')
            
        except Exception as e:
            return {"error": str(e)}
    
    def _detect_column_anomalies(self, df: pd.DataFrame, column: str, threshold: float) -> List[Dict]:
        """Detect anomalies in a specific column."""
        try:
            if column not in df.columns:
                return []
            
            values = df[column].dropna()
            if len(values) < 3:
                return []
            
            mean = values.mean()
            std = values.std()
            
            # Find values beyond threshold
            anomalies = []
            for idx, value in enumerate(values):
                z_score = abs((value - mean) / std) if std > 0 else 0
                if z_score > threshold:
                    anomalies.append({
                        "index": idx,
                        "value": value,
                        "z_score": z_score,
                        "timestamp": df.iloc[idx].get('datetime', idx)
                    })
            
            return anomalies
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to detect anomalies in column {column}")
            return []
    
    def _detect_network_anomalies(self, df: pd.DataFrame, threshold: float) -> List[Dict]:
        """Detect network usage anomalies."""
        try:
            if 'network_bytes_sent' not in df.columns or 'network_bytes_recv' not in df.columns:
                return []
            
            df['network_total'] = df['network_bytes_sent'] + df['network_bytes_recv']
            return self._detect_column_anomalies(df, 'network_total', threshold)
            
        except Exception as e:
            return []
    
    def _calculate_summary_stats(self, df: pd.DataFrame) -> Dict:
        """Calculate summary statistics for all numeric columns."""
        try:
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            summary = {}
            
            for col in numeric_columns:
                if col in df.columns:
                    values = df[col].dropna()
                    if len(values) > 0:
                        summary[col] = {
                            "count": len(values),
                            "mean": values.mean(),
                            "std": values.std(),
                            "min": values.min(),
                            "max": values.max(),
                            "median": values.median()
                        }
            
            return summary
            
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_cpu_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate CPU-specific metrics."""
        try:
            if 'cpu_percent' not in df.columns:
                return {"error": "CPU data not available"}
            
            cpu_values = df['cpu_percent'].dropna()
            if len(cpu_values) == 0:
                return {"error": "No CPU data available"}
            
            return {
                "avg_usage": cpu_values.mean(),
                "peak_usage": cpu_values.max(),
                "usage_std": cpu_values.std(),
                "high_usage_periods": len(cpu_values[cpu_values > 80]),
                "low_usage_periods": len(cpu_values[cpu_values < 20])
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_memory_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate memory-specific metrics."""
        try:
            if 'memory_percent' not in df.columns:
                return {"error": "Memory data not available"}
            
            memory_values = df['memory_percent'].dropna()
            if len(memory_values) == 0:
                return {"error": "No memory data available"}
            
            return {
                "avg_usage": memory_values.mean(),
                "peak_usage": memory_values.max(),
                "usage_std": memory_values.std(),
                "high_usage_periods": len(memory_values[memory_values > 80]),
                "swap_usage": df.get('swap_percent', pd.Series()).mean() if 'swap_percent' in df.columns else 0
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_disk_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate disk-specific metrics."""
        try:
            if 'disk_percent' not in df.columns:
                return {"error": "Disk data not available"}
            
            disk_values = df['disk_percent'].dropna()
            if len(disk_values) == 0:
                return {"error": "No disk data available"}
            
            return {
                "avg_usage": disk_values.mean(),
                "peak_usage": disk_values.max(),
                "usage_std": disk_values.std(),
                "high_usage_periods": len(disk_values[disk_values > 90]),
                "io_read_total": df.get('disk_io_read', pd.Series()).sum() if 'disk_io_read' in df.columns else 0,
                "io_write_total": df.get('disk_io_write', pd.Series()).sum() if 'disk_io_write' in df.columns else 0
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_network_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate network-specific metrics."""
        try:
            if 'network_bytes_sent' not in df.columns or 'network_bytes_recv' not in df.columns:
                return {"error": "Network data not available"}
            
            sent_total = df['network_bytes_sent'].sum()
            recv_total = df['network_bytes_recv'].sum()
            
            return {
                "total_sent": sent_total,
                "total_received": recv_total,
                "total_traffic": sent_total + recv_total,
                "avg_sent_rate": sent_total / len(df) if len(df) > 0 else 0,
                "avg_received_rate": recv_total / len(df) if len(df) > 0 else 0
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_performance_score(self, df: pd.DataFrame) -> float:
        """Calculate overall performance score (0-100)."""
        try:
            score = 100.0
            
            # CPU penalty
            if 'cpu_percent' in df.columns:
                avg_cpu = df['cpu_percent'].mean()
                if avg_cpu > 80:
                    score -= 20
                elif avg_cpu > 60:
                    score -= 10
            
            # Memory penalty
            if 'memory_percent' in df.columns:
                avg_memory = df['memory_percent'].mean()
                if avg_memory > 80:
                    score -= 20
                elif avg_memory > 60:
                    score -= 10
            
            # Disk penalty
            if 'disk_percent' in df.columns:
                avg_disk = df['disk_percent'].mean()
                if avg_disk > 90:
                    score -= 20
                elif avg_disk > 80:
                    score -= 10
            
            return max(0, score)
            
        except Exception as e:
            return 0.0 