#!/bin/bash
# Setup script for KDrama IA
set -e

echo "=== KDrama IA Setup ==="

if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found. Install Python 3.10+."
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "Usage:"
echo "  source venv/bin/activate"
echo "  python train.py       # Fine-tune the model"
echo "  python chat.py        # Chat with the trained model"
