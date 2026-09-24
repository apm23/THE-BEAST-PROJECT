@echo off
title DLTB CHECK CURRENT MODE
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0CHECK_MODE.ps1"
set EC=%ERRORLEVEL%
echo.
echo ExitCode=%EC%
pause
exit /b %EC%
