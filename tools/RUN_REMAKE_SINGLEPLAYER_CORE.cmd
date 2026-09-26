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

rem Authoritative gate: trust CURRENT_RUNTIME.json, not an incidental wrapper code.
set RUNTIME_OK=0
if exist local_build\CURRENT_RUNTIME_PREP\CURRENT_RUNTIME.json (
  python -c "import json,sys; p=json.load(open(r'local_build\CURRENT_RUNTIME_PREP\CURRENT_RUNTIME.json',encoding='utf-8')); sys.exit(0 if p.get('mode')=='SPECIAL45_CORE_BYTE_COMPATIBLE' and not p.get('mapping_inputs_missing') else 1)"
  if not errorlevel 1 set RUNTIME_OK=1
)

if "%RUNTIME_OK%"=="1" goto :build
if %PREP%==2 goto :port
if not %PREP%==0 goto :fail

:build
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
