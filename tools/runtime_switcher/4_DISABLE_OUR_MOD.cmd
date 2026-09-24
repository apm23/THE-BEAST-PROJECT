@echo off
title DLTB DISABLE OUR MOD
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0DISABLE_OUR_MOD.ps1"
set EC=%ERRORLEVEL%
echo.
echo ExitCode=%EC%
pause
exit /b %EC%
