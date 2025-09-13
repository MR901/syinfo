# Contributing to SyInfo

Thank you for your interest in contributing to SyInfo! This guide will help you get started with development and ensure your contributions align with our standards.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A Linux development environment (for full functionality)

### Setting up the Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MR901/syinfo.git
   cd syinfo
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e .[dev,full]
   ```

4. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

5. **Run the test suite:**
   ```bash
   pytest
   ```

## Code Quality Standards

### Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking
- **Bandit**: Security vulnerability scanning

Run all checks:
```bash
# Format code
black syinfo tests
isort syinfo tests

# Lint code
ruff check syinfo tests

# Type checking
mypy syinfo

# Security check
bandit -r syinfo
```

### Type Hints

All code must include comprehensive type hints:

```python
from typing import Dict, List, Optional, Union, Any

def process_data(
    data: Dict[str, Any],
    filters: Optional[List[str]] = None,
    strict: bool = True
) -> Dict[str, Union[str, int, float]]:
    """Process system data with optional filtering."""
    # Implementation here
    pass
```

### Error Handling

Use the custom exception hierarchy:

```python
from syinfo.core.exceptions import (
    DataCollectionError,
    SystemAccessError,
    ValidationError
)

def collect_system_info() -> Dict[str, Any]:
    """Collect system information with proper error handling."""
    try:
        # System data collection
        pass
    except PermissionError as e:
        raise SystemAccessError(
            "Insufficient permissions to access system information",
            details={"required_privilege": "elevated"},
            original_exception=e
        )
    except ValueError as e:
        raise ValidationError(
            "Invalid system data format",
            original_exception=e
        )
```

### Documentation

All functions and classes must have comprehensive docstrings:

```python
def analyze_performance(
    data: Dict[str, Any],
    metrics: List[str],
    threshold: float = 0.8
) -> Dict[str, Any]:
    """Analyze system performance metrics.
    
    This function processes raw system data and calculates performance
    metrics based on the provided thresholds and criteria.
    
    Args:
        data: Raw system data dictionary containing metrics
        metrics: List of metric names to analyze
        threshold: Performance threshold (0.0-1.0) for alerts
        
    Returns:
        Dictionary containing analyzed performance data with keys:
        - 'overall_score': Overall performance score (0.0-1.0)
        - 'alerts': List of performance alerts
        - 'metrics': Detailed metric analysis
        
    Raises:
        ValidationError: If data format is invalid
        DataCollectionError: If required metrics are missing
        
    Examples:
        >>> data = {'cpu_usage': 75.5, 'memory_usage': 60.2}
        >>> result = analyze_performance(data, ['cpu_usage'], 0.8)
        >>> print(f"Score: {result['overall_score']:.2f}")
        Score: 0.75
        
    Note:
        Performance analysis requires at least 5 minutes of data
        for accurate trending calculations.
    """
```

## Testing Guidelines

### Test Structure

Organize tests in the following structure:
```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for combined functionality
├── performance/    # Performance and benchmark tests
└── conftest.py    # Shared fixtures and configuration
```

### Writing Tests

Use pytest with comprehensive fixtures:

```python
import pytest
from unittest.mock import Mock, patch

def test_device_info_collection(mock_system_calls):
    """Test device information collection with mocked system calls."""
    # Arrange
    mock_system_calls['cpu_count'].return_value = 8
    
    # Act
    collector = DeviceInfoCollector()
    info = collector.get_system_info()
    
    # Assert
    assert info['cpu_info']['cores']['logical'] == 8
    assert 'device_info' in info
    assert 'hostname' in info['device_info']

@pytest.mark.performance
def test_collection_performance(performance_threshold):
    """Test that data collection meets performance requirements."""
    import time
    
    start_time = time.time()
    collector = DeviceInfoCollector()
    info = collector.get_system_info()
    execution_time = time.time() - start_time
    
    assert execution_time < performance_threshold['device_info_collection']
```

### Test Coverage

Maintain minimum 80% test coverage:

```bash
pytest --cov=syinfo --cov-report=html --cov-report=term-missing
```

## Architecture Guidelines

### SOLID Principles

Follow SOLID design principles:

1. **Single Responsibility**: Each class has one reason to change
2. **Open/Closed**: Open for extension, closed for modification
3. **Liskov Substitution**: Derived classes must be substitutable
4. **Interface Segregation**: Many specific interfaces are better
5. **Dependency Inversion**: Depend on abstractions, not concretions

### Design Patterns

Use appropriate design patterns:

- **Factory Pattern**: For creating collectors and services
- **Observer Pattern**: For monitoring and event handling  
- **Strategy Pattern**: For different data collection strategies
- **Decorator Pattern**: For performance monitoring and caching

### Error Handling Strategy

Implement comprehensive error handling:

```python
# Good: Specific exceptions with context
try:
    data = collect_system_data()
except PermissionError as e:
    raise SystemAccessError(
        "Cannot access system resources",
        details={"required_privilege": "elevated", "resource_path": "/sys/devices"},
        original_exception=e
    )

# Bad: Generic exception handling
try:
    data = collect_system_data()
except Exception as e:
    print(f"Error: {e}")  # Don't do this
```

## Performance Considerations

### Caching

Use appropriate caching strategies:

```python
from functools import lru_cache
import time

class SystemCollector:
    def __init__(self):
        self._cache_timeout = 300  # 5 minutes
        self._last_update = None
        self._cached_data = {}
    
    @lru_cache(maxsize=128)
    def get_static_info(self) -> Dict[str, Any]:
        """Get static system information (cached)."""
        pass
    
    def get_dynamic_info(self) -> Dict[str, Any]:
        """Get dynamic system information (cache with timeout)."""
        current_time = time.time()
        if (self._last_update is None or 
            current_time - self._last_update > self._cache_timeout):
            self._cached_data = self._collect_dynamic_data()
            self._last_update = current_time
        return self._cached_data
```

### Memory Management

Be mindful of memory usage:

```python
# Good: Use generators for large datasets
def process_large_dataset():
    for item in data_generator():
        yield process_item(item)

# Good: Clean up resources
try:
    with open(large_file) as f:
        process_file(f)
finally:
    cleanup_resources()

# Bad: Loading everything into memory
def process_data():
    all_data = load_entire_dataset()  # Avoid this
    return [process_item(item) for item in all_data]
```

## Contribution Workflow

### 1. Planning

- Check existing issues for similar features/bugs
- Create an issue for features with detailed description
- Discuss approach in the issue before starting work

### 2. Development

- Create a feature branch from `main`
- Follow the coding standards and architecture guidelines
- Write comprehensive tests for your changes
- Update documentation as needed

### 3. Testing

- Run the full test suite: `pytest`
- Run performance tests: `pytest tests/performance/`
- Check code coverage: `pytest --cov=syinfo`
- Test on different Python versions using `tox`

### 4. Submission

- Create a pull request with clear description
- Link to related issues
- Ensure all CI checks pass
- Request review from maintainers

### 5. Review Process

- Address feedback promptly
- Update tests based on review comments
- Maintain clean commit history

## Release Process

### Versioning

We use semantic versioning (SemVer):
- **Major**: Breaking changes
- **Minor**: Features (backward compatible)
- **Patch**: Bug fixes

### Release Checklist

- [ ] Update version in `_version.py`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release PR
- [ ] Tag release after merge
- [ ] Publish to PyPI

## Getting Help

- **Documentation**: Check the `docs/` directory
- **Issues**: Search existing issues on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers at mohitrajput901@gmail.com

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

---

Thank you for contributing to SyInfo!