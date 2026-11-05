#!/bin/bash
cd "$(dirname "$0")"

echo "========================================"
echo "   CVM colorBot Launcher (macOS)"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Start CVM colorBot using venv Python
echo "[*] Starting CVM colorBot..."
echo ""

venv/bin/python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Program exited with error"
fi
