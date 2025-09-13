"""Utility functions and classes for the SyInfo package.

This module provides core utility functions for system operations,
data conversion, and command execution with proper error handling.
"""

import functools
import logging
import os
import platform
import subprocess
import time
import urllib.request
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union, Tuple

from syinfo.constants import (
    UNKNOWN, 
    NEED_SUDO, 
    BYTES_IN_KB, 
    BYTES_IN_MB, 
    BYTES_IN_GB, 
    BYTES_IN_TB,
    DAY_IN_SECONDS,
    HOUR_IN_SECONDS,
    MINUTE_IN_SECONDS
)
from syinfo.exceptions import (
    SystemAccessError,
    ValidationError,
)


# Type variables for generic functions
F = TypeVar("F", bound=Callable[..., Any])

# Configure logging
logger = logging.getLogger(__name__)


def handle_system_error(func):
    """Simple decorator for system error handling."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PermissionError as e:
            raise SystemAccessError(f"Insufficient permissions: {e!s}")
        except Exception as e:
            raise SystemAccessError(f"Error in {func.__name__}: {e!s}")

    return wrapper


def create_highlighted_heading(
    msg: str, 
    line_symbol: str = "━", 
    total_length: int = 100, 
    prefix_suffix: str = "#",
    center_highlighter: Tuple[str, str] = (" ◄◂◀ ", " ▶▸► ")
) -> str:
    """Create a center aligned message with highlighters.
    
    Args:
        msg: The message to highlight
        line_symbol: Character used for the line
        total_length: Total length of the heading
        prefix_suffix: Prefix/suffix characters
        center_highlighter: Tuple of left and right highlighter strings
        
    Returns:
        Formatted heading string with ANSI color codes
        
    Raises:
        ValidationError: If parameters are invalid
    """
    if not isinstance(msg, str):
        raise ValidationError("Message must be a string", details={"field_name": "msg", "expected_type": str.__name__})
    if total_length < 20:
        raise ValidationError("Total length must be at least 20", details={"field_name": "total_length"})
    
    msg = f" {msg} "
    msg_len = len(msg)
    msg = "\033[1m" + msg + "\033[0m"
    
    start, end = (
        (f"{prefix_suffix} ", f" {prefix_suffix}")
        if len(prefix_suffix) > 0 else
        ("", "")
    )
    
    lt_sep_cnt = (
        int(total_length / 2) - len(center_highlighter[0]) - len(start) -
        (int(msg_len / 2) if msg_len % 2 == 0 else int((msg_len + 1) / 2))
    )
    rt_sep_cnt = (
        int(total_length / 2) - len(center_highlighter[1]) - len(end) -
        (int(msg_len / 2) if msg_len % 2 == 0 else int((msg_len - 1) / 2))
    )
    
    _msg = f"{start}{line_symbol*lt_sep_cnt}{center_highlighter[0]}{msg}{center_highlighter[1]}{line_symbol*rt_sep_cnt}{end}"
    return _msg


class HumanReadable:
    """Convert various data formats to human-readable representations.
    
    This class provides static methods for converting bytes to human-readable sizes,
    time durations to readable formats, and other data conversions.
    Methods are cached for performance optimization.
    """

    @staticmethod
    @lru_cache(maxsize=128)
    def size_to_bytes(size: Union[str, int, float]) -> int:
        """Convert size with units to number of bytes.
        
        Args:
            size: Size string with unit (e.g., "32 MB", "100 kB") or numeric value
            
        Returns:
            Number of bytes as integer
            
        Raises:
            ValidationError: If size format is invalid
            
        Examples:
            >>> HumanReadable.size_to_bytes("32 MB")
            33554432
            >>> HumanReadable.size_to_bytes("1 GB")
            1073741824
        """
        multipliers: Dict[str, int] = {
            "kb": BYTES_IN_KB,
            "mb": BYTES_IN_MB,
            "gb": BYTES_IN_GB,
            "tb": BYTES_IN_TB,
        }
        
        if isinstance(size, (int, float)):
            return int(size)
            
        size_str = str(size).strip().lower()
        
        # Remove spaces between number and unit
        size_str = size_str.replace(" ", "")
        
        # Check for unit multipliers
        for suffix, multiplier in multipliers.items():
            if size_str.endswith(suffix):
                try:
                    value = float(size_str[:-len(suffix)])
                    return int(value * multiplier)
                except ValueError:
                    raise ValidationError(
                        f"Invalid numeric value in size: {size}",
                        details={"field_name": "size", "field_value": str(size)}
                    )
        
        # Handle bytes suffix
        if size_str.endswith("b"):
            try:
                return int(float(size_str[:-1]))
            except ValueError:
                raise ValidationError(
                    f"Invalid numeric value in size: {size}",
                    details={"field_name": "size", "field_value": str(size)}
                )
        
        # Plain number
        try:
            return int(float(size_str))
        except ValueError:
            raise ValidationError(
                f"Invalid size format: {size}. Expected format like '1GB', '512MB', or plain number",
                details={"field_name": "size", "field_value": str(size)}
            )

    @staticmethod
    @lru_cache(maxsize=128)
    def bytes_to_size(num_bytes: Union[int, float], suffix: str = "B") -> str:
        """Convert bytes to a human-readable format.
        
        Args:
            num_bytes: Number of bytes to convert
            suffix: Suffix to append to the unit
            
        Returns:
            Human-readable size string
            
        Examples:
            >>> HumanReadable.bytes_to_size(1073741824)
            '1.0 GB'
            >>> HumanReadable.bytes_to_size(1536)
            '1.5 KB'
        """
        if not isinstance(num_bytes, (int, float)):
            raise ValidationError(
                "num_bytes must be numeric",
                details={"field_name": "num_bytes", "expected_type": "int or float"}
            )
            
        if num_bytes < 0:
            return f"-{HumanReadable.bytes_to_size(-num_bytes, suffix)}"
            
        units = ["", "K", "M", "G", "T", "P", "E", "Z"]
        
        for unit in units:
            if abs(num_bytes) < 1024.0:
                return f"{num_bytes:3.1f} {unit}{suffix}"
            num_bytes /= 1024.0
        
        return f"{num_bytes:.1f} Yi{suffix}"

    @staticmethod
    @lru_cache(maxsize=64)
    def time_spend(time_in_sec: Union[int, float]) -> str:
        """Convert time in seconds to human readable format.
        
        Args:
            time_in_sec: Time duration in seconds
            
        Returns:
            Human readable time string
            
        Raises:
            ValidationError: If time_in_sec is not numeric
            
        Examples:
            >>> HumanReadable.time_spend(3661)
            '1 hr, 1 min, 1 sec, 0.0 ms'
            >>> HumanReadable.time_spend(90)
            '1 min, 30 sec, 0.0 ms'
        """
        if not isinstance(time_in_sec, (int, float)):
            raise ValidationError(
                "time_in_sec must be numeric",
                details={"field_name": "time_in_sec", "expected_type": "int or float"}
            )
            
        if time_in_sec < 0:
            return f"negative time: {time_in_sec}"
        
        day = int(time_in_sec // DAY_IN_SECONDS)
        time_in_sec = time_in_sec % DAY_IN_SECONDS
        hour = int(time_in_sec // HOUR_IN_SECONDS)
        time_in_sec %= HOUR_IN_SECONDS
        minutes = int(time_in_sec // MINUTE_IN_SECONDS)
        time_in_sec %= MINUTE_IN_SECONDS
        seconds = int(time_in_sec)
        msec = round((time_in_sec % 1) * 1000, 2)

        if day != 0:
            return f"{day} day, {hour} hr, {minutes} min, {seconds} sec, {msec} ms"
        elif hour != 0:
            return f"{hour} hr, {minutes} min, {seconds} sec, {msec} ms"
        elif minutes != 0:
            return f"{minutes} min, {seconds} sec, {msec} ms"
        else:
            return f"{seconds} sec, {msec} ms"


class Execute:
    """Execute commands on shell or make API requests with proper error handling.
    
    This class provides secure command execution and API request functionality
    with comprehensive error handling and logging.
    """

    @staticmethod
    @handle_system_error
    def on_shell(
        cmd: str, 
        line_no: Optional[int] = None,
        timeout: Optional[int] = 30,
        capture_stderr: bool = True
    ) -> str:
        """Execute a shell command with proper error handling.
        
        Args:
            cmd: Shell command to execute
            line_no: Specific line number to return (None for all output)
            timeout: Command timeout in seconds
            capture_stderr: Whether to capture stderr output
            
        Returns:
            Command output as string
            
        Raises:
            SystemAccessError: If command requires elevated privileges
            ValidationError: If command is invalid
            
        Examples:
            >>> Execute.on_shell("echo 'hello'")
            'hello'
        """
        if not cmd or not isinstance(cmd, str):
            raise ValidationError("Command must be a non-empty string", details={"field_name": "cmd"})
            
        # Security check: warn about potentially dangerous commands
        dangerous_cmds = ["rm -rf", "dd if=", "mkfs", "fdisk", ":(){:|:&};:"]
        if any(danger in cmd.lower() for danger in dangerous_cmds):
            logger.warning(f"Potentially dangerous command detected: {cmd}")
        
        result: str = UNKNOWN
        
        try:
            # Use subprocess.run for better control and security
            process_result = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE if capture_stderr else None,
                timeout=timeout,
                text=True,
                check=False  # Don't raise exception on non-zero exit
            )
            
            if process_result.stderr and capture_stderr:
                error_msg = process_result.stderr.strip()
                if error_msg:
                    logger.warning(f"Command stderr: {error_msg}")
            
            stdout = process_result.stdout or ""
            
            if line_no is not None:
                lines = stdout.split("\n")
                if 0 <= line_no < len(lines):
                    result = lines[line_no].strip()
                else:
                    logger.warning(f"Line number {line_no} out of range for command output")
                    result = UNKNOWN
            else:
                result = stdout.strip()
                
        except subprocess.TimeoutExpired:
            raise SystemAccessError(
                f"Command timed out after {timeout} seconds: {cmd}",
                details={"timeout": timeout, "command": cmd}
            )
        except subprocess.SubprocessError as e:
            raise SystemAccessError(
                f"Failed to execute command: {cmd}",
                details={"error": str(e), "command": cmd}
            )
        except Exception as e:
            logger.error(f"Unexpected error executing command '{cmd}': {e}")
            raise
        
        # Check if sudo is needed
        if (
            platform.system() in ["Linux", "Darwin"]
            and "sudo " in cmd.lower()
            and os.getuid() != 0
            and result == UNKNOWN
        ):
            logger.info(f"Command may need elevated privileges: {cmd}")
            return NEED_SUDO
            
        return result

    @staticmethod
    def api(
        url: str, 
        line_no: Optional[int] = None,
        timeout: int = 30,
        headers: Optional[Dict[str, str]] = None
    ) -> str:
        """Make an API request with proper error handling.
        
        Args:
            url: URL to request
            line_no: Specific line number to return (None for all response)
            timeout: Request timeout in seconds
            headers: Optional HTTP headers
            
        Returns:
            API response as string
            
        Raises:
            ValidationError: If URL is invalid
            SystemAccessError: If request fails
            
        Examples:
            >>> Execute.api("https://api.github.com")
            '{"current_user_url":"https://api.github.com/user",...}'
        """
        if not url or not isinstance(url, str):
            raise ValidationError("URL must be a non-empty string", details={"field_name": "url"})
            
        if not url.startswith(("http://", "https://")):
            raise ValidationError("URL must start with http:// or https://", details={"field_name": "url"})
        
        result: str = UNKNOWN
        
        try:
            # Create request with headers
            request = urllib.request.Request(url)
            
            # Add default user agent
            request.add_header("User-Agent", "SyInfo/1.0 (+https://github.com/MR901/syinfo)")
            
            # Add custom headers if provided
            if headers:
                for key, value in headers.items():
                    request.add_header(key, value)
            
            # Make request with timeout
            with urllib.request.urlopen(request, timeout=timeout) as response:
                content = response.read().decode("utf-8")
                
                if line_no is not None:
                    lines = content.split("\n")
                    if 0 <= line_no < len(lines):
                        result = lines[line_no].strip()
                    else:
                        logger.warning(f"Line number {line_no} out of range for API response")
                        result = UNKNOWN
                else:
                    result = content.strip()
                    
        except urllib.error.HTTPError as e:
            raise SystemAccessError(
                f"HTTP error {e.code} requesting {url}: {e.reason}",
                details={"status_code": e.code, "url": url}
            )
        except urllib.error.URLError as e:
            raise SystemAccessError(
                f"URL error requesting {url}: {e.reason}",
                details={"url": url, "reason": str(e.reason)}
            )
        except Exception as e:
            logger.error(f"Unexpected error requesting {url}: {e}")
            raise SystemAccessError(
                f"Failed to request {url}: {str(e)}",
                details={"url": url, "error": str(e)}
            )
        
        return result


# Performance monitoring decorator
def monitor_performance(func: F) -> F:
    """Decorator to monitor function performance.
    
    Args:
        func: Function to monitor
        
    Returns:
        Wrapped function with performance monitoring
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(
                f"Function {func.__name__} executed in {execution_time:.4f} seconds"
            )
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"Function {func.__name__} failed after {execution_time:.4f} seconds: {e}"
            )
            raise
    return wrapper


