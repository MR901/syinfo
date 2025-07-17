PyPI Build and Release Guide
============================

This document provides instructions for building and releasing SyInfo to PyPI.

Prerequisites
------------

* PyPI account with project access
* TestPyPI account for testing
* Build tools installed
* GPG key for signing (optional)

Setup
-----

1. **Install Build Tools**

   .. code-block:: bash

      pip install build twine wheel
      pip install setuptools --upgrade

2. **Configure PyPI Credentials**

   Create `~/.pypirc`:

   .. code-block:: ini

      [distutils]
      index-servers =
          pypi
          testpypi
      
      [pypi]
      repository = https://upload.pypi.org/legacy/
      username = your_username
      password = your_password
      
      [testpypi]
      repository = https://test.pypi.org/legacy/
      username = your_username
      password = your_password

3. **Update Version**

   Update version in `syinfo/_version.py`:

   .. code-block:: python

      __version__ = "1.0.0"

Build Process
------------

1. **Clean Previous Builds**

   .. code-block:: bash

      rm -rf build/ dist/ *.egg-info/
      python setup.py clean --all

2. **Build Distribution**

   .. code-block:: bash

      # Build source and wheel distributions
      python -m build
      
      # Or use setup.py (legacy)
      python setup.py sdist bdist_wheel

3. **Verify Build**

   .. code-block:: bash

      # Check distribution files
      ls -la dist/
      
      # Verify wheel contents
      python -m wheel unpack dist/syinfo-*.whl

Testing Release
--------------

