#!/bin/bash
# FIFOLive launcher
cd "$(dirname "$0")"

echo "🚀 Starting FIFOLive..."
echo "   Open http://localhost:8000 once the server starts"
echo ""

# Use venv python
if [ -f ".venv/bin/python" ]; then
    .venv/bin/python main.py
else
    echo "Venv not found. Creating one..."
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    .venv/bin/python main.py
fi
