:: This file is part of MinimalPlayer.
::
:: MinimalPlayer is free software: you can redistribute it and/or modify either this part (mp_autocomplete) of the software and/or this whole software under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
:: 
:: MinimalPlayer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
::
:: You should have received a copy of the GNU General Public License (LICENSE) along with this project. If not, see <https://www.gnu.org/licenses/>.
::
:: You should also have a copy of the main python script (minimalplayer.py) if you're downloading the source.

@echo off
setlocal enabledelayedexpansion

set "PROMPT=Enter the audio file path: "

:loop
set /p "input=%PROMPT%"
if exist "!input!" (
    echo !input! > "%TEMP%\filename_output.txt"
    goto end
) else (
    echo File not found. Please try again.
    goto loop
)

:end
endlocal