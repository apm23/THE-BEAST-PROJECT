@echo off
title THE BEAST PROJECT - 1.71E PORTABLE BOOTSTRAP
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0bootstrap_1.71E_user_special45.ps1"
set EC=%ERRORLEVEL%
echo.
echo ExitCode=%EC%
pause
exit /b %EC%
