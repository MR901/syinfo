import os
from setuptools import setup, find_packages
# from Cython.Build import cythonize

# Avoids IDE errors, but actual version is read from version.py
__version__ = None
with open("syinfo/_version.py") as f:
    exec(f.read())

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

# Core dependencies (required for basic functionality)
install_requires = [
    # "tabulate",
    "tabulate==0.9.0",
    "getmac==0.9.4",
    "GPUtil==1.4.0",
    "PyYAML==6.0.1",
    "psutil==5.9.5",
    "scapy==2.5.0",
    "py-cpuinfo==9.0.0"
]

# Optional dependencies for monitoring features
extras_require = {
    'monitoring': [
        'pandas>=1.3.0',
        'matplotlib>=3.5.0',
        'seaborn>=0.11.0',
        'numpy>=1.21.0',
    ],
    'full': [
        'pandas>=1.3.0',
        'matplotlib>=3.5.0',
        'seaborn>=0.11.0',
        'numpy>=1.21.0',
        'paramiko>=2.8.0',  # For remote data collection
        'requests>=2.25.0',  # For API calls
    ],
    'dev': [
        'pytest>=6.0.0',
        'pytest-cov>=2.10.0',
        'black>=21.0.0',
        'flake8>=3.8.0',
        'mypy>=0.800',
    ]
}

setup(
    name="syinfo",
    version=__version__,

    description="A Python package to get device and network information with advanced monitoring capabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Mohit Rajput",
    author_email="mohitrajput901@gmail.com",
    maintainer="Mohit Rajput",
    maintainer_email="mohitrajput901@gmail.com",

    url="https://github.com/MR901/syinfo",
    keywords=["system", "monitoring", "information", "network", "hardware", "linux"],

    # license="Apache 2.0",

    zip_safe=False,
    install_requires=install_requires,
    extras_require=extras_require,

    packages=find_packages(),
    # ext_modules=cythonize("syinfo/*.pyx"),  #include_path=[...]), # ValueError: 'syinfo/*.pyx' doesn't match any files
    # Check
    # - https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html
    # - https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#multiple-cython-files-in-a-package

    include_package_data=True,
    package_data={
        'syinfo': ['config/*.yaml'],
    },

    classifiers=[
        # "Development Status :: 1 - Alpha",
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        # 'License :: OSI Approved :: Apache Software License',
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: Linux",
    ],
    platforms=["Linux"],
    python_requires=">=3.8",

    # scripts=[
    #     "syinfo/constants.py",
    #     "syinfo/device_info.py",
    #     "syinfo/__init__.py",
    #     "syinfo/__main__.py",
    #     "syinfo/network_info.py",
    #     "syinfo/search_network.py",
    #     "syinfo/syinfo.py",
    #     "syinfo/utils.py",
    #     "syinfo/_version.py",
    # ],
    py_modules=["syinfo"],
    # package_dir={"": "syinfo"},

    entry_points={
        "console_scripts": [
            "syinfo=syinfo.__main__:main",
            # "syinfo=sys_info:main",
        ],
    },

    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/MR901/syinfo/issues',
        'Source': 'https://github.com/MR901/syinfo',
        'Documentation': 'https://github.com/MR901/syinfo#readme',
    },

)
