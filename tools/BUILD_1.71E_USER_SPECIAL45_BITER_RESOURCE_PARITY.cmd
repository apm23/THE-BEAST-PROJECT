@echo off
setlocal
cd /d "%~dp0.."

echo ============================================================
echo THE BEAST PROJECT - SPECIAL45 BITER RESOURCE PARITY CANDIDATE
echo ============================================================
echo.
echo This builds a local candidate from the verified 1.71E baseline.
echo Canonical SPECIAL45 is not overwritten.
echo.

python ".\tools\build_user_special45_biter_resource_parity.py"
if errorlevel 1 (
    echo.
    echo BUILD FAILED.
    echo Nothing was installed into the game.
    pause
    exit /b 1
)

echo.
echo BUILD PASS.
echo Candidate:
echo   local_build\USER_SPECIAL45_BITER_RESOURCE_PARITY\data2_payload.pak
echo.
echo STATUS: CANDIDATE - NOT RUNTIME GREEN.
echo Test NORMAL mode first before promoting it.
pause
