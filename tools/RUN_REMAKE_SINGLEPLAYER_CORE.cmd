@echo off
setlocal
cd /d "%~dp0.."
echo ==============================================================
echo  THE BEAST PROJECT - REMAKE PROVEN45 SINGLEPLAYER CORE
echo  Runtime target: 1.71PE
echo  Sense: DEFERRED   CO-OP: DEFERRED
echo ==============================================================
echo.

call tools\RUN_1.71PE_CORE_PREP.cmd
set PREP=%ERRORLEVEL%
if %PREP%==2 goto :port
if not %PREP%==0 goto :fail

call tools\BUILD_REMAKE_PROVEN45_RECOVERED.cmd
if errorlevel 1 goto :transplant

call tools\PACKAGE_REMAKE_CANDIDATE.cmd
if errorlevel 1 goto :fail

python tools\remake_status.py

echo.
echo ==============================================================
echo  PIPELINE COMPLETE TO RUNTIME-TEST PACKAGE
echo  ZIP: local_build\DLTB_REMAKE_PROVEN45_1.71PE_CANDIDATE.zip
echo  STATUS: CANDIDATE_NOT_RUNTIME_GREEN until in-game tests pass.
echo ==============================================================
exit /b 0

:transplant
echo.
echo ==============================================================
echo  SAFE STOP: RECOVERED G1 TRANSPLANT DID NOT MATCH 1.71PE
echo  No guessed patch was produced and no game file was installed.
echo  Review CURRENT_RUNTIME mapping / context before changing anything.
echo ==============================================================
python tools\remake_status.py
exit /b 4

:port
echo.
echo ==============================================================
echo  SAFE STOP: DEDICATED 1.71PE SPECIAL45 PORT REQUIRED
echo  Review local_build\PORT_1.71PE_PLAN\PORT_PLAN.txt
echo  No gameplay candidate was installed or packaged.
echo ==============================================================
python tools\remake_status.py
exit /b 2

:fail
echo.
echo REMAKE PIPELINE FAILED SAFELY. No automatic install was performed.
python tools\remake_status.py
exit /b 1
