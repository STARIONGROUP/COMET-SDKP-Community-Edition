"""
Sphinx configuration for COMET SDKP Community Edition documentation
"""

from __future__ import annotations

import os
import sys
from datetime import datetime

# -- Path setup --------------------------------------------------------------

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -- Project information -----------------------------------------------------

project = "COMET SDKP Community Edition"

author = "STARION GROUP"

copyright = f"{datetime.now().year}, {author}"

release = "0.1.0"
version = "0.1"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]

# Template path
templates_path = ["_templates"]

# Exclude patterns
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    "venv",
]

# MyST (Markdown) configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

# HTML output configuration
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "show_prev_next": True,
    "github_url": "https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition",
    "navbar_end": ["navbar-icon-links"],
    "footer_items": ["copyright"],
}

html_static_path = []
html_css_files = []

# Autodoc configuration
autodoc_typehints = "description"

# MyST parser configuration
myst_heading_anchors = 3
myst_html_meta = {
    "description": "Python SDK for CDP4 Integration",
    "keywords": "CDP4, COMET, SDK, Python",
}
