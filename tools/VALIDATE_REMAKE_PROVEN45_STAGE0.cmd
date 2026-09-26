@echo off
setlocal
cd /d "%~dp0.."
python tools\validate_remake_proven45_stage0.py
set "EC=%ERRORLEVEL%"
echo.
if "%EC%"=="0" (
  echo [PASS] REMAKE PROVEN45 Stage0 ready.
) else (
  echo [STOP] Stage0 validation failed. ExitCode=%EC%
)
pause
exit /b %EC%
