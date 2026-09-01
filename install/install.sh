#!/bin/bash

# Horizons Event Checker - One-Click Install & Run
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
        PLATFORM="macos-arm"
    else
        PLATFORM="macos-intel"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
else
    PLATFORM="macos"
fi

echo "Detected platform: $PLATFORM"

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "Downloading latest release..."

# Try to download from GitHub Releases first
RELEASE_URL="https://github.com/$GITHUB_REPO/releases/latest/download/horizons-checker-$PLATFORM"

if curl -sL "$RELEASE_URL" -o horizons-checker 2>/dev/null; then
    echo "✅ Downloaded pre-built binary!"
else
    echo "⚠️  Pre-built binary not found. Downloading source and building..."
    
    # Download source files
    curl -sL "https://raw.githubusercontent.com/$GITHUB_REPO/main/main.py" -o main.py
    curl -sL "https://raw.githubusercontent.com/$GITHUB_REPO/main/events.json" -o events.json
    curl -sL "https://raw.githubusercontent.com/$GITHUB_REPO/main/config_local.py" -o config_local.py 2>/dev/null || true
    curl -sL "https://raw.githubusercontent.com/$GITHUB_REPO/main/requirements.txt" -o requirements.txt
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        echo "Python 3 not found. Installing..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            if command -v brew &> /dev/null; then
                brew install python
            else
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                brew install python
            fi
        else
            sudo apt update && sudo apt install -y python3 python3-pip 2>/dev/null || \
            sudo dnf install -y python3 python3-pip 2>/dev/null || \
            sudo yum install -y python3 python3-pip 2>/dev/null
        fi
    fi
    
    # Install dependencies and run
    echo "Installing dependencies..."
    pip3 install --break-system-packages -r requirements.txt 2>/dev/null || pip3 install -r requirements.txt
    
    echo ""
    echo "=================================="
    echo "  Starting Horizons Event Checker"
    echo "=================================="
    echo ""
    
    python3 main.py
    
    # Cleanup
    cd -
    rm -rf "$TEMP_DIR"
    exit 0
fi

# Make executable
chmod +x horizons-checker

echo ""
echo "=================================="
echo "  Starting Horizons Event Checker"
echo "=================================="
echo ""

# Run
./horizons-checker

# Cleanup
cd -
rm -rf "$TEMP_DIR"
