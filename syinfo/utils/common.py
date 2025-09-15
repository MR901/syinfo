"""Common utility functions and decorators."""

import functools
import logging
import platform
import time
from functools import lru_cache
from typing import Any, Callable, Dict, Tuple, TypeVar

from syinfo.exceptions import SystemAccessError, ValidationError

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
    "handle_system_error",
    "create_highlighted_heading",
    "monitor_performance", 
    "get_system_info_cached",
]
