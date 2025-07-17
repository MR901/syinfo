Developer Documentation
=======================

This section contains documentation for developers who want to contribute to or extend SyInfo.

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide:

   ../internal/github_pages_setup
   ../internal/pypi_build

Contributing
------------

SyInfo is an open-source project and contributions are welcome! Here's how you can contribute:

**Getting Started**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

**Development Setup**

.. code-block:: bash

   git clone https://github.com/MR901/syinfo.git
   cd syinfo
   pip install -e .
   pip install -r requirements-dev.txt

**Running Tests**

.. code-block:: bash

   # Run all tests
   python -m pytest
   
   # Run with coverage
   python -m pytest --cov=syinfo
   
   # Run specific test categories
   python -m pytest tests/unit/
   python -m pytest tests/integration/

**Code Style**

SyInfo follows PEP 8 style guidelines. Use a code formatter like `black`:

.. code-block:: bash

   pip install black
   black syinfo/ tests/

**Documentation**

When adding new features, please update the documentation:

1. Update docstrings in your code
2. Add examples to the user guide
3. Update API documentation if needed
4. Test that documentation builds correctly

.. code-block:: bash

   cd docs
   make html
   make linkcheck

Project Structure
----------------

::

   syinfo/
   ├── syinfo/                 # Main package
   │   ├── core/              # Core system information modules
   │   ├── monitoring/        # Monitoring and analysis features
   │   ├── cli/               # Command-line interface
   │   ├── api/               # API modules
   │   └── utils/             # Utility functions
   ├── tests/                 # Test suite
   ├── docs/                  # Documentation
   ├── examples/              # Usage examples
   └── scripts/               # Build and deployment scripts

Architecture
-----------

SyInfo is designed with a modular architecture:

* **Core Module**: Legacy system information gathering
* **Monitoring Module**: Real-time monitoring and data collection
* **CLI Module**: Command-line interface
* **API Module**: Programmatic access to features
* **Utils Module**: Shared utilities and helpers

Release Process
--------------

1. Update version in `syinfo/_version.py`
2. Update changelog
3. Run full test suite
4. Build documentation
5. Create release tag
6. Deploy to PyPI

For more detailed information about the release process, see the internal documentation. 