#!/bin/bash
# Startup script for MCQ Paper Generator Web App

echo "======================================================"
echo "    MCQ PAPER GENERATOR - WEB APPLICATION"
echo "======================================================"
echo ""

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Install dependencies if needed
if ! python -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install flask werkzeug
fi

# Start the web server
echo ""
echo "Starting web server..."
echo ""
python app_web.py
