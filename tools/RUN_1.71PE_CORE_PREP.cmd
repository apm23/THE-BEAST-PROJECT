@echo off
setlocal
cd /d "%~dp0.."
echo ==============================================================
echo  THE BEAST PROJECT - 1.71PE CORE PREP
echo ==============================================================
echo.
call tools\EXTRACT_1.71PE_TARGETS.cmd
if errorlevel 1 goto :fail
call tools\CHECK_1.71PE_COMPATIBILITY.cmd
if errorlevel 1 goto :fail
call tools\PREPARE_CURRENT_RUNTIME.cmd
if errorlevel 1 goto :port

python tools\collect_remake_r1_r2_mapping.py
if errorlevel 1 goto :fail
python tools\collect_remake_r3_r4_mapping.py
if errorlevel 1 goto :fail

echo.
echo ==============================================================
echo  CORE PREP PASS
echo  1.71PE baseline + compatibility + mappings are ready.
echo ==============================================================
pause
exit /b 0

:port
echo.
echo ==============================================================
echo  STOP: 1.71PE CORE PORT REQUIRED
echo  No gameplay candidate was built.
echo  See local_build\CURRENT_RUNTIME_PREP\CURRENT_RUNTIME.txt
echo ==============================================================
pause
exit /b 2

:fail
echo.
echo CORE PREP FAILED. No gameplay candidate was built.
pause
exit /b 1
