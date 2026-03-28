#!/usr/bin/env bash
set -euo pipefail

VERSION="$(cat VERSION)"
ARTIFACT="dist/zspin-${VERSION}.zip"

mkdir -p dist
rm -f "$ARTIFACT"

zip -r "$ARTIFACT" README.md CHANGELOG.md VERSION pyproject.toml src docs scripts examples >/dev/null
sha256sum "$ARTIFACT" > "${ARTIFACT}.sha256"

echo "Built $ARTIFACT"
