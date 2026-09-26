@echo off
setlocal
cd /d "%~dp0.."
python tools\package_remake_candidate.py
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo PACKAGE READY: local_build\DLTB_REMAKE_PROVEN45_1.71PE_CANDIDATE.zip
) else (
  echo PACKAGE FAILED OR FINAL CANDIDATE NOT READY.
)
pause
exit /b %RC%
