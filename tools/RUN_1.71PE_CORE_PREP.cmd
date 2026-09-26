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
rem Do not trust a transient wrapper return code here. The materialized
rem CURRENT_RUNTIME.json is the authoritative gate for this branch.

python tools\collect_remake_r1_r2_mapping.py
if errorlevel 1 goto :fail
python tools\collect_remake_special_infected_mapping.py
if errorlevel 1 goto :fail
python tools\collect_remake_r3_r4_mapping.py
if errorlevel 1 goto :fail

python -c "import json,sys; p='local_build/CURRENT_RUNTIME_PREP/CURRENT_RUNTIME.json'; d=json.load(open(p,encoding='utf-8')); sys.exit(0 if d.get('mode')=='SPECIAL45_CORE_BYTE_COMPATIBLE' and not d.get('core_non_identical') and not d.get('mapping_inputs_missing') else 2)"
set GATE_RC=%ERRORLEVEL%
if "%GATE_RC%"=="2" goto :port
if not "%GATE_RC%"=="0" goto :fail

echo.
echo ==============================================================
echo  CORE PREP PASS
echo  CURRENT_RUNTIME.json confirms 1.71PE direct SPECIAL45 reuse.
echo  Baseline + compatibility + all core mappings ready.
echo ==============================================================
exit /b 0

:port
echo.
echo ==============================================================
echo  1.71PE CORE PORT REQUIRED - AUTHORITATIVE REPORT GATE
echo  No gameplay candidate was built.
echo  Port plan: local_build\PORT_1.71PE_PLAN\PORT_PLAN.txt
echo  Runtime:   local_build\CURRENT_RUNTIME_PREP\CURRENT_RUNTIME.txt
echo  Mappings:  local_build\REMAKE_PROVEN45\mapping
echo ==============================================================
exit /b 2

:fail
echo.
echo CORE PREP FAILED. No gameplay candidate was built.
exit /b 1
