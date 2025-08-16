#! /usr/bin/env sh

cd src
uv run marimo edit --headless --host 0.0.0.0 --sandbox --no-token $(tv files)
