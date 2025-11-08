@echo off
REM YAML-Only Tool Orchestration - Simple Execution
REM No Python code needed!

setlocal enabledelayedexpansion

:menu
cls
echo =====================================
echo   YAML-Only Tool Orchestration
echo =====================================
echo.
echo 1. Simple Web Search
echo 2. Multi-Source Research
echo 3. Parallel Regional Search
echo 4. List All Tools
echo 5. List All Agents
echo 6. List All Workflows
echo 7. Exit
echo.

set /p choice="Select option (1-7): "

if "%choice%"=="1" goto simple_search
if "%choice%"=="2" goto multi_research
if "%choice%"=="3" goto parallel_search
if "%choice%"=="4" goto list_tools
if "%choice%"=="5" goto list_agents
if "%choice%"=="6" goto list_workflows
if "%choice%"=="7" goto end
echo Invalid option
pause
goto menu

:simple_search
echo.
set /p topic="Enter search topic (or press Enter for 'artificial intelligence'): "
if "%topic%"=="" set topic=artificial intelligence
echo.
echo Executing simple web search for: %topic%
echo Please wait...
echo.
curl -X POST http://localhost:8000/workflows/simple_web_search_workflow/execute ^
  -H "Content-Type: application/json" ^
  -d "{\"parameters\": {\"topic\": \"%topic%\"}}"
echo.
pause
goto menu

:multi_research
echo.
set /p topic="Enter research topic (or press Enter for 'climate change'): "
if "%topic%"=="" set topic=climate change
echo.
echo Executing multi-source research for: %topic%
echo Please wait...
echo.
curl -X POST http://localhost:8000/workflows/multi_source_research/execute ^
  -H "Content-Type: application/json" ^
  -d "{\"parameters\": {\"topic\": \"%topic%\"}}"
echo.
pause
goto menu

:parallel_search
echo.
set /p topic="Enter topic (or press Enter for 'technology trends'): "
if "%topic%"=="" set topic=technology trends
echo.
echo Executing parallel regional search for: %topic%
echo Please wait...
echo.
curl -X POST http://localhost:8000/workflows/parallel_region_search/execute ^
  -H "Content-Type: application/json" ^
  -d "{\"parameters\": {\"topic\": \"%topic%\"}}"
echo.
pause
goto menu

:list_tools
echo.
echo Fetching all tools...
echo.
curl http://localhost:8000/tools/
echo.
pause
goto menu

:list_agents
echo.
echo Fetching all agents...
echo.
curl http://localhost:8000/agents/
echo.
pause
goto menu

:list_workflows
echo.
echo Fetching all workflows...
echo.
curl http://localhost:8000/workflows/
echo.
pause
goto menu

:end
echo.
echo Goodbye!
echo.
exit /b
