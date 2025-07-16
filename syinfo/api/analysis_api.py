"""Analysis API Module

Provides programmatic access to data analysis functionality.
"""

from typing import Dict, Any, Optional, List
import json
import os

try:
    from syinfo.monitoring.analyzer import DataAnalyzer
    from syinfo.monitoring.visualizer import DataVisualizer
    ANALYSIS_AVAILABLE = True
except ImportError:
    ANALYSIS_AVAILABLE = False


class AnalysisAPI:
    """API for data analysis operations."""
    
    def __init__(self):
        """Initialize analysis API."""
        self.analyzer = None
        self.visualizer = None
        
        if ANALYSIS_AVAILABLE:
            self.analyzer = DataAnalyzer()
            self.visualizer = DataVisualizer()
    
    def analyze_trends(self, data_file: str) -> Dict[str, Any]:
        """Analyze system trends from data file."""
        if not ANALYSIS_AVAILABLE:
            return {
                "success": False,
                "error": "Analysis features not available"
            }
        
        try:
            trends = self.analyzer.analyze_system_trends(data_file)
            
            if "error" not in trends:
                return {
                    "success": True,
                    "data": trends,
                    "message": "Trend analysis completed successfully"
                }
            else:
                return {"success": False, "error": f"Trend analysis failed: {trends['error']}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def detect_anomalies(self, data_file: str) -> Dict[str, Any]:
        """Detect anomalies in system data."""
        if not ANALYSIS_AVAILABLE:
            return {
                "success": False,
                "error": "Analysis features not available"
            }
        
        try:
            anomalies = self.analyzer.detect_anomalies(data_file)
            
            if "error" not in anomalies:
                return {
                    "success": True,
                    "data": anomalies,
                    "message": "Anomaly detection completed successfully"
                }
            else:
                return {"success": False, "error": f"Anomaly detection failed: {anomalies['error']}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_report(
        self,
        data_file: str,
        output_file: Optional[str] = None,
        include_charts: bool = True
    ) -> Dict[str, Any]:
        """Generate comprehensive analysis report."""
        if not ANALYSIS_AVAILABLE:
            return {
                "success": False,
                "error": "Analysis features not available"
            }
        
        try:
            # Get analysis results
            trends = self.analyzer.analyze_system_trends(data_file)
            anomalies = self.analyzer.detect_anomalies(data_file)
            
            if "error" in trends or "error" in anomalies:
                return {
                    "success": False,
                    "error": "Failed to generate report due to analysis errors"
                }
            
            report = {
                "trends": trends,
                "anomalies": anomalies,
                "summary": {
                    "data_file": data_file,
                    "analysis_timestamp": self.analyzer.get_timestamp()
                }
            }
            
            # Generate charts if requested
            if include_charts:
                chart_path = self.visualizer.create_system_dashboard(
                    data_file,
                    output_path="report_charts.png"
                )
                if chart_path:
                    report["charts"] = {"dashboard": chart_path}
            
            # Save report if output file specified
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(report, f, indent=2)
                return {
                    "success": True,
                    "data": report,
                    "message": f"Report generated and saved to {output_file}"
                }
            else:
                return {
                    "success": True,
                    "data": report,
                    "message": "Report generated successfully"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_dashboard(
        self,
        data_file: str,
        output_path: Optional[str] = None,
        chart_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create visualization dashboard."""
        if not ANALYSIS_AVAILABLE:
            return {
                "success": False,
                "error": "Visualization features not available"
            }
        
        try:
            if not output_path:
                output_path = "system_dashboard.png"
            
            dashboard_path = self.visualizer.create_system_dashboard(
                data_file,
                output_path=output_path,
                chart_types=chart_types
            )
            
            if dashboard_path:
                return {
                    "success": True,
                    "data": {"dashboard_path": dashboard_path},
                    "message": f"Dashboard created successfully: {dashboard_path}"
                }
            else:
                return {"success": False, "error": "Failed to create dashboard"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_chart(
        self,
        data_file: str,
        chart_type: str,
        output_path: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create specific chart type."""
        if not ANALYSIS_AVAILABLE:
            return {
                "success": False,
                "error": "Visualization features not available"
            }
        
        try:
            if not output_path:
                output_path = f"{chart_type}_chart.png"
            
            chart_path = self.visualizer.create_chart(
                data_file,
                chart_type,
                output_path=output_path,
                **kwargs
            )
            
            if chart_path:
                return {
                    "success": True,
                    "data": {"chart_path": chart_path},
                    "message": f"Chart created successfully: {chart_path}"
                }
            else:
                return {"success": False, "error": f"Failed to create {chart_type} chart"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_available_chart_types(self) -> Dict[str, Any]:
        """Get list of available chart types."""
        if not ANALYSIS_AVAILABLE:
            return {
                "success": False,
                "error": "Visualization features not available"
            }
        
        try:
            chart_types = [
                'cpu_usage', 'memory_usage', 'disk_usage', 'network_io',
                'process_count', 'system_load', 'temperature', 'custom'
            ]
            
            return {
                "success": True,
                "data": chart_types,
                "message": f"Available chart types: {len(chart_types)}"
            }
                
        except Exception as e:
            return {"success": False, "error": str(e)} 