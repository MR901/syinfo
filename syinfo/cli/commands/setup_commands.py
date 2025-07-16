"""Setup Commands Module

Handles system setup and configuration commands.
"""

import json
import sys
from typing import Dict, Any, Optional

try:
    from syinfo.monitoring.scheduler import CronManager
    from syinfo.monitoring.utils import MonitoringConfig
    SETUP_AVAILABLE = True
except ImportError:
    SETUP_AVAILABLE = False


class SetupCommands:
    """System setup and configuration commands."""
    
    @staticmethod
    def install_cron_jobs(
        interval_minutes: int = 1,
        config_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Install monitoring cron jobs."""
        if not SETUP_AVAILABLE:
            return {
                "success": False,
                "error": "Setup features not available. Install required dependencies."
            }
        
        try:
            cron_manager = CronManager()
            
            template = cron_manager.generate_cron_template(
                interval_minutes=interval_minutes,
                config_path=config_path
            )
            
            if template:
                return {
                    "success": True,
                    "data": {"template": template},
                    "message": "Cron template generated successfully",
                    "instructions": "Please manually add the template to your crontab using 'crontab -e'"
                }
            else:
                return {"success": False, "error": "Failed to generate cron template"}
                
        except Exception as e:
            return {"success": False, "error": f"Setup error: {e}"}
    
    @staticmethod
    def remove_cron_jobs() -> Dict[str, Any]:
        """Remove monitoring cron jobs."""
        if not SETUP_AVAILABLE:
            return {
                "success": False,
                "error": "Setup features not available. Install required dependencies."
            }
        
        try:
            cron_manager = CronManager()
            
            if cron_manager.remove_monitoring_jobs():
                return {
                    "success": True,
                    "message": "Monitoring cron jobs removed successfully"
                }
            else:
                return {"success": False, "error": "Failed to remove monitoring cron jobs"}
                
        except Exception as e:
            return {"success": False, "error": f"Setup error: {e}"}
    
    @staticmethod
    def create_config(
        output_path: str = "monitoring_config.yaml",
        template_type: str = "default"
    ) -> Dict[str, Any]:
        """Create monitoring configuration file."""
        if not SETUP_AVAILABLE:
            return {
                "success": False,
                "error": "Setup features not available. Install required dependencies."
            }
        
        try:
            config = MonitoringConfig()
            
            if config.create_template(output_path, template_type):
                return {
                    "success": True,
                    "data": {"config_path": output_path},
                    "message": f"Configuration file created: {output_path}"
                }
            else:
                return {"success": False, "error": "Failed to create configuration file"}
                
        except Exception as e:
            return {"success": False, "error": f"Configuration error: {e}"}
    
    @staticmethod
    def validate_config(config_path: str) -> Dict[str, Any]:
        """Validate monitoring configuration file."""
        if not SETUP_AVAILABLE:
            return {
                "success": False,
                "error": "Setup features not available. Install required dependencies."
            }
        
        try:
            config = MonitoringConfig(config_path)
            validation_result = config.validate()
            
            if validation_result["valid"]:
                return {
                    "success": True,
                    "data": validation_result,
                    "message": "Configuration file is valid"
                }
            else:
                return {
                    "success": False,
                    "data": validation_result,
                    "error": "Configuration file validation failed"
                }
                
        except Exception as e:
            return {"success": False, "error": f"Validation error: {e}"}
    
    @staticmethod
    def setup_directories(base_path: str = "./monitoring_data") -> Dict[str, Any]:
        """Setup monitoring directories."""
        if not SETUP_AVAILABLE:
            return {
                "success": False,
                "error": "Setup features not available. Install required dependencies."
            }
        
        try:
            import os
            
            directories = [
                base_path,
                f"{base_path}/logs",
                f"{base_path}/data",
                f"{base_path}/reports",
                f"{base_path}/charts"
            ]
            
            created_dirs = []
            for directory in directories:
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                    created_dirs.append(directory)
            
            return {
                "success": True,
                "data": {
                    "base_path": base_path,
                    "created_directories": created_dirs,
                    "all_directories": directories
                },
                "message": f"Monitoring directories setup completed at {base_path}"
            }
                
        except Exception as e:
            return {"success": False, "error": f"Directory setup error: {e}"} 