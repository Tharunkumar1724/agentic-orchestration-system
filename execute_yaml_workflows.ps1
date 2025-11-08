# YAML-Only Tool Orchestration - PowerShell Helper
# Execute workflows without writing any Python code!

$BaseUrl = "http://localhost:8000"

function Show-Menu {
    Write-Host "`n=================================" -ForegroundColor Cyan
    Write-Host "  YAML-Only Tool Orchestration" -ForegroundColor Cyan
    Write-Host "=================================" -ForegroundColor Cyan
    Write-Host "`n1. Simple Web Search"
    Write-Host "2. Multi-Source Research (Web + News + Academic)"
    Write-Host "3. Parallel Regional Search (US + UK)"
    Write-Host "4. Custom Search (Enter your own topic)"
    Write-Host "5. List All Tools"
    Write-Host "6. List All Agents"
    Write-Host "7. List All Workflows"
    Write-Host "8. Exit"
    Write-Host ""
}

function Execute-Workflow {
    param(
        [string]$WorkflowId,
        [string]$Topic
    )
    
    Write-Host "`nExecuting workflow: $WorkflowId" -ForegroundColor Yellow
    Write-Host "Topic: $Topic" -ForegroundColor Yellow
    Write-Host "Please wait..." -ForegroundColor Yellow
    
    $body = @{
        parameters = @{
            topic = $Topic
        }
    } | ConvertTo-Json
    
    try {
        $result = Invoke-RestMethod -Uri "$BaseUrl/workflows/$WorkflowId/execute" `
            -Method Post `
            -ContentType "application/json" `
            -Body $body
        
        Write-Host "`n✓ Success!" -ForegroundColor Green
        Write-Host "`nResults:" -ForegroundColor Cyan
        $result | ConvertTo-Json -Depth 10 | Write-Host
        
        return $result
    }
    catch {
        Write-Host "`n✗ Error:" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        return $null
    }
}

function Get-Items {
    param(
        [string]$Type
    )
    
    Write-Host "`nFetching $Type..." -ForegroundColor Yellow
    
    try {
        $items = Invoke-RestMethod -Uri "$BaseUrl/$Type/" -Method Get
        
        Write-Host "`n✓ Found $($items.Count) $Type" -ForegroundColor Green
        
        foreach ($item in $items) {
            Write-Host "`n---" -ForegroundColor Gray
            Write-Host "ID: $($item.id)" -ForegroundColor Cyan
            Write-Host "Name: $($item.name)" -ForegroundColor White
            if ($item.type) {
                Write-Host "Type: $($item.type)" -ForegroundColor Yellow
            }
            if ($item.description) {
                Write-Host "Description: $($item.description)" -ForegroundColor Gray
            }
        }
        
        Write-Host ""
    }
    catch {
        Write-Host "`n✗ Error:" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
    }
}

# Main loop
$running = $true

while ($running) {
    Show-Menu
    $choice = Read-Host "Select option (1-8)"
    
    switch ($choice) {
        "1" {
            $topic = Read-Host "`nEnter search topic (or press Enter for 'artificial intelligence')"
            if ([string]::IsNullOrWhiteSpace($topic)) {
                $topic = "artificial intelligence"
            }
            Execute-Workflow -WorkflowId "simple_web_search_workflow" -Topic $topic
        }
        
        "2" {
            $topic = Read-Host "`nEnter research topic (or press Enter for 'climate change')"
            if ([string]::IsNullOrWhiteSpace($topic)) {
                $topic = "climate change"
            }
            Execute-Workflow -WorkflowId "multi_source_research" -Topic $topic
        }
        
        "3" {
            $topic = Read-Host "`nEnter topic for regional search (or press Enter for 'technology trends')"
            if ([string]::IsNullOrWhiteSpace($topic)) {
                $topic = "technology trends"
            }
            Execute-Workflow -WorkflowId "parallel_region_search" -Topic $topic
        }
        
        "4" {
            Write-Host "`nAvailable workflows:"
            Write-Host "  - simple_web_search_workflow"
            Write-Host "  - multi_source_research"
            Write-Host "  - parallel_region_search"
            
            $workflowId = Read-Host "`nEnter workflow ID"
            $topic = Read-Host "Enter topic"
            
            if (-not [string]::IsNullOrWhiteSpace($workflowId) -and -not [string]::IsNullOrWhiteSpace($topic)) {
                Execute-Workflow -WorkflowId $workflowId -Topic $topic
            }
            else {
                Write-Host "`n✗ Workflow ID and topic are required" -ForegroundColor Red
            }
        }
        
        "5" {
            Get-Items -Type "tools"
        }
        
        "6" {
            Get-Items -Type "agents"
        }
        
        "7" {
            Get-Items -Type "workflows"
        }
        
        "8" {
            Write-Host "`nGoodbye!" -ForegroundColor Cyan
            $running = $false
        }
        
        default {
            Write-Host "`n✗ Invalid option" -ForegroundColor Red
        }
    }
    
    if ($running) {
        Read-Host "`nPress Enter to continue"
    }
}
