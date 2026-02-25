import os
import sys
# Assumes your project's source code is one level up from the docs folder
sys.path.insert(0, os.path.abspath('../')) 

# Also, ensure 'sphinx_rtd_theme' (or your chosen theme) is set as the html theme
# html_theme = 'sphinx_rtd_theme'



# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'threefive'
copyright = '2026, Superkabbuki'
author = 'Superkabuki'
release = '3.0.77'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',]

templates_path = ['_templates']
exclude_patterns = []

