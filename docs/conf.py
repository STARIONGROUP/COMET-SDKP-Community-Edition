from __future__ import annotations

import os

import sys

from datetime import datetime

# -- Path setup --------------------------------------------------------------

sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------

project = "COMET SDKP"

author = "STARION GROUP"

copyright = f"{datetime.now().year}, {author}"

release = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
]

autosummary_generate = True

autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_typehints_format = "short"

napoleon_google_docstring = True
napoleon_numpy_docstring = False

# MyST

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
    "attrs_inline",
    "fieldlist",
]

autodoc_mock_imports = ["ctypes"]

# -- HTML output -------------------------------------------------------------

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "navigation_depth": 3,
    "show_prev_next": False,
    "show_toc_level": 2,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition",
            "icon": "fab fa-github",
        }
    ],
}

html_static_path = ["_static"]
