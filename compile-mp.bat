@echo off

REM Compile the Python script into an executable
pyinstaller --onefile --add-data "mp_autocomplete.bat:." minimalplayer.py

REM Remove the build directory and the spec file if they exist
rd /s /q "%cd%\build"
del "%cd%\minimalplayer.spec"
move "%cd%\dist\minimalplayer.exe" "%cd%"
rd /s /q "%cd%\dist"