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

python tools\generate_1.71PE_port_plan.py
if errorlevel 1 goto :fail

call tools\PREPARE_CURRENT_RUNTIME.cmd
set PREP_RC=%ERRORLEVEL%

rem PREPARE_CURRENT_RUNTIME always materializes CURRENT_RUNTIME before returning
rem port-required status. Collect mappings from the actual 1.71PE runtime either way.
python tools\collect_remake_r1_r2_mapping.py
if errorlevel 1 goto :fail
python tools\collect_remake_special_infected_mapping.py
if errorlevel 1 goto :fail
python tools\collect_remake_r3_r4_mapping.py
if errorlevel 1 goto :fail

if not "%PREP_RC%"=="0" goto :port

echo.
echo ==============================================================
echo  CORE PREP PASS
echo  1.71PE baseline + compatibility + all core mappings ready.
echo ==============================================================
pause
exit /b 0

:port
echo.
echo ==============================================================
echo  1.71PE CORE PORT REQUIRED - ANALYSIS READY
echo  No gameplay candidate was built.
echo  Port plan: local_build\PORT_1.71PE_PLAN\PORT_PLAN.txt
echo  Runtime:   local_build\CURRENT_RUNTIME_PREP\CURRENT_RUNTIME.txt
echo  Mappings:  local_build\REMAKE_PROVEN45\mapping
echo ==============================================================
pause
exit /b 2

:fail
echo.
echo CORE PREP FAILED. No gameplay candidate was built.
pause
exit /b 1
