# Agentic AI Platform - Quick Start Script
# This script starts both backend and frontend servers

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "🤖 Agentic AI Platform - Quick Start" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if frontend dependencies are installed
if (-Not (Test-Path "frontend\node_modules")) {
    Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
    cd frontend
    npm install
    cd ..
    Write-Host "✅ Frontend dependencies installed!" -ForegroundColor Green
    Write-Host ""
}

Write-Host "🚀 Starting servers..." -ForegroundColor Cyan
Write-Host ""

# Start backend in a new window
Write-Host "1️⃣  Starting Backend API (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    Write-Host '🔧 Backend API Server' -ForegroundColor Cyan
    Write-Host '=====================' -ForegroundColor Cyan
    Write-Host ''
    cd C:\Sorry\agentic_app
    `$env:PYTHONPATH='C:\Sorry\agentic_app'
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"@

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend in a new window
Write-Host "2️⃣  Starting Frontend Dashboard (Port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
    Write-Host '🎨 Frontend Dashboard' -ForegroundColor Cyan
    Write-Host '====================' -ForegroundColor Cyan
    Write-Host ''
    cd C:\Sorry\agentic_app\frontend
    npm start
"@

Write-Host ""
Write-Host "✅ Servers starting..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access the application at:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop the servers" -ForegroundColor Yellow
Write-Host ""
