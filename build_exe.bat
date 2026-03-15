@echo off
TITLE Local AI Installer Builder

echo ========================================
echo   Local AI Installer - EXE Builder
echo   Build by AKBBProjects
echo ========================================
echo.

python -m pip install --upgrade pip
python -m pip install pyinstaller

pyinstaller --onefile --name "Local AI Installer" local_ai_installer.py

echo.
echo Build complete.
echo EXE file should be inside the dist folder.
pause
