@echo off
title DLTB SWITCH TO COOP MULTIMOD
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0SWITCH_TO_COOP.ps1"
set EC=%ERRORLEVEL%
echo.
echo ExitCode=%EC%
pause
exit /b %EC%
