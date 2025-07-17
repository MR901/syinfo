"""CLI Output Formatter

Handles formatting of CLI output in various formats.
"""

import json
import sys
from typing import Dict, Any, List, Optional


class OutputFormatter:
    """Format CLI output in different styles."""
    
    # ANSI color codes
    COLORS = {
        'PURPLE': '\033[95m',
        'CYAN': '\033[96m', 
        'DARKCYAN': '\033[36m',
        'BLUE': '\033[94m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'RED': '\033[91m',
        'BOLD': '\033[1m',
        'UNDER': '\033[4m',
        'END': '\033[0m'
    }
    
    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """Add color to text."""
        color_code = cls.COLORS.get(color.upper(), '')
        return f"{color_code}{text}{cls.COLORS['END']}"
    
    @classmethod
    def success(cls, message: str) -> str:
        """Format success message."""
        return cls.colorize(f"✅ {message}", "GREEN")
    
    @classmethod
    def error(cls, message: str) -> str:
        """Format error message."""
        return cls.colorize(f"❌ {message}", "RED")
    
    @classmethod
    def warning(cls, message: str) -> str:
        """Format warning message."""
        return cls.colorize(f"⚠️  {message}", "YELLOW")
    
    @classmethod
    def info(cls, message: str) -> str:
        """Format info message."""
        return cls.colorize(f"ℹ️  {message}", "BLUE")
    
    @classmethod
    def header(cls, text: str) -> str:
        """Format header text."""
        return cls.colorize(f"\n{text}", "BOLD")
    
    @classmethod
    def section(cls, text: str) -> str:
        """Format section text."""
        return cls.colorize(f"\n{text}:", "CYAN")
    
    @classmethod
    def format_json(cls, data: Dict[str, Any], indent: int = 2) -> str:
        """Format data as JSON."""
        return json.dumps(data, indent=indent, default=str)
    
    @classmethod
    def format_table(cls, headers: List[str], rows: List[List[str]]) -> str:
        """Format data as a table."""
        if not headers or not rows:
            return ""
        
        # Calculate column widths
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(header)
            for row in rows:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            col_widths.append(max_width + 2)
        
        # Create header
        table = []
        header_row = "|"
        separator_row = "|"
        for header, width in zip(headers, col_widths):
            header_row += f" {header:<{width-1}}|"
            separator_row += f" {'-' * (width-1)} |"
        
        table.append(header_row)
        table.append(separator_row)
        
        # Add data rows
        for row in rows:
            row_str = "|"
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    row_str += f" {str(cell):<{col_widths[i]-1}}|"
            table.append(row_str)
        
        return "\n".join(table)
    
    @classmethod
    def print_result(cls, result: Dict[str, Any], format: str = "auto") -> None:
        """Print formatted result."""
        if format == "json":
            print(cls.format_json(result))
            return
        
        # Auto format based on result structure
        if result.get("success"):
            print(cls.success(result.get("message", "Operation completed successfully")))
            
            if "data" in result:
                data = result["data"]
                if isinstance(data, dict):
                    if "template" in data:
                        print(cls.section("Cron Template"))
                        print(data["template"])
                    elif "dashboard_path" in data:
                        print(cls.info(f"Output: {data['dashboard_path']}"))
                    elif "config_path" in data:
                        print(cls.info(f"Config: {data['config_path']}"))
                    else:
                        print(cls.section("Data"))
                        print(cls.format_json(data))
                elif isinstance(data, list):
                    print(cls.section("Data"))
                    for item in data:
                        print(f"  - {item}")
                else:
                    print(cls.section("Data"))
                    print(data)
        else:
            print(cls.error(result.get("error", "Operation failed")))
        
        if "instructions" in result:
            print(cls.warning(result["instructions"]))
    
    @classmethod
    def print_contact(cls) -> str:
        """Print contact information."""
        contact_info = [
            cls.colorize("Contact Information:", "BOLD"),
            f"  Email: {cls.colorize('mohitrajput901@gmail.com', 'BLUE')}",
            f"  GitHub: {cls.colorize('https://github.com/MR901/syinfo', 'BLUE')}"
        ]
        return "\n".join(contact_info) 