1. **Upload to TestPyPI**

   .. code-block:: bash

      # Upload to test repository
      twine upload --repository testpypi dist/*
      
      # Or use specific files
      twine upload --repository testpypi dist/syinfo-1.0.0.tar.gz dist/syinfo-1.0.0-py3-none-any.whl

2. **Test Installation**

   .. code-block:: bash

      # Install from test repository
      pip install --index-url https://test.pypi.org/simple/ syinfo
      
      # Test functionality
      python -c "import syinfo; print(syinfo.__version__)"
      syinfo --version

3. **Verify Documentation**

   * Check that all features work correctly
   * Test both basic and monitoring installations
   * Verify CLI commands function properly

Production Release
-----------------

1. **Final Verification**

   .. code-block:: bash

      # Check distribution files
      twine check dist/*
      
      # Verify package metadata
      python setup.py check --metadata --strict

2. **Upload to PyPI**

   .. code-block:: bash

      # Upload to production PyPI
      twine upload dist/*
      
      # Or upload specific files
      twine upload dist/syinfo-1.0.0.tar.gz dist/syinfo-1.0.0-py3-none-any.whl

3. **Verify Release**

   .. code-block:: bash

      # Install from PyPI
      pip install syinfo
      
      # Test installation
      python -c "import syinfo; print(syinfo.__version__)"
      syinfo --version

Automated Release
----------------

Create `.github/workflows/release.yml`:

.. code-block:: yaml

   name: Release to PyPI
   
   on:
     release:
       types: [published]
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v3
       
       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.9'
       
       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install build twine wheel
       
       - name: Build package
         run: python -m build
       
       - name: Publish to PyPI
         env:
           TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
           TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
         run: twine upload dist/*

Version Management
-----------------

1. **Semantic Versioning**

   Follow semantic versioning (MAJOR.MINOR.PATCH):
   * MAJOR: Breaking changes
   * MINOR: New features, backward compatible
   * PATCH: Bug fixes, backward compatible

2. **Version Update Process**

   .. code-block:: bash

      # Update version in _version.py
      sed -i 's/__version__ = ".*"/__version__ = "1.0.1"/' syinfo/_version.py
      
      # Update setup.py if needed
      sed -i 's/version=".*"/version="1.0.1"/' setup.py
      
      # Commit version change
      git add syinfo/_version.py setup.py
      git commit -m "Bump version to 1.0.1"
      git tag v1.0.1
      git push origin main --tags

3. **Changelog Management**

   * Update CHANGELOG.md with new version
   * Include all changes since last release
   * Follow conventional changelog format

Package Configuration
--------------------

1. **setup.py Configuration**

   Ensure `setup.py` includes:

   .. code-block:: python

      setup(
          name="syinfo",
          version=__version__,
          description="System Information and Monitoring Tool",
          long_description=long_description,
          long_description_content_type="text/markdown",
          author="MR901",
          author_email="mohitrajput901@gmail.com",
          url="https://github.com/MR901/syinfo",
          packages=find_packages(),
          classifiers=[
              "Development Status :: 4 - Beta",
              "Intended Audience :: Developers",
              "Intended Audience :: System Administrators",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3.7",
              "Programming Language :: Python :: 3.8",
              "Programming Language :: Python :: 3.9",
              "Programming Language :: Python :: 3.10",
              "Programming Language :: Python :: 3.11",
              "Topic :: System :: Monitoring",
              "Topic :: System :: Systems Administration",
          ],
          python_requires=">=3.7",
          install_requires=[
              # Core dependencies
          ],
          extras_require={
              "monitoring": [
                  "psutil>=5.8.0",
                  "matplotlib>=3.3.0",
                  "pandas>=1.3.0",
                  "pyyaml>=5.4.0",
              ],
              "dev": [
                  "pytest>=6.0.0",
                  "pytest-cov>=2.10.0",
                  "black>=21.0.0",
                  "flake8>=3.8.0",
                  "mypy>=0.800",
                  "sphinx>=4.0.0",
                  "sphinx-rtd-theme>=1.0.0",
              ],
          },
          entry_points={
              "console_scripts": [
                  "syinfo=syinfo.__main__:main",
              ],
          },
      )

2. **MANIFEST.in**

   Create `MANIFEST.in` to include additional files:

   .. code-block:: text

      include README.rst
      include LICENSE
      include CHANGELOG.md
      include requirements.txt
      include pytest.ini
      recursive-include syinfo *.py
      recursive-exclude * __pycache__
      recursive-exclude * *.py[co]

3. **pyproject.toml (Optional)**

   For modern Python packaging:

   .. code-block:: toml

      [build-system]
      requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
      build-backend = "setuptools.build_meta"
      
      [project]
      name = "syinfo"
      dynamic = ["version"]
      description = "System Information and Monitoring Tool"
      readme = "README.rst"
      license = {text = "MIT"}
      authors = [
          {name = "MR901", email = "mohitrajput901@gmail.com"}
      ]
      classifiers = [
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
      ]
      requires-python = ">=3.7"
      dependencies = []
      
      [project.optional-dependencies]
      monitoring = [
          "psutil>=5.8.0",
          "matplotlib>=3.3.0",
          "pandas>=1.3.0",
          "pyyaml>=5.4.0",
      ]
      dev = [
          "pytest>=6.0.0",
          "pytest-cov>=2.10.0",
          "black>=21.0.0",
          "flake8>=3.8.0",
          "mypy>=0.800",
          "sphinx>=4.0.0",
          "sphinx-rtd-theme>=1.0.0",
      ]
      
      [project.scripts]
      syinfo = "syinfo.__main__:main"
      
      [project.urls]
      Homepage = "https://github.com/MR901/syinfo"
      Documentation = "https://mr901.github.io/syinfo/"
      Repository = "https://github.com/MR901/syinfo"
      "Bug Tracker" = "https://github.com/MR901/syinfo/issues"
      
      [tool.setuptools_scm]
      write_to = "syinfo/_version.py"

Quality Assurance
----------------

1. **Pre-release Testing**

   .. code-block:: bash

      # Run all tests
      pytest tests/
      
      # Check code quality
      flake8 syinfo/
      black --check syinfo/
      mypy syinfo/
      
      # Test installation
      pip install -e .
      python -c "import syinfo; print(syinfo.__version__)"

2. **Distribution Testing**

   .. code-block:: bash

      # Test build
      python -m build
      
      # Test installation from wheel
      pip install dist/syinfo-*.whl
      
      # Test functionality
      syinfo --version
      syinfo --help

3. **Documentation Testing**

   .. code-block:: bash

      # Build documentation
      cd docs
      make html
      
      # Check for broken links
      make linkcheck

Troubleshooting
--------------

**Build Failures**

* Check Python version compatibility
* Verify all dependencies are available
* Check for syntax errors in source code

**Upload Failures**

* Verify PyPI credentials
* Check package name availability
* Ensure version is unique

**Installation Issues**

* Test on clean environment
* Check dependency conflicts
* Verify entry points are correct

**Documentation Issues**

* Check Sphinx configuration
* Verify theme installation
* Test documentation build locally

Security Considerations
----------------------

* Use API tokens instead of passwords
* Enable two-factor authentication
* Regularly rotate credentials
* Sign packages with GPG (optional)

Monitoring and Maintenance
-------------------------

* Monitor PyPI download statistics
* Track issue reports and bug reports
* Maintain compatibility with Python versions
* Regular dependency updates

Next Steps
----------

1. **Set up automated releases** with GitHub Actions
2. **Configure monitoring** for PyPI statistics
3. **Set up security scanning** for dependencies
4. **Create release templates** for consistent releases
5. **Document release process** for team members 