@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo DLTB A/B TEST - 3 RESTORE PROVEN SPECIAL45 CONTROL
ECHO ============================================================
echo.
echo This will clean the candidate/other live mod data first,
echo then rebuild and install exact proven SPECIAL45.
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\INSTALL_PROVEN_SPECIAL45_CONTROL.ps1"
set ERR=%ERRORLEVEL%
echo.
if not "%ERR%"=="0" echo RESTORE PROVEN SPECIAL45 FAILED.
if "%ERR%"=="0" echo PROVEN SPECIAL45 CONTROL INSTALLED.
pause
exit /b %ERR%
