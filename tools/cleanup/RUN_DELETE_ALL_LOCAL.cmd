@echo off
title DLTB TOTAL CLEAN - DELETE ALL LOCAL
echo ==============================================================
echo  DLTB TOTAL CLEAN - DELETE ALL LOCAL
echo ==============================================================
echo.
echo WAJIB SEBELUM LANJUT:
echo 1. Uninstall DLTB dari Steam.
echo 2. Steam Cloud DLTB = OFF.
echo 3. Steam ^> Exit sampai benar-benar tertutup.
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0DLTB_TOTAL_CLEAN.ps1" -Mode Delete
set EC=%ERRORLEVEL%
echo.
echo ExitCode=%EC%
pause
exit /b %EC%
