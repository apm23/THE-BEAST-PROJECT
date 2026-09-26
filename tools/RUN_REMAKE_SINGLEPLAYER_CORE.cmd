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
if errorlevel 1 goto :authoring

python tools\remake_status.py
if errorlevel 1 goto :fail

if exist "local_build\REMAKE_PROVEN45_SINGLEPLAYER_CORE\data2_payload.pak" (
  call tools\PACKAGE_REMAKE_CANDIDATE.cmd
  exit /b %ERRORLEVEL%
)

echo.
echo ==============================================================
echo  PARTIAL BUILD COMPLETE
echo  R1/R2 candidate exists, but combined R3/R4/final candidate is not ready.
echo  See local_build\REMAKE_STATUS\status.txt
echo ==============================================================
exit /b 3

:authoring
echo.
echo ==============================================================
echo  SAFE STOP: R1/R2 OPERATIONS NEED CURRENT-RUNTIME AUTHORING
echo  No guessed gameplay PAK was installed or packaged.
echo  Mapping files are under local_build\REMAKE_PROVEN45\mapping
echo ==============================================================
python tools\remake_status.py
exit /b 4

:port
echo.
echo ==============================================================
echo  SAFE STOP: DEDICATED 1.71PE PORT REQUIRED
echo  Review generated port plan before gameplay build.
echo ==============================================================
python tools\remake_status.py
exit /b 2

:fail
echo.
echo REMAKE PIPELINE FAILED SAFELY. No automatic install was performed.
python tools\remake_status.py
exit /b 1
