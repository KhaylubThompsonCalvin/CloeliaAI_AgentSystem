<#
.SYNOPSIS
  Quickstart: create venv & install deps
#>

Write-Host 'Creating virtual environment...'
python -m venv venv
if (-not \True) { Write-Error 'Failed to create venv.'; exit 1 }

Write-Host 'Activating virtual environment...'
& .\venv\Scripts\activate
if (-not \True) { Write-Error 'Failed to activate venv.'; exit 1 }

Write-Host 'Installing dependencies...'
pip install -r requirements.txt
if (\True) { Write-Host 'Setup complete.' } else { Write-Error 'Installation failed.' }