# File system utilities
def safe_file_read(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """Safely read a file with proper error handling.
    
    Args:
        file_path: Path to the file
        encoding: File encoding
        
    Returns:
        File contents as string
        
    Raises:
        SystemAccessError: If file cannot be read
    """
    path = Path(file_path)
    
    if not path.exists():
        raise SystemAccessError(
            f"File not found: {path}",
            resource_path=str(path)
        )
    
    if not path.is_file():
        raise SystemAccessError(
            f"Path is not a file: {path}",
            resource_path=str(path)
        )
    
    try:
        return path.read_text(encoding=encoding)
    except PermissionError:
        raise SystemAccessError(
            f"Permission denied reading file: {path}",
            required_privilege="read",
            resource_path=str(path)
        )
    except UnicodeDecodeError as e:
        raise SystemAccessError(
            f"Cannot decode file {path} with encoding {encoding}: {e}",
            resource_path=str(path)
        )


def get_system_info_cached() -> Dict[str, Any]:
    """Get cached system information to avoid repeated system calls.
    
    Returns:
        Dictionary containing basic system information
    """
    @lru_cache(maxsize=1)
    def _get_system_info():
        return {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node(),
        }
    
    return _get_system_info()


__all__ = [
    "create_highlighted_heading",
    "HumanReadable", 
    "Execute",
    "monitor_performance",
    "safe_file_read",
    "get_system_info_cached",
]
