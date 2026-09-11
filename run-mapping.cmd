@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Python virtual environment not found.
    echo Follow the initial setup instructions in README.md first.
    pause
    exit /b 1
)

rem Use this file's location rather than a machine-specific path.
rem Elevate for the temporary gameinfo symlinks used by the Python launcher.
set "CS2FIXES_MAPPING_LAUNCHER=%~f0"
powershell.exe -NoProfile -Command "$ErrorActionPreference = 'Stop'; $identity = [Security.Principal.WindowsIdentity]::GetCurrent(); $principal = New-Object Security.Principal.WindowsPrincipal($identity); if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) { try { Start-Process -FilePath $env:CS2FIXES_MAPPING_LAUNCHER -Verb RunAs; exit 10 } catch { Write-Host 'Administrator launch was cancelled or failed.'; exit 1 } }"
if errorlevel 10 exit /b 0
if errorlevel 1 (
    pause
    exit /b 1
)

".venv\Scripts\python.exe" run-mapping.py
if errorlevel 1 (
    echo.
    echo Launch failed. Check the messages above.
    pause
    exit /b 1
)
endlocal
