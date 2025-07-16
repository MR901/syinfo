Installation Guide
=================

This guide covers different installation methods for SyInfo, from basic usage to full monitoring capabilities.

Prerequisites
------------

* **Python**: 3.7 or higher
* **Operating System**: Linux, macOS, Windows
* **Package Manager**: pip (recommended) or conda

Basic Installation
-----------------

For core system information features only:

.. code-block:: bash

   pip install syinfo

This installation includes:
* Device information gathering
* Network information scanning
* System information collection
* Command-line interface
* Python library access

Full Installation
----------------

For complete monitoring and analysis features:

.. code-block:: bash

   pip install syinfo[monitoring]

This installation includes everything from basic installation plus:
* Real-time system monitoring
* Process monitoring and analysis
* Data collection and storage
* Trend analysis and anomaly detection
* Data visualization and charts
* Automated scheduling with cron jobs
* Advanced API access

Development Installation
-----------------------

For contributing to the project:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/MR901/syinfo.git
   cd syinfo
   
   # Install in development mode
   pip install -e .
   
   # Install development dependencies
   pip install -e ".[dev]"

Development dependencies include:
* Testing frameworks (pytest, pytest-cov)
* Documentation tools (Sphinx)
* Code quality tools (flake8, black)
* Type checking (mypy)

Alternative Installation Methods
-------------------------------

**Using conda:**

.. code-block:: bash

   conda install -c conda-forge syinfo

**From source (latest development version):**

.. code-block:: bash

   pip install git+https://github.com/MR901/syinfo.git

**Specific version:**

.. code-block:: bash

   pip install syinfo==1.0.0

Dependencies
-----------

Core Dependencies
~~~~~~~~~~~~~~~~

* **No external dependencies** for basic functionality
* Uses only Python standard library

Monitoring Dependencies
~~~~~~~~~~~~~~~~~~~~~~

When installing with monitoring features, the following packages are automatically installed:

* **psutil**: System and process utilities
* **matplotlib**: Data visualization
* **pandas**: Data analysis and manipulation
* **pyyaml**: Configuration file handling

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~

* **numpy**: Enhanced numerical operations
* **scipy**: Advanced statistical analysis
* **seaborn**: Enhanced plotting capabilities

Verifying Installation
---------------------

**Check installation:**

.. code-block:: bash

   python -c "import syinfo; print(syinfo.__version__)"

**Test basic functionality:**

.. code-block:: bash

   syinfo --version
   syinfo --help

**Test monitoring features (if installed):**

.. code-block:: bash

   python -c "from syinfo import MONITORING_AVAILABLE; print(f'Monitoring available: {MONITORING_AVAILABLE}')"

Upgrading
---------

**Upgrade to latest version:**

.. code-block:: bash

   pip install --upgrade syinfo

**Upgrade with monitoring features:**

.. code-block:: bash

   pip install --upgrade syinfo[monitoring]

**Upgrade from basic to full installation:**

.. code-block:: bash

   pip install syinfo[monitoring]

Uninstalling
-----------

**Remove SyInfo:**

.. code-block:: bash

   pip uninstall syinfo

**Remove with dependencies:**

.. code-block:: bash

   pip uninstall syinfo psutil matplotlib pandas pyyaml

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

**Import Error for monitoring features:**

.. code-block:: text

   ImportError: Monitoring features not available. Install required dependencies.

**Solution:** Install with monitoring extras:

.. code-block:: bash

   pip install syinfo[monitoring]

**Permission errors on Linux/macOS:**

.. code-block:: text

   PermissionError: [Errno 13] Permission denied

**Solution:** Use sudo or install for current user:

.. code-block:: bash

   pip install --user syinfo

**Missing dependencies on Windows:**

.. code-block:: text

   Microsoft Visual C++ 14.0 is required

**Solution:** Install Visual Studio Build Tools or use pre-compiled wheels:

.. code-block:: bash

   pip install --only-binary=all syinfo

**Python version compatibility:**

.. code-block:: text

   Python 3.7+ is required

**Solution:** Upgrade Python to 3.7 or higher

Getting Help
-----------

If you encounter issues during installation:

* **Check the troubleshooting section above**
* **Review system requirements**
* **Search existing issues**: https://github.com/MR901/syinfo/issues
* **Create a new issue**: https://github.com/MR901/syinfo/issues/new
* **Contact support**: mohitrajput901@gmail.com

Next Steps
----------

After successful installation:

1. **Read the User Guide**: :doc:`user_guide/index`
2. **Explore the API**: :doc:`api/index`
3. **Try the CLI**: :doc:`cli/index`
4. **Run examples**: :doc:`examples/index` 