@echo off
setlocal
cd /d "%~dp0.."
python tools\prepare_current_runtime_baseline.py
set RC=%ERRORLEVEL%
echo.
if %RC%==0 (
  echo CURRENT RUNTIME READY: SPECIAL45 core is byte-compatible.
) else (
  echo CURRENT RUNTIME NEEDS PORT BEFORE GAMEPLAY BUILD.
)
echo Report: local_build\CURRENT_RUNTIME_PREP\CURRENT_RUNTIME.txt
pause
exit /b %RC%
