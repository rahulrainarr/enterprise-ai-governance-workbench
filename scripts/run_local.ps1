$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
& ".\.venv\Scripts\python.exe" -m streamlit run app\streamlit_app.py --server.headless=true --server.port=8766 --browser.gatherUsageStats=false
