#!/usr/bin/env bash
# 🎉 QUICK START - AI Marking System
# Run this script to get your application running immediately

echo "=========================================="
echo "AI Marking System - Quick Start"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "apps/api" ] || [ ! -d "apps/web" ]; then
    echo "❌ Please run this script from the project root directory"
    echo "   Current directory: $(pwd)"
    exit 1
fi

echo "✅ Project structure verified"
echo ""

# Check Python
if ! command -v python3.13 &> /dev/null; then
    echo "⚠️  Python 3.13 not found, trying 'python'"
    PYTHON="python"
else
    PYTHON="python3.13"
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

NODE_VERSION=$($($node -v | cut -d'v' -f2 | cut -d'.' -f1))
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ required, found $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) found"
echo "✅ Python found"
echo ""

# Backend Setup
echo "================================"
echo "🔧 Setting up Backend..."
echo "================================"
cd apps/api

if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    $PYTHON -m venv venv
fi

echo "📦 Installing Python dependencies..."
$PYTHON -m pip install -q -r requirements.txt

echo "✅ Backend dependencies installed"
echo ""

cd ../../

# Frontend Setup
echo "================================"
echo "🔧 Setting up Frontend..."
echo "================================"
cd apps/web

if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
fi

echo "✅ Frontend dependencies installed"
echo ""

cd ../../

# Instructions
echo "================================"
echo "🚀 READY TO START!"
echo "================================"
echo ""
echo "📌 STEP 1: Start the Backend Server"
echo "   Open a terminal and run:"
echo "   $ cd apps/api"
echo "   $ python -m uvicorn app.main:app --reload"
echo ""
echo "   ✓ Backend will be available at: http://127.0.0.1:8000"
echo "   ✓ API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "📌 STEP 2: Start the Frontend Server"
echo "   Open another terminal and run:"
echo "   $ cd apps/web"
echo "   $ npm run dev"
echo ""
echo "   ✓ Frontend will be available at: http://localhost:5173"
echo ""
echo "📌 STEP 3: Access Your App"
echo "   Open your browser: http://localhost:5173"
echo "   Register a new account or login"
echo "   Upload answer sheets for evaluation"
echo ""
echo "================================"
echo "✨ Enjoy! Your app is ready! ✨"
echo "================================"
