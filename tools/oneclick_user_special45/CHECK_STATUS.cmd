@echo off
title DLTB MOD STATUS
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0CHECK_STATUS.ps1"
set EC=%ERRORLEVEL%
echo.
echo ExitCode=%EC%
pause
exit /b %EC%
