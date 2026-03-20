@echo off
setlocal
cd /d "%~dp0"
title SootoPYlis Launcher

set "SYSTEM_PYTHON=python"
set "VENV_PYTHON=%~dp0.venv\Scripts\python.exe"
set "PYTHON_CMD=%SYSTEM_PYTHON%"

call :check_pyside "%SYSTEM_PYTHON%"
if errorlevel 1 (
  if exist "%VENV_PYTHON%" (
    call :check_pyside "%VENV_PYTHON%"
    if not errorlevel 1 set "PYTHON_CMD=%VENV_PYTHON%"
  )
)

set "PYTHONUNBUFFERED=1"

echo SootoPYlis desktop launcher
echo Using Python: %PYTHON_CMD%
echo.

"%PYTHON_CMD%" desktop_probe.py
if errorlevel 1 (
  echo.
  echo Desktop probe failed.
  pause
  exit /b %errorlevel%
)

echo.
echo Launching desktop app...
"%PYTHON_CMD%" run_desktop.py
set "EXIT_CODE=%ERRORLEVEL%"

echo.
echo Desktop app exited with code %EXIT_CODE%.

if not "%EXIT_CODE%"=="0" (
  echo.
  echo Desktop app failed to launch.
)

echo.
echo Press any key to close this launcher.
pause >nul
exit /b %EXIT_CODE%

:check_pyside
"%~1" -c "import importlib.util, site, sys; sys.path.append(site.getusersitepackages()); raise SystemExit(0 if importlib.util.find_spec('PySide6') else 1)" >nul 2>nul
exit /b %ERRORLEVEL%
