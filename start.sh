#!/bin/bash

echo "🎬 Video Recommender - Starting up..."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Virtual environment created"
else
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env and add your ANTHROPIC_API_KEY"
    echo "   Get your key from: https://console.anthropic.com/"
    echo ""
    read -p "Press Enter to open .env in editor (or Ctrl+C to exit)..."
    ${EDITOR:-nano} .env
fi

# Source the .env file
export $(cat .env | grep -v '^#' | xargs)

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "your_api_key_here" ]; then
    echo "❌ ANTHROPIC_API_KEY not set in .env file"
    echo "   Please add your API key to .env and try again"
    exit 1
fi

echo "✅ API key configured"
echo "🚀 Starting Flask server..."
echo ""
echo "   Open your browser to: http://localhost:6006"
echo "   Press Ctrl+C to stop the server"
echo ""

# Run the app
python app.py
