#! /usr/bin/env sh

if [ $# -eq 0 ]; then
  NOTEBOOK_DIR="notebooks"
  uv run marimo edit --headless --host 0.0.0.0 --sandbox --no-token "$NOTEBOOK_DIR/$(tv files $NOTEBOOK_DIR)"
else
  uv run marimo edit --headless --host 0.0.0.0 --sandbox --no-token "$1"
fi
