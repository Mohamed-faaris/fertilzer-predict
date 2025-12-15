#!/bin/bash

# Quick Start Script for Fertilizer Prediction Application
# This script sets up the environment and runs the application

set -e  # Exit on error

echo "🌾 Fertilizer Prediction Application - Quick Start"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if Java is installed (required for PySpark)
if ! command -v java &> /dev/null; then
    echo "⚠️  Java is not installed. PySpark requires Java 8 or 11."
    echo "   Install with: sudo apt install openjdk-11-jdk"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Java found: $(java -version 2>&1 | head -n 1)"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    
    # Check if python3-venv is available
    if ! python3 -m venv --help &> /dev/null; then
        echo "❌ python3-venv is not installed."
        echo "   Install with: sudo apt install python3-venv"
        exit 1
    fi
    
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
else
    echo "✅ Virtual environment already exists"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/requirements_installed.flag" ]; then
    echo "📥 Installing dependencies..."
    echo "   This may take a few minutes..."
    echo ""
    
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    
    # Create flag file
    touch venv/requirements_installed.flag
    
    echo "✅ Dependencies installed successfully"
    echo ""
else
    echo "✅ Dependencies already installed"
    echo ""
fi

# Verify key packages
echo "🔍 Verifying installation..."
python3 -c "import streamlit; print('  ✅ Streamlit:', streamlit.__version__)" 2>/dev/null || echo "  ❌ Streamlit not found"
python3 -c "import pyspark; print('  ✅ PySpark:', pyspark.__version__)" 2>/dev/null || echo "  ❌ PySpark not found"
python3 -c "import pandas; print('  ✅ Pandas:', pandas.__version__)" 2>/dev/null || echo "  ❌ Pandas not found"
echo ""

# Check if data file exists
if [ ! -f "data/Fertilizer Prediction.csv" ]; then
    echo "⚠️  Warning: Data file not found at data/Fertilizer Prediction.csv"
    echo ""
fi

echo "🚀 Starting Streamlit application..."
echo "   The app will open in your browser at http://localhost:8501"
echo "   Press Ctrl+C to stop the application"
echo ""
echo "=================================================="
echo ""

# Run the application
streamlit run app.py
