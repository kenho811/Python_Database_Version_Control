# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

from distutils.util import strtobool

import os
import sys

# For src/dvc folder
sys.path.insert(0, os.path.abspath('../src'))

# For tests/ folder
sys.path.insert(1, os.path.abspath('..'))

from dvc.version import __version__

KEY__ISLOCAL = "ISLOCAL"
is_local = bool(os.getenv(KEY__ISLOCAL))
print(f"***********Running conf.py locally: {is_local}***************************")

# -- Project information -----------------------------------------------------

project = 'Database Version Control'
copyright = '2022, Ken Ho'
author = 'Ken Ho'

# The full version, including alpha/beta/rc tags
release = __version__

html_logo = "_static/img/logo/app_logo_black.png"

html_theme_options = {
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#336790",  # "blue"
        "color-brand-content": "#336790",
    },
    "dark_css_variables": {
        "color-brand-primary": "#E5B62F",  # "yellow"
        "color-brand-content": "#E5B62F",
    },
}

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # Create diagrams with graph-viz
    'sphinx.ext.graphviz',

    # create .rst files for source documnetation
    'sphinx.ext.autodoc',

    # Create [source] for method signature
    'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
html_static_path = [
    # Copy everything in the below folders to the _static folder
    '_static',
    'dynamic/pytest']

html_css_files = [
    'css/custom.css',
]

# -- Options for sphinx.ext.viewcode -------------------------------------------
# See: https://www.sphinx-doc.org/es/master/usage/extensions/viewcode.html

# If this is True, viewcode extension will emit viewcode-follow-imported event to resolve the name of
# the module by other extensions. The default is True.
viewcode_follow_imported_members = True

## Github Action - Readthedocs Integration
# The name of your GitHub repository
if not is_local:
    print(f"NOTE: To generate sphinx doc locally, do `{KEY__ISLOCAL}=1 make clean html")
    extensions.append('rtds_action')

    rtds_action_github_repo = "kenho811/Python_Database_Version_Control"

    # The path where the artifact should be extracted
    # Note: this is relative to the conf.py file!
    rtds_action_path = "dynamic"

    # The "prefix" used in the `upload-artifact` step of the action
    rtds_action_artifact_prefix = "dynamic-asset-"

    # A GitHub personal access token is required, more info below
    rtds_action_github_token = os.environ["GITHUB_TOKEN"]

    # Whether or not to raise an error on Read the Docs if the
    # artifact containing the notebooks can't be downloaded (optional)
    rtds_action_error_if_missing = True
