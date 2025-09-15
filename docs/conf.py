import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath('..'))

project = 'SyInfo'
author = 'Mohit Rajput'
current_year = datetime.now().year
copyright = f'{current_year}, {author}'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinxcontrib.mermaid',
]

templates_path = ['_templates']
exclude_patterns = ['_build']

html_theme = 'alabaster'
html_static_path = ['_static']
