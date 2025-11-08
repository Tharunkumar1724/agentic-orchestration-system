$env:PYTHONPATH = "c:\Sorry\agentic_app"
cd c:\Sorry\agentic_app
python -m uvicorn app.main:app --reload --port 8000
