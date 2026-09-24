@echo off
title DLTB ONE-CLICK INSTALL
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0INSTALL_ONE_CLICK.ps1"
set EC=%ERRORLEVEL%
echo.
echo ExitCode=%EC%
pause
exit /b %EC%
