@echo off
title DLTB TOTAL CLEAN - SCAN ONLY
echo ==============================================================
echo  DLTB TOTAL CLEAN - SCAN ONLY
echo ==============================================================
echo Tidak ada file yang akan dihapus.
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0DLTB_TOTAL_CLEAN.ps1" -Mode Scan
set EC=%ERRORLEVEL%
echo.
echo ExitCode=%EC%
pause
exit /b %EC%
