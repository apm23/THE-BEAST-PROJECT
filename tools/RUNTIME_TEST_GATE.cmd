@echo off
setlocal
cd /d "%~dp0.."
if "%~1"=="" goto :help
python tools\runtime_test_gate.py %*
exit /b %ERRORLEVEL%

:help
echo Usage:
echo   tools\RUNTIME_TEST_GATE.cmd init
echo   tools\RUNTIME_TEST_GATE.cmd pass T01 --note "boot normal"
echo   tools\RUNTIME_TEST_GATE.cmd fail T03 --note "corpse F missing"
echo   tools\RUNTIME_TEST_GATE.cmd hard-fail --note "save corrupted"
echo   tools\RUNTIME_TEST_GATE.cmd status
echo   tools\RUNTIME_TEST_GATE.cmd promote
echo   tools\RUNTIME_TEST_GATE.cmd reset
exit /b 1
