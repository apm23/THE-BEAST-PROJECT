@echo off
setlocal
cd /d "%~dp0\.."
python .\tools\build_special45_global_loot_root_v1.py
set EC=%ERRORLEVEL%
echo.
if not "%EC%"=="0" (
  echo BUILD FAILED - exit %EC%
) else (
  echo BUILD PASS
)
pause
exit /b %EC%
