@echo off
setlocal
cd /d "%~dp0.."
python tools\collect_remake_r1_r2_mapping.py
set "EC=%ERRORLEVEL%"
echo.
if "%EC%"=="0" (
  echo [PASS] R1/R2 mapping generated under local_build\REMAKE_PROVEN45\mapping
) else (
  echo [STOP] Mapping collector failed. ExitCode=%EC%
)
pause
exit /b %EC%
