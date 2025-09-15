#! /usr/bin/env sh

NOTEBOOK_DIR="notebooks"
uv run marimo edit --headless --host 0.0.0.0 --sandbox --no-token "$NOTEBOOK_DIR/$(tv files $NOTEBOOK_DIR)"
