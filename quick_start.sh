#!/bin/bash

echo "🚀 Setting up CCS-Validator..."

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Run tests
echo "📊 Running tests..."
pytest tests/ -v

# Run demo
echo "🎯 Running demonstration..."
python examples/simple_test.py

echo "✅ Setup complete!"