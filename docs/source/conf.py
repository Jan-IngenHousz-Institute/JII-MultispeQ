# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import toml
from jii_multispeq import __version__

sys.path.insert(0, os.path.abspath('../../src/jii_multispeq'))

config = toml.load("../../pyproject.toml")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = config["tool"]["sphinx"]["project"]
copyright = "%Y - "  + config["tool"]["sphinx"]["copyright"]
author = config["tool"]["sphinx"]["author"]
version = __version__
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  "sphinx.ext.autodoc",
  'sphinx.ext.autosummary',
  'sphinx.ext.duration',
  "sphinx.ext.napoleon",
  "sphinx.ext.viewcode",
  "myst_parser",
  # "nbsphinx" # Implement Jupyter notebooks later
]

templates_path = ["_templates"]
exclude_patterns = ["Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "classic"
html_theme = "furo"
# html_theme = "sphinx_rtd_theme"
# html_permalinks_icon = '<span>#</span>'
# html_theme = 'sphinxawesome_theme'
html_title = "JII - MultispeQ"
html_short_title = "JII MQ"
html_logo = "_static/images/jan-ingenhousz-institute-logo.webp"
html_favicon = "_static/images/favicon.png"
html_theme_options = {
    # 'logo_only': True, # Not available for furo
    # 'display_version': False, # Not available for furo
}

html_static_path = ["_static"]
source_suffix = {
  ".rst": "restructuredtext", 
  ".md": "markdown"
}

# -- Options for autodoc -------------------------------------------------

autodoc_member_order = "bysource"
autodoc_special_members = "__init__"
autodoc_undoc_members = True
autodoc_exclude_members = "__weakref__"

add_module_names = False
