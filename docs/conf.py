# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LLAMATOR'
copyright = '2024, LLaMasters'
author = 'Neronov Roman, Nizamov Timur, Fazlyev Albert, Ivanov Nikita, Iogan Maksim'

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
    "sphinx.ext.extlinks",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for TODOs -------------------------------------------------------
#

todo_include_todos = False

# -- Options for Markdown files ----------------------------------------------
#

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
myst_heading_anchors = 3

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
# Set link name generated in the top bar.
html_title = "LLAMATOR"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#1d3d64",  # Темно-синий для основного цвета
        "color-brand-content": "#18578d",  # Темно-синий для контента
        "color-admonition-background": "#f0f8ff",  # Светлый фон для предупреждений (note)
        "color-admonition-title-background": "#007acc",  # Цвет фона заголовка note
        "color-admonition-border": "#007acc",  # Цвет границы для note
        "color-admonition-title": "#007acc",  # Цвет заголовка note
    },
    "dark_css_variables": {
        "color-brand-primary": "#d8673e",
        "color-brand-content": "#f99470",
        "color-admonition-background": "#333333",  # Темный фон для note в тёмной теме
        "color-admonition-title-background": "#d8673e",  # Цвет фона заголовка note
        "color-admonition-border": "#d8673e",  # Цвет границы для note
        "color-admonition-title": "#f99470",  # Цвет заголовка note
    },
    "sidebar_hide_name": False,
    "footer_icons": [
            {
                "name": "GitHub",
                "url": "https://github.com/RomiconEZ/llamator",
                "html": """
                    <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                    </svg>
                """,
                "class": "",
            },
        ],
    "source_repository": "https://github.com/RomiconEZ/llamator",
    "source_branch": "main",
    "source_directory": "src/",
}

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

pygments_style = "sphinx"
pygments_dark_style = "monokai"

# workaround for sphinx material issue with empty left sidebar
# See: https://github.com/bashtage/sphinx-material/issues/30
# uncomment below lines if you use: html_theme = "sphinx_material"
# html_sidebars = {
#    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
# }
