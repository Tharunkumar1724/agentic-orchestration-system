# GitHub Login and Push Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Authentication & Push Helper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Refresh environment variables to pick up GitHub CLI
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Check if gh is available
if (Get-Command gh -ErrorAction SilentlyContinue) {
    Write-Host "✓ GitHub CLI found!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Starting GitHub login..." -ForegroundColor Yellow
    Write-Host ""
    
    # Login to GitHub
    gh auth login
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ Login successful!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Now pushing your code to GitHub..." -ForegroundColor Yellow
        
        # Navigate to project directory
        Set-Location "c:\Sorry\agentic_app"
        
        # Push to GitHub
        git push -u origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "✓ SUCCESS! Code pushed to GitHub!" -ForegroundColor Green
            Write-Host "========================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "View your repository at:" -ForegroundColor Cyan
            Write-Host "https://github.com/Tharunkumar1724/agentic-orchestration-system" -ForegroundColor Yellow
        } else {
            Write-Host ""
            Write-Host "✗ Push failed. Please check the error above." -ForegroundColor Red
        }
    } else {
        Write-Host "✗ Login failed. Please try again." -ForegroundColor Red
    }
} else {
    Write-Host "✗ GitHub CLI not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please close this PowerShell window and open a NEW one, then run:" -ForegroundColor Yellow
    Write-Host "  .\github-login-push.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "OR use GitHub Desktop: https://desktop.github.com/" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
