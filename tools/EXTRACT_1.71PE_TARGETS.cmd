@echo off
setlocal
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File tools\extract_targeted_baseline_1.71PE.ps1
if errorlevel 1 (
  echo.
  echo EXTRACTION FAILED.
  pause
  exit /b 1
)
echo.
echo EXTRACTION COMPLETE. Run tools\CHECK_1.71PE_COMPATIBILITY.cmd next.
pause
