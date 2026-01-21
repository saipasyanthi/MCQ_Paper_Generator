#!/bin/bash
# Setup script for MCQ Paper Generator
# Run: bash setup.sh

echo "=================================="
echo "MCQ Paper Generator"
echo "Setup Script"
echo "=================================="
echo ""

# Check Python version
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 not found"
    echo "Please install Python 3.7 or later from python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '(?<=Python ).*')
echo "✓ Found Python $PYTHON_VERSION"

# Check/Install pip
echo ""
echo "[2/5] Checking pip..."
if ! python3 -m pip --version &> /dev/null; then
    echo "Installing pip..."
    python3 -m ensurepip --default-pip
fi
echo "✓ Pip is available"

# Install dependencies
echo ""
echo "[3/5] Installing dependencies..."
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Error installing dependencies"
    exit 1
fi

# Create necessary directories
echo ""
echo "[4/5] Setting up directories..."
mkdir -p output licenses
echo "✓ Directories created"

# Generate initial license
echo ""
echo "[5/5] License Setup"
echo ""
echo "Would you like to:"
echo "1. Generate a new license (for administrator)"
echo "2. Skip (if you already have license.json)"
read -p "Choose (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    python3 license_generator.py
fi

echo ""
echo "=================================="
echo "✓ Setup Complete!"
echo "=================================="
echo ""
echo "To start the application, run:"
echo "  python3 app.py"
echo ""
echo "For more information, see README_GUI.md"
echo ""
