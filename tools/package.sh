#!/usr/bin/env bash
# Builds dist/Sakha-Keyboard.zip, the release download with the double-click installers.
set -euo pipefail
cd "$(dirname "$0")/.."

stage="dist/Sakha Keyboard"
rm -rf dist && mkdir -p "$stage"
cp -R Sakha.bundle install.sh packaging/*.command "$stage/"
cp packaging/README.txt "$stage/Read Me.txt"
chmod +x "$stage/install.sh" "$stage"/*.command
(cd dist && zip -qrX Sakha-Keyboard.zip "Sakha Keyboard")
echo "dist/Sakha-Keyboard.zip"
