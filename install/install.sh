#!/bin/bash

# Horizons Event Checker - One-Click Install and Run
# For macOS/Linux

echo "=================================="
echo "  Horizons Event Checker Setup"
echo "=================================="
echo ""

GITHUB_REPO="QAISALNAJJAR/horizons-event-fix"

# Detect platform
if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
    if [[ $(uname -m) == "arm64" ]]; then
        FILE="horizons-checker-macos-arm"
    else
        FILE="horizons-checker-macos-intel"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
    FILE="horizons-checker-linux"
else
    PLATFORM="macos"
    FILE="horizons-checker-macos-intel"
fi

echo "Detected platform: $PLATFORM"

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "Downloading latest release..."

# Download pre-built binary from GitHub Releases
DOWNLOAD_URL="https://github.com/$GITHUB_REPO/releases/latest/download/$FILE"

if curl -sL "$DOWNLOAD_URL" -o horizons-checker 2>/dev/null; then
    chmod +x horizons-checker
    echo "✅ Downloaded pre-built binary!"
    echo ""
    echo "=================================="
    echo "  Starting Horizons Event Checker"
    echo "=================================="
    echo ""
    ./horizons-checker
else
    echo ""
    echo "=============================================================="
    echo "  PRE-BUILT BINARY NOT AVAILABLE"
    echo "=============================================================="
    echo ""
    echo "  Please download manually from:"
    echo "  https://github.com/$GITHUB_REPO/releases"
    echo ""
    echo "  Or build from source:"
    echo "  1. Install Python from https://www.python.org/downloads/"
    echo "  2. Run: pip install requests browser-cookie3"
    echo "  3. Run: python main.py"
    echo ""
    echo "=============================================================="
fi

# Cleanup
cd -
rm -rf "$TEMP_DIR"
