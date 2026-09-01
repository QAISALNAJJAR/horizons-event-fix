#!/bin/bash

# Horizons Event Checker - One-Click Install and Run
# For macOS/Linux

echo "=================================="
echo "  Horizons Event Checker Setup"
echo "=================================="
echo ""

GITHUB_REPO="QAISALNAJJAR/horizons-event-fix"

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "Downloading latest code..."

# Download files
curl -sL "https://raw.githubusercontent.com/$GITHUB_REPO/main/main.py" -o main.py
curl -sL "https://raw.githubusercontent.com/$GITHUB_REPO/main/events.json" -o events.json
curl -sL "https://raw.githubusercontent.com/$GITHUB_REPO/main/requirements.txt" -o requirements.txt

# Check if Python 3 is installed
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

echo "Python 3 found: $(python3 --version)"
echo ""
echo "Installing required packages..."
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
