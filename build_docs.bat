@echo off
REM Build documentation script for Windows

echo Building COMET SDKP Documentation...
echo ======================================

cd docs

echo Cleaning previous builds...
if exist _build rmdir /s /q _build

echo Building HTML documentation...
call make.bat html

echo.
echo Documentation built successfully!
echo.
echo View the documentation at:
echo   %CD%\_build\html\index.html
echo.
pause