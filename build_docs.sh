#!/bin/bash

# Force Sphinx to rebuild documentation - otherwise it generates incosistencies.
rm -rf public/ docs/_build

# Exit on error for the next commands
set -e -x

# Activate venv for licenses and also it simplifies sphinx code documentation generation.
. venv/bin/activate

# Generate a table with all installed libraries, licenses etc
pip-licenses --from=mixed --format rst --with-urls --with-description --output-file=docs/licenses_table.rst

# Build sphinx docs to public/ directory
sphinx-build -d docs/_build/doctrees docs/ public/
