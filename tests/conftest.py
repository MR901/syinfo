"""Simple test configuration for SyInfo."""

from unittest.mock import patch

import pytest


@pytest.fixture
def mock_system():
    """Simple system mocks for testing."""
    with patch("psutil.cpu_count", return_value=8), patch(
        "psutil.virtual_memory",
    ) as mock_memory, patch("subprocess.run") as mock_run:

        # Mock memory
        mock_memory.return_value.total = 16 * 1024**3  # 16GB
        mock_memory.return_value.available = 8 * 1024**3  # 8GB
        mock_memory.return_value.percent = 50.0

        # Mock subprocess
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "test output"

        yield {"memory": mock_memory, "run": mock_run}
