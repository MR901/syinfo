import os
from setuptools import setup, find_packages

# Avoids IDE errors, but actual version is read from version.py
__version__ = None
with open('sys_info/_version.py') as f:
    exec(f.read())

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

install_requires = [
    # ipywidgets, tabulate, 'py-cpuinfo==5.0.0',
]

setup(
    name='sys_info',
    version=__version__,

    description="A Python package to get device and network information.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Mohit Rajput",
    author_email="mohitrajput901@gmail.com",
    maintainer="Mohit Rajput",
    maintainer_email="mohitrajput901@gmail.com",

    url='https://github.com/MR901/sys_info',
    keywords=[],

    # license="Apache 2.0",

    zip_safe=False,
    install_requires=install_requires,

    packages=find_packages(),

    include_package_data=True,

    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.6',
)
