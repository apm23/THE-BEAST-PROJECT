@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo DLTB A/B TEST - 1 CLEAN ALL LIVE MOD DATA
ECHO ============================================================
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\CLEAN_FOR_AB_TEST.ps1"
set ERR=%ERRORLEVEL%
echo.
if not "%ERR%"=="0" echo CLEAN FAILED - jangan lanjut install.
if "%ERR%"=="0" echo CLEAN PASS - siap pilih NEW TEST atau PROVEN CONTROL.
pause
exit /b %ERR%
