#!/bin/bash
set -e


echo "Running Tests!"
echo "================"

python -m pip install --upgrade pip
if [ -f pyproject.toml ]; then
  python -m pip install .[dev]
elif [ -f requirements_ci.txt ]; then
  python -m pip install -r requirements_ci.txt
else
  python -m pip install pytest flake8 pytest-cov
fi

flake8 . > flakereport.txt
pytest --disable-warnings

echo "Done!"