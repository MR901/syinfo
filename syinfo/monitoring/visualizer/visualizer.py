"""
Data visualization module for monitoring data.

This module provides comprehensive visualization capabilities including:
- Real-time dashboards
- Historical trend charts
- Process resource heatmaps
- System health indicators
- Export to multiple formats
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import seaborn as sns

from ..utils.logger import MonitoringLogger


class DataVisualizer:
    """
    Comprehensive visualization system with multiple output formats.
    
    Features:
    - Real-time dashboards
    - Historical trend charts
    - Process resource heatmaps
    - System health indicators
    - Export to multiple formats
    """
    
    def __init__(self):
        """Initialize data visualizer."""
        self.logger = MonitoringLogger()
        # Set matplotlib style
        plt.style.use('default')
        sns.set_palette("husl")
    
    def create_system_dashboard(self, system_data: pd.DataFrame, process_data: Optional[pd.DataFrame] = None, 
                               output_path: str = "system_dashboard.png") -> str:
        """
        Create comprehensive system monitoring dashboard.
        
        Args:
            system_data: System monitoring data
            process_data: Process monitoring data (optional)
            output_path: Path to save the dashboard
            
        Returns:
            Path to the created dashboard file
        """
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('System Monitoring Dashboard', fontsize=16, fontweight='bold')
            
            # CPU Usage
            if 'cpu_percent' in system_data.columns:
                axes[0, 0].plot(system_data['datetime'], system_data['cpu_percent'], 
                               color='red', linewidth=2)
                axes[0, 0].set_title('CPU Usage (%)')
                axes[0, 0].set_ylabel('CPU %')
                axes[0, 0].grid(True, alpha=0.3)
                axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Memory Usage
            if 'memory_percent' in system_data.columns:
                axes[0, 1].plot(system_data['datetime'], system_data['memory_percent'], 
                               color='blue', linewidth=2)
                axes[0, 1].set_title('Memory Usage (%)')
                axes[0, 1].set_ylabel('Memory %')
                axes[0, 1].grid(True, alpha=0.3)
                axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Disk Usage
            if 'disk_percent' in system_data.columns:
                axes[1, 0].plot(system_data['datetime'], system_data['disk_percent'], 
                               color='green', linewidth=2)
                axes[1, 0].set_title('Disk Usage (%)')
                axes[1, 0].set_ylabel('Disk %')
                axes[1, 0].grid(True, alpha=0.3)
                axes[1, 0].tick_params(axis='x', rotation=45)
            
            # Network Usage
            if 'network_bytes_sent' in system_data.columns and 'network_bytes_recv' in system_data.columns:
                axes[1, 1].plot(system_data['datetime'], system_data['network_bytes_sent'] / 1024 / 1024, 
                               label='Sent', color='orange', linewidth=2)
                axes[1, 1].plot(system_data['datetime'], system_data['network_bytes_recv'] / 1024 / 1024, 
                               label='Received', color='purple', linewidth=2)
                axes[1, 1].set_title('Network Usage (MB)')
                axes[1, 1].set_ylabel('MB')
                axes[1, 1].legend()
                axes[1, 1].grid(True, alpha=0.3)
                axes[1, 1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.log_monitoring_event("INFO", f"Dashboard created: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to create system dashboard")
            return ""
    
    def plot_resource_utilization(self, data_file: str, resources: Optional[List[str]] = None, 
                                 output_path: str = "resource_utilization.png") -> str:
        """
        Plot resource utilization over time.
        
        Args:
            data_file: Path to monitoring data file
            resources: List of resources to plot (default: all available)
            output_path: Path to save the plot
            
        Returns:
            Path to the created plot file
        """
        try:
            # Load data
            df = self._load_data(data_file)
            if df is None or df.empty:
                return ""
            
            # Determine resources to plot
            if resources is None:
                resources = ['cpu_percent', 'memory_percent', 'disk_percent']
            
            available_resources = [r for r in resources if r in df.columns]
            if not available_resources:
                return ""
            
            # Create plot
            fig, axes = plt.subplots(len(available_resources), 1, figsize=(12, 3 * len(available_resources)))
            if len(available_resources) == 1:
                axes = [axes]
            
            colors = ['red', 'blue', 'green', 'orange', 'purple']
            
            for i, resource in enumerate(available_resources):
                color = colors[i % len(colors)]
                axes[i].plot(df['datetime'], df[resource], color=color, linewidth=2)
                axes[i].set_title(f'{resource.replace("_", " ").title()}')
                axes[i].set_ylabel('Percentage' if 'percent' in resource else 'Value')
                axes[i].grid(True, alpha=0.3)
                axes[i].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.log_monitoring_event("INFO", f"Resource utilization plot created: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to create resource utilization plot")
            return ""
    
    def generate_performance_charts(self, data_file: str, output_format: str = "html") -> str:
        """
        Generate performance analysis charts.
        
        Args:
            data_file: Path to monitoring data file
            output_format: Output format ("html", "png", "pdf")
            
        Returns:
            Path to the generated charts file
        """
        try:
            # Load data
            df = self._load_data(data_file)
            if df is None or df.empty:
                return ""
            
            if output_format == "html":
                return self._generate_html_report(df, data_file)
            else:
                return self._generate_image_charts(df, output_format)
                
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to generate performance charts")
            return ""
    
    def create_process_heatmap(self, data_file: str, output_path: str = "process_heatmap.png") -> str:
        """
        Create process resource usage heatmap.
        
        Args:
            data_file: Path to process monitoring data file
            output_path: Path to save the heatmap
            
        Returns:
            Path to the created heatmap file
        """
        try:
            # Load data
            df = self._load_data(data_file)
            if df is None or df.empty:
                return ""
            
            # Prepare data for heatmap
            if 'name' in df.columns and 'cpu_percent' in df.columns:
                # Group by process name and calculate average CPU usage
                process_cpu = df.groupby('name')['cpu_percent'].mean().sort_values(ascending=False)
                
                # Create heatmap
                plt.figure(figsize=(10, max(6, len(process_cpu) * 0.3)))
                sns.heatmap(process_cpu.values.reshape(-1, 1), 
                           yticklabels=process_cpu.index,
                           xticklabels=['CPU %'],
                           annot=True,
                           fmt='.1f',
                           cmap='YlOrRd')
                plt.title('Process CPU Usage Heatmap')
                plt.tight_layout()
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()
                
                self.logger.log_monitoring_event("INFO", f"Process heatmap created: {output_path}")
                return output_path
            
            return ""
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to create process heatmap")
            return ""
    
    def _load_data(self, data_file: str) -> Optional[pd.DataFrame]:
        """Load data from file."""
        try:
            if data_file.endswith('.csv'):
                df = pd.read_csv(data_file)
            elif data_file.endswith('.json'):
                with open(data_file, 'r') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
            else:
                return None
            
            # Convert timestamp to datetime
            if 'timestamp' in df.columns:
                df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            elif 'datetime' in df.columns:
                df['datetime'] = pd.to_datetime(df['datetime'])
            
            return df
            
        except Exception as e:
            self.logger.log_error_with_context(e, f"Failed to load data from {data_file}")
            return None
    
    def _generate_html_report(self, df: pd.DataFrame, data_file: str) -> str:
        """Generate HTML report with embedded charts."""
        try:
            # Create multiple charts
            charts = []
            
            # CPU chart
            if 'cpu_percent' in df.columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(df['datetime'], df['cpu_percent'], color='red', linewidth=2)
                ax.set_title('CPU Usage Over Time')
                ax.set_ylabel('CPU %')
                ax.grid(True, alpha=0.3)
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                
                # Save chart as base64 for HTML embedding
                import base64
                from io import BytesIO
                buffer = BytesIO()
                plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
                buffer.seek(0)
                chart_data = base64.b64encode(buffer.getvalue()).decode()
                plt.close()
                
                charts.append(f'<img src="data:image/png;base64,{chart_data}" alt="CPU Usage">')
            
            # Memory chart
            if 'memory_percent' in df.columns:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(df['datetime'], df['memory_percent'], color='blue', linewidth=2)
                ax.set_title('Memory Usage Over Time')
                ax.set_ylabel('Memory %')
                ax.grid(True, alpha=0.3)
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                
                buffer = BytesIO()
                plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
                buffer.seek(0)
                chart_data = base64.b64encode(buffer.getvalue()).decode()
                plt.close()
                
                charts.append(f'<img src="data:image/png;base64,{chart_data}" alt="Memory Usage">')
            
            # Generate HTML
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>System Performance Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                    .chart {{ margin: 20px 0; text-align: center; }}
                    .summary {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>System Performance Report</h1>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Data file: {os.path.basename(data_file)}</p>
                </div>
                
                <div class="summary">
                    <h2>Summary Statistics</h2>
                    <p>Total data points: {len(df)}</p>
                    <p>Time range: {df['datetime'].min()} to {df['datetime'].max()}</p>
                </div>
                
                <div class="charts">
                    {''.join(charts)}
                </div>
            </body>
            </html>
            """
            
            # Save HTML file
            output_path = data_file.replace('.csv', '_report.html').replace('.json', '_report.html')
            with open(output_path, 'w') as f:
                f.write(html_content)
            
            self.logger.log_monitoring_event("INFO", f"HTML report generated: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to generate HTML report")
            return ""
    
    def _generate_image_charts(self, df: pd.DataFrame, output_format: str) -> str:
        """Generate image-based charts."""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('System Performance Analysis', fontsize=16, fontweight='bold')
            
            # CPU Usage
            if 'cpu_percent' in df.columns:
                axes[0, 0].plot(df['datetime'], df['cpu_percent'], color='red', linewidth=2)
                axes[0, 0].set_title('CPU Usage')
                axes[0, 0].set_ylabel('CPU %')
                axes[0, 0].grid(True, alpha=0.3)
                axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Memory Usage
            if 'memory_percent' in df.columns:
                axes[0, 1].plot(df['datetime'], df['memory_percent'], color='blue', linewidth=2)
                axes[0, 1].set_title('Memory Usage')
                axes[0, 1].set_ylabel('Memory %')
                axes[0, 1].grid(True, alpha=0.3)
                axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Disk Usage
            if 'disk_percent' in df.columns:
                axes[1, 0].plot(df['datetime'], df['disk_percent'], color='green', linewidth=2)
                axes[1, 0].set_title('Disk Usage')
                axes[1, 0].set_ylabel('Disk %')
                axes[1, 0].grid(True, alpha=0.3)
                axes[1, 0].tick_params(axis='x', rotation=45)
            
            # Network Usage
            if 'network_bytes_sent' in df.columns and 'network_bytes_recv' in df.columns:
                axes[1, 1].plot(df['datetime'], df['network_bytes_sent'] / 1024 / 1024, 
                               label='Sent', color='orange', linewidth=2)
                axes[1, 1].plot(df['datetime'], df['network_bytes_recv'] / 1024 / 1024, 
                               label='Received', color='purple', linewidth=2)
                axes[1, 1].set_title('Network Usage')
                axes[1, 1].set_ylabel('MB')
                axes[1, 1].legend()
                axes[1, 1].grid(True, alpha=0.3)
                axes[1, 1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            # Save with appropriate format
            output_path = f"performance_charts.{output_format}"
            plt.savefig(output_path, dpi=300, bbox_inches='tight', format=output_format)
            plt.close()
            
            self.logger.log_monitoring_event("INFO", f"Performance charts generated: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.log_error_with_context(e, "Failed to generate image charts")
            return "" 