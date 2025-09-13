Building and Publishing
=======================

Build
-----

.. code-block:: bash

   # Ensure build and twine are available
   pip install build twine

   # Build sdist and wheel
   python -m build

   # Verify artifacts
   python -m twine check dist/*

TestPyPI
--------

.. code-block:: bash

   # Upload to TestPyPI (username is __token__)
   python -m twine upload --repository testpypi dist/*

   # Install from TestPyPI for verification
   pip install -i https://test.pypi.org/simple/ syinfo \
       --extra-index-url https://pypi.org/simple

   # With extras
   pip install -i https://test.pypi.org/simple/ 'syinfo[full]' \
       --extra-index-url https://pypi.org/simple

PyPI
----

.. code-block:: bash

   # Upload to PyPI (username is __token__, password is a pypi- token)
   python -m twine upload dist/*

Optional: ~/.pypirc
-------------------

.. code-block:: ini

   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
     repository: https://upload.pypi.org/legacy/
     username: __token__
     password: pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

   [testpypi]
     repository: https://test.pypi.org/legacy/
     username: __token__
     password: pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Notes
-----

- Use PEP 517 builds (``python -m build``) instead of legacy ``setup.py sdist``.
- Validate Trove classifiers and ``readme`` in ``pyproject.toml``.
- Run tests and linters prior to publishing.
