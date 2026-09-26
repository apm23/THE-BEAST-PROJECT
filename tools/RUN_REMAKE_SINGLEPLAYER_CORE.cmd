@echo off
setlocal
cd /d "%~dp0.."
echo ==============================================================
echo  THE BEAST PROJECT - REMAKE PROVEN45 SINGLEPLAYER CORE
echo  Runtime target: 1.71PE
echo ==============================================================
echo.

call tools\RUN_1.71PE_CORE_PREP.cmd
set PREP=%ERRORLEVEL%
if %PREP%==2 goto :port
if not %PREP%==0 goto :fail

call tools\BUILD_REMAKE_PROVEN45_R1_R2.cmd
if errorlevel 1 goto :r1authoring

call tools\BUILD_REMAKE_PROVEN45_FINAL.cmd
if errorlevel 1 goto :finalauthoring

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

:r1authoring
echo.
echo ==============================================================
echo  SAFE STOP: R1/R2 OPS NEED 1.71PE CURRENT-RUNTIME AUTHORING
echo  Mapping: local_build\REMAKE_PROVEN45\mapping\R1_R2_MAPPING.*
echo  No guessed gameplay PAK was installed or packaged.
echo ==============================================================
python tools\remake_status.py
exit /b 4

:finalauthoring
echo.
echo ==============================================================
echo  SAFE STOP: FINAL OPS NEED CURRENT-RUNTIME AUTHORING
echo  Review SPECIAL_INFECTED_EXOTIC_MAPPING and R3_R4_MAPPING.
echo  Then author config\remake_proven45_final_ops.json.
echo ==============================================================
python tools\remake_status.py
exit /b 5

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
