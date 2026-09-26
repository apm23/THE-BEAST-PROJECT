@echo off
setlocal
cd /d "%~dp0.."
python tools\check_1.71PE_compatibility.py
if errorlevel 1 (
  echo.
  echo CHECK FAILED.
  pause
  exit /b 1
)
echo.
echo CHECK COMPLETE. See local_build\COMPAT_1.71PE_VS_1.71E\compatibility.txt
pause
