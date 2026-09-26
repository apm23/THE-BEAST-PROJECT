@echo off
setlocal
cd /d "%~dp0.."
echo ==============================================================
echo  THE BEAST PROJECT - BUILD RECOVERED PROVEN45 CORE
echo  SPECIAL45 exact foundation + proven G1 transplant specs
echo  Sense: DEFERRED   CO-OP: DEFERRED
echo ==============================================================
echo.
python tools\build_remake_proven45_recovered_candidate.py
set ERR=%ERRORLEVEL%
if not "%ERR%"=="0" (
  echo.
  echo BUILD STOPPED SAFELY. No game files were changed.
  exit /b %ERR%
)
echo.
echo BUILD PASS: local_build\REMAKE_PROVEN45_SINGLEPLAYER_CORE\data2_payload.pak
exit /b 0
