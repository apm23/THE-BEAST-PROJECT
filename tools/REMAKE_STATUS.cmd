@echo off
setlocal
cd /d "%~dp0.."
python tools\remake_status.py
echo.
echo Report: local_build\REMAKE_STATUS\status.txt
pause
