#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "==> Generating icons and header..."
python3 generate_assets.py

echo "==> Configuring CMake..."
cmake -B build -DCMAKE_BUILD_TYPE=Release

echo "==> Building iD Mixer..."
cmake --build build -j"$(nproc)"

echo "==> Packaging with CPack (DEB & TGZ)..."
(cd build && cpack)

cp build/id-mixer_*.deb ./ 2>/dev/null || true
cp build/id-mixer-*.tar.gz ./ 2>/dev/null || true
echo "==> Build complete! Generated packages:"
ls -1 id-mixer_*.deb id-mixer-*.tar.gz 2>/dev/null || true
