# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LLAMATOR'
copyright = '2023, LLaMasters'
author = 'deepsense.ai'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",# support for google style docstrings
    "sphinx.ext.autodoc", # auto* are for automatic code docs generation
    "sphinx.ext.autosummary", # as above
    "sphinx.ext.intersphinx", # allows to cross reference other sphinx documentations
    "sphinx.ext.autosectionlabel", # each doc section gets automatic reference generated
    "myst_parser", # adds support for Markdown
    "sphinxcontrib.mermaid", # allows to use Mermaid diagrams
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

autosectionlabel_prefix_document = True

# Mapping to link other documentations
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "numpy": ("https://numpy.org/doc/stable", None),
}


# Configuration for Napoleon extension
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

add_module_names = False
autodoc_typehints = 'both'

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# workaround for sphinx material issue with empty left sidebar
# See: https://github.com/bashtage/sphinx-material/issues/30
# uncomment below lines if you use: html_theme = "sphinx_material"
# html_sidebars = {
#    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
# }
