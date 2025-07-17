"""Analyze Commands Module

Handles data analysis and visualization commands.
"""

import json
import sys
from typing import Dict, Any, Optional

try:
    from syinfo.monitoring.analyzer import DataAnalyzer
    from syinfo.monitoring.visualizer import DataVisualizer
    ANALYSIS_AVAILABLE = True
except ImportError:
    ANALYSIS_AVAILABLE = False


class AnalyzeCommands:
    """Data analysis and visualization commands."""
    
    @staticmethod
    def analyze_trends(data_file: str) -> Dict[str, Any]:
        """Analyze system trends from data file."""
        if not ANALYSIS_AVAILABLE:
            return {
                "success": False,
                "error": "Analysis features not available. Install required dependencies."
            }
        
        try:
            analyzer = DataAnalyzer()
            trends = analyzer.analyze_system_trends(data_file)
            
            if "error" not in trends:
                return {
                    "success": True,
                    "data": trends,
                    "message": "Trend analysis completed successfully"
                }
            else:
                return {"success": False, "error": f"Trend analysis failed: {trends['error']}"}
                
        except Exception as e:
            return {"success": False, "error": f"Analysis error: {e}"}
    
    @staticmethod
    def detect_anomalies(data_file: str) -> Dict[str, Any]:
        """Detect anomalies in system data."""
        if not ANALYSIS_AVAILABLE:
            return {
                "success": False,
                "error": "Analysis features not available. Install required dependencies."
            }
        
        try:
            analyzer = DataAnalyzer()
            anomalies = analyzer.detect_anomalies(data_file)
            
            if "error" not in anomalies:
                return {
                    "success": True,
                    "data": anomalies,
                    "message": "Anomaly detection completed successfully"
                }
            else:
                return {"success": False, "error": f"Anomaly detection failed: {anomalies['error']}"}
                
        except Exception as e:
            return {"success": False, "error": f"Analysis error: {e}"}
    
    @staticmethod
    def generate_report(data_file: str, output_file: Optional[str] = None) -> Dict[str, Any]:
        """Generate comprehensive analysis report."""
        if not ANALYSIS_AVAILABLE:
            return {
                "success": False,
                "error": "Analysis features not available. Install required dependencies."
            }
        
        try:
            analyzer = DataAnalyzer()
            
            # Get both trends and anomalies
            trends = analyzer.analyze_system_trends(data_file)
            anomalies = analyzer.detect_anomalies(data_file)
            
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
                    "analysis_timestamp": analyzer.get_timestamp()
                }
            }
            
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
            return {"success": False, "error": f"Report generation error: {e}"}
    
    @staticmethod
    def create_dashboard(
        data_file: str,
        output_path: Optional[str] = None,
        chart_types: Optional[list] = None
    ) -> Dict[str, Any]:
        """Create visualization dashboard."""
        if not ANALYSIS_AVAILABLE:
            return {
                "success": False,
                "error": "Visualization features not available. Install required dependencies."
            }
        
        try:
            visualizer = DataVisualizer()
            
            if not output_path:
                output_path = "system_dashboard.png"
            
            dashboard_path = visualizer.create_system_dashboard(
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
            return {"success": False, "error": f"Dashboard creation error: {e}"}
    
    @staticmethod
    def create_chart(
        data_file: str,
        chart_type: str,
        output_path: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create specific chart type."""
        if not ANALYSIS_AVAILABLE:
            return {
                "success": False,
                "error": "Visualization features not available. Install required dependencies."
            }
        
        try:
            visualizer = DataVisualizer()
            
            if not output_path:
                output_path = f"{chart_type}_chart.png"
            
            chart_path = visualizer.create_chart(
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
            return {"success": False, "error": f"Chart creation error: {e}"} 