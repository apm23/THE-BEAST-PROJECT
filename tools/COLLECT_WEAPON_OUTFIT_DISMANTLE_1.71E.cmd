@echo off
setlocal
cd /d "%~dp0.."

echo ============================================================
echo THE BEAST PROJECT - WEAPON + OUTFIT DISMANTLE COLLECTOR
echo READ-ONLY - tidak mengubah PAK, save, config, atau MultiMod
echo ============================================================
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0collect_weapon_outfit_dismantle_1.71E.ps1" %*
set "ERR=%ERRORLEVEL%"

echo.
if not "%ERR%"=="0" (
    echo FAIL: collector berhenti dengan error code %ERR%.
) else (
    echo DONE: upload ZIP hasil yang ditampilkan di atas ke chat.
)
echo.
pause
exit /b %ERR%
