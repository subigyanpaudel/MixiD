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

echo "==> Packaging .deb with CPack..."
(cd build && cpack -G DEB)

cp build/id-mixer_*.deb ./
echo "==> Build complete! Package generated at: $(ls -1 id-mixer_*.deb | head -n 1)"
