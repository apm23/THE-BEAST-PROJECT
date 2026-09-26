@echo off
setlocal
cd /d "%~dp0.."

python tools\validate_remake_proven45_stage0.py
if errorlevel 1 goto :fail

python tools\build_remake_final_candidate.py
if errorlevel 1 goto :fail

echo.
echo FINAL SINGLEPLAYER CORE CANDIDATE BUILT.
echo Output: local_build\REMAKE_PROVEN45_SINGLEPLAYER_CORE\data2_payload.pak
echo NOTE: still CANDIDATE_NOT_RUNTIME_GREEN until test matrix passes in game.
pause
exit /b 0

:fail
echo.
echo FINAL BUILD STOPPED SAFELY. Read the error above.
pause
exit /b 1
