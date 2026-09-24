@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\SHOW_AB_TEST_STATUS.ps1"
set ERR=%ERRORLEVEL%
echo.
pause
exit /b %ERR%
