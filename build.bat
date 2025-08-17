@echo off
echo Building executable...
echo This might take a moment.

pyinstaller --noconfirm --onefile --windowed --icon=NONE gui.py

echo.
echo =================================================================
echo Build complete!
echo Your executable file can be found in the 'dist' folder.
echo =================================================================
echo.
pause
