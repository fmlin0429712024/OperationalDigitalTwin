# Run in two separate terminals for best results, 
# or use this script to launch them in background (simple version)

Write-Host "Starting Simulator (Background)..." -ForegroundColor Cyan
Start-Process -NoNewWindow -FilePath ".\venv\Scripts\python.exe" -ArgumentList "simulator.py"

Write-Host "Starting Streamlit Dashboard..." -ForegroundColor Green
Invoke-Expression ".\venv\Scripts\streamlit run main.py"
