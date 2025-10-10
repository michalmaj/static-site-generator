#!/usr/bin/env bash
set -euo pipefail

# Twoje repo na GitHub to michalmaj/static-site-generator,
# więc basepath musi być /static-site-generator/

echo "[build] Generating site for GitHub Pages..."
python3 src/main.py "/static-site-generator/"

echo "[build] Site ready for deployment!"
echo "[build] You can now push to GitHub Pages:"
echo "https://michalmaj.github.io/static-site-generator/"