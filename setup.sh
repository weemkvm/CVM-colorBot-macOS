#!/bin/bash
cd "$(dirname "$0")"

echo "========================================"
echo "   CVM colorBot Setup Script (macOS)"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Install via: brew install python3"
    exit 1
fi

echo "[*] Checking Python version..."
python3 --version

# Create virtual environment
if [ -d "venv" ]; then
    echo "[*] Virtual environment already exists, skipping creation"
else
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "[OK] Virtual environment created successfully"
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
echo "[*] Upgrading pip..."
python3 -m pip install --upgrade pip --quiet

# Install dependencies
if [ -f "requirements_macos.txt" ]; then
    echo "[*] Installing macOS dependencies..."
    pip install -r requirements_macos.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
    echo "[OK] Dependencies installed successfully"
else
    echo "[WARNING] requirements_macos.txt not found, using requirements.txt"
    pip install -r requirements.txt
fi

echo ""
echo "========================================"
echo "   Setup Complete!"
echo "========================================"
echo ""
echo "You can now run ./run.sh to start the program"
echo ""
