#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "==> Generating icons and header..."
python3 generate_assets.py

echo "==> Configuring CMake..."
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr

echo "==> Building iD Mixer..."
cmake --build build -j"$(nproc)"

echo "==> Cleaning previous packages..."
rm -f build/*.deb build/*.tar.gz *.deb *.tar.gz

echo "==> Packaging with CPack (DEB & TGZ)..."
(cd build && cpack)

cp build/*.deb ./ 2>/dev/null || true
cp build/*.tar.gz ./ 2>/dev/null || true
echo "==> Build complete! Generated packages:"
ls -1 mixid_*.deb mixid-*.tar.gz 2>/dev/null || true
