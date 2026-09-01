#!/bin/bash

# Horizons Event Checker - One-Click Install & Run
# For macOS/Linux

echo "=================================="
echo "  Horizons Event Checker Setup"
echo "=================================="
echo ""

GITHUB_RAW="https://raw.githubusercontent.com/QAISALNAJJAR/horizons-event-fix/main"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Installing..."
    
    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install python
        else
            echo "Installing Homebrew first..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            brew install python
        fi
    # Linux
    else
        if command -v apt &> /dev/null; then
            sudo apt update && sudo apt install -y python3 python3-pip
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3 python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip
        else
            echo "Please install Python 3 manually: https://www.python.org/downloads/"
            exit 1
        fi
    fi
fi

echo "Python 3 found: $(python3 --version)"
echo ""
echo "Downloading latest code from GitHub..."
echo ""

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Download files from GitHub
curl -sL "$GITHUB_RAW/main.py" -o main.py
curl -sL "$GITHUB_RAW/events.json" -o events.json
curl -sL "$GITHUB_RAW/requirements.txt" -o requirements.txt

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
