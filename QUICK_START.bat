@echo off
REM 🎉 QUICK START - AI Marking System (Windows)
REM Run this script to get your application running immediately

cls
echo.
echo ==========================================
echo AI Marking System - Quick Start (Windows)
echo ==========================================
echo.

REM Check if we're in the right directory
if not exist "apps\api" (
    echo ❌ Error: apps\api directory not found
    echo    Please run this script from the project root directory
    pause
    exit /b 1
)

if not exist "apps\web" (
    echo ❌ Error: apps\web directory not found
    echo    Please run this script from the project root directory
    pause
    exit /b 1
)

echo ✅ Project structure verified
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python 3.13 and add it to PATH
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed
    echo    Please install Node.js 18+ from https://nodejs.org
    pause
    exit /b 1
)

for /f %%i in ('node --version') do set NODE_VERSION=%%i
echo ✅ Node.js %NODE_VERSION% found
echo.

REM Backend Setup
echo ================================
echo 🔧 Setting up Backend...
echo ================================

cd apps\api

echo 📦 Installing Python dependencies...
python -m pip install -q -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Backend dependencies installed
echo.

cd ..\..\

REM Frontend Setup
echo ================================
echo 🔧 Setting up Frontend...
echo ================================

cd apps\web

if not exist "node_modules" (
    echo 📦 Installing npm dependencies...
    call npm install
)

if %errorlevel% neq 0 (
    echo ⚠️  Warning: npm install had some issues
    echo    You may need to run 'npm install' manually
)

echo ✅ Frontend dependencies installed
echo.

cd ..\..\

REM Instructions
echo ================================
echo 🚀 READY TO START!
echo ================================
echo.
echo 📌 STEP 1: Start the Backend Server
echo    Open a new Command Prompt and run:
echo    $ cd apps\api
echo    $ python -m uvicorn app.main:app --reload
echo.
echo    ✓ Backend will be available at: http://127.0.0.1:8000
echo    ✓ API Docs: http://127.0.0.1:8000/docs
echo.
echo 📌 STEP 2: Start the Frontend Server
echo    Open another Command Prompt and run:
echo    $ cd apps\web
echo    $ npm run dev
echo.
echo    ✓ Frontend will be available at: http://localhost:5173
echo.
echo 📌 STEP 3: Access Your App
echo    Open your browser: http://localhost:5173
echo    Register a new account or login
echo    Upload answer sheets for evaluation
echo.
echo 📌 BONUS: View API Documentation
echo    Open: http://127.0.0.1:8000/docs
echo.
echo ================================
echo ✨ Enjoy! Your app is ready! ✨
echo ================================
echo.

pause
