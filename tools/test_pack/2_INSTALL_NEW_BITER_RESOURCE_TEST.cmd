@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo DLTB A/B TEST - 2 INSTALL NEW BITER RESOURCE TEST
ECHO ============================================================
echo.
echo This will clean live mod data again before installing the candidate.
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\INSTALL_NEW_BITER_RESOURCE_TEST.ps1"
set ERR=%ERRORLEVEL%
echo.
if not "%ERR%"=="0" echo INSTALL NEW TEST FAILED.
if "%ERR%"=="0" echo INSTALL NEW TEST PASS - launch game and test ordinary Biters.
pause
exit /b %ERR%
