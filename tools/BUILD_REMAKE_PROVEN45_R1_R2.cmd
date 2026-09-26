@echo off
setlocal
cd /d "%~dp0\.."

python .\tools\validate_remake_proven45_stage0.py
if errorlevel 1 goto :fail

python .\tools\collect_remake_r1_r2_mapping.py
if errorlevel 1 goto :fail

python .\tools\build_remake_r1_r2_candidate.py
if errorlevel 1 goto :fail

echo.
echo R1/R2 CANDIDATE BUILD COMPLETE.
echo NOTE: This is NOT runtime-green until in-game validation passes.
pause
exit /b 0

:fail
echo.
echo BUILD STOPPED SAFELY. Read the error above.
pause
exit /b 1
