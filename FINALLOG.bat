@echo off
setlocal

REM Set the log file path and name
set "LOGFILE=C:\Users\File.txt"

REM Clear the log file if it already exists
if exist "%LOGFILE%" del "%LOGFILE%"

REM Loop to read and execute commands from the user
:inputLoop
setlocal enabledelayedexpansion
for /f %%a in ('wmic os get localdatetime ^| find "."') do (
    set datetime=%%a
)
set "YYYY=%datetime:~0,4%"
set "MM=%datetime:~4,2%"
set "DD=%datetime:~6,2%"
set "HH=%datetime:~8,2%"
set "MIN=%datetime:~10,2%"
set "SEC=%datetime:~12,2%"
endlocal & (
    set "YEAR=%YYYY%"
    set "MONTH=%MM%"
    set "DAY=%DD%"
    set "HOUR=%HH%"
    set "MINUTE=%MIN%"
    set "SECOND=%SEC%"
)

:inputLoop
set /p "CMD=Enter a command (or type 'exit' to quit): "
if /i "%CMD%"=="exit" (
    goto :eof
)
echo Running command: %CMD%
echo Date and Time: %YEAR%-%MONTH%-%DAY% %HOUR%:%MINUTE%:%SECOND%
echo ---------------------------------------
%CMD% 2>&1
%CMD% 2>&1 >> "%LOGFILE%"
echo. >> "%LOGFILE%"
goto inputLoop

:end
