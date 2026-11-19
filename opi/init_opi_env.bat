@echo off
setlocal

set "OPI_DIR=%~dp0"
if "%OPI_DIR:~-1%"=="\" set "OPI_DIR=%OPI_DIR:~0,-1%"

echo Setting OPI folder to: %OPI_DIR%
setx OPI_HOME "%OPI_DIR%"
setx OPI_HOME_ELI "%OPI_DIR%"

echo Done. Open a NEW terminal before launching Phoebus.
pause