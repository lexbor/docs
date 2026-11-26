# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "lexbor"
copyright = "2024-2026, Alexander Borisov"
author = "Alexander Borisov"
html_title = "lexbor docs"


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinx_copybutton"]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
myst_heading_anchors = 3

# -- Custom CSS files --------------------------------------------------------
html_css_files = [
    "css/variables.css",
    "css/typography.css",
    "css/custom.css",
]

# -- Furo theme --------------------------------------------------------------
# https://pradyunsg.me/furo/customisation/

html_theme_options = {
    "top_of_page_buttons": ["view", "edit"],
    "source_repository": "https://github.com/lexbor/docs/",
    "source_branch": "main",
    "source_directory": "source/",
    "light_css_variables": {
        "color-brand-primary": "#802022",
        "color-brand-content": "#0366d6",
        "color-foreground-primary": "#313841",
        "color-foreground-secondary": "#4d5e6d",
        "color-background-primary": "#ffffff",
        "color-background-secondary": "#f1f1f1",
        "font-stack": "'Open Sans', arial, sans-serif",
        "font-stack--monospace": "'Source Code Pro', monospace",
        "color-sidebar-link-text--top-level": "var(--color-foreground-secondary)",
    },
    "dark_css_variables": {
        "color-brand-primary": "#a84044",
        "color-brand-content": "#4da3ff",
        "color-foreground-primary": "#e8eaed",
        "color-foreground-secondary": "#aab4be",
        "color-background-primary": "#1a1d21",
        "color-background-secondary": "#22262c",
        "color-background-border": "#363b44",
        "font-stack": "'Open Sans', arial, sans-serif",
        "font-stack--monospace": "'Source Code Pro', monospace",
        "color-sidebar-link-text--top-level": "var(--color-foreground-secondary)",
    },
}
