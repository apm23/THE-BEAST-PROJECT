@echo off
setlocal
cd /d "%~dp0.."
python tools\collect_remake_r3_r4_mapping.py
if errorlevel 1 (
  echo.
  echo R3/R4 mapping FAILED.
  exit /b 1
)
echo.
echo R3/R4 mapping complete.
endlocal
