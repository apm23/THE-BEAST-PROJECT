@echo off
title DLTB SWITCH BACK NORMAL PROVEN
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0SWITCH_BACK_NORMAL.ps1"
set EC=%ERRORLEVEL%
echo.
echo ExitCode=%EC%
pause
exit /b %EC%
