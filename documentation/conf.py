# Configuration file for the Sphinx documentation builder.
#
# SPDX-License-Identifier: CC-BY-2.0-UK
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import datetime

# -- Project information -----------------------------------------------------
project = 'The Yocto Project'
copyright = '2010-%s, The Linux Foundation' % datetime.datetime.now().year
author = 'The Linux Foundation'


# -- General configuration ---------------------------------------------------

# to load local extension from the folder 'sphinx'
sys.path.insert(0, os.path.abspath('sphinx'))

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.extlinks',
    'yocto-vars'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# master document name. The default changed from contents to index. so better
# set it ourselves.
master_doc = 'index'

# create substitution for project configuration variables
rst_prolog = """
.. |project_name| replace:: %s
.. |copyright| replace:: %s
.. |author| replace:: %s
""" % (project, copyright, author)

# external links and substitutions
extlinks = {
    'yocto_home': ('https://yoctoproject.org%s', None),
    'yocto_wiki': ('https://wiki.yoctoproject.org%s', None),
    'yocto_dl': ('https://downloads.yoctoproject.org%s', None),
    'yocto_lists': ('https://lists.yoctoproject.org%s', None),
    'yocto_bugs': ('https://bugzilla.yoctoproject.org%s', None),
    'yocto_ab': ('https://autobuilder.yoctoproject.org%s', None),
    'yocto_git': ('https://git.yoctoproject.org%s', None),
    'oe_home': ('https://www.openembedded.org%s', None),
    'oe_lists': ('https://lists.openembedded.org%s', None),
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_logo = 'sphinx-static/YoctoProject_Logo_RGB.jpg'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['sphinx-static']

html_context = {
    'css_files': [
        '_static/theme_overrides.css',
    ],
}
