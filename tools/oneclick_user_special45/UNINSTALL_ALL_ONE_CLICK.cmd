@echo off
title DLTB ONE-CLICK UNINSTALL ALL
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0UNINSTALL_ALL.ps1"
set EC=%ERRORLEVEL%
echo.
echo ExitCode=%EC%
pause
exit /b %EC%
