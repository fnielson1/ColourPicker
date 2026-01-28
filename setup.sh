#!/usr/bin/env bash

# Exit on error
set -e

PIP="pip"

usage() {
  echo "Usage: $0 [-p <pip>] [-h]"
  echo ""
  echo "Options:"
  echo "  -p, --pip <pip>   Specify pip executable to use (default: pip)"
  echo "  -h, --help        Show this help message"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--pip)
      PIP="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      break
      ;;
  esac
done

# Check for pyproject.toml
if [ ! -f pyproject.toml ]; then
  echo "pyproject.toml not found in current directory."
  exit 1
fi

# Check if running inside a venv and if it has access to system site packages
if python3 -c "import sys; print(getattr(sys, 'real_prefix', None) or sys.prefix != getattr(sys, 'base_prefix', sys.prefix))" | grep -q "True"; then
  # In a venv, check for system site packages
  if ! python3 -c "import site; print(any('site-packages' in p and 'local' not in p for p in site.getsitepackages()))" | grep -q "True"; then
    echo "WARNING: Your virtual environment does not have access to system site packages."
    echo "         Please recreate it with:"
    echo "             python3 -m venv --system-site-packages .venv"
    echo "         Otherwise, system packages like 'gi' will not be available."
  fi
fi

# Extract Python dependencies from pyproject.toml (PEP 621 or poetry format)
DEPS=$(awk '/^\[project\]/{flag=1} flag && /^dependencies = \[/{getline; while($0 !~ /\]/){gsub(/[",]/,""); print $1; getline}}' pyproject.toml)

# Extract system dependencies from [tool.system-dependencies] section
SYS_DEPS=$(awk '/^\[tool.system-dependencies\]/{flag=1; next} /^\[.*\]/{flag=0} flag && NF {gsub(/[",\[\]]/, ""); if ($0 !~ /^system-dependencies/) print}' pyproject.toml | tr '\n' ' ')

if [ -z "$DEPS" ]; then
  echo "No Python dependencies found in pyproject.toml."
else
  echo "Installing Python dependencies:"
  echo "$DEPS"
  echo ""
  echo "---"
  for dep in $DEPS; do
    echo "Running: $PIP install $dep"
    "$PIP" install "$dep"
  done
fi

if [ -n "$SYS_DEPS" ]; then
  echo ""
  echo "Installing system dependencies with apt-get (requires sudo):"
  echo "$SYS_DEPS"
  echo ""
  echo "---"
  sudo apt-get update
  sudo apt-get install -y $SYS_DEPS
fi
