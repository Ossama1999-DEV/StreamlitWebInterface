@echo off
setlocal enabledelayedexpansion

REM ───────────────────────────────────────────────
REM Install dependencies if not already present
REM ───────────────────────────────────────────────
pip install -r requirements.txt --user >nul 2>&1

REM ───────────────────────────────────────────────
REM Ask user whether to change default Excel file
REM ───────────────────────────────────────────────
:ask
set /p yn=Do you want to change the default Excel file (AOCS_equipment.xlsx)? [y/n] 
if /i "%yn%"=="y" goto yes
if /i "%yn%"=="n" goto no
echo Please answer y or n.
goto ask

:yes
set /p xls_file=Enter the full path of the Excel file: 
if exist "%xls_file%" (
    set "STREAMLIT_XLS_FILE=%xls_file%"
) else (
    echo File not found. Using the default file instead.
    set "STREAMLIT_XLS_FILE=AOCS_equipment.xlsx"
)
goto launch

:no
set "STREAMLIT_XLS_FILE=AOCS_equipment.xlsx"

:launch
REM ───────────────────────────────────────────────
REM Run Streamlit with no browser prompt
REM ───────────────────────────────────────────────
echo Launching Streamlit with file: %STREAMLIT_XLS_FILE%

set "STREAMLIT_XLS_FILE=%STREAMLIT_XLS_FILE%"

streamlit run app.py ^
    --browser.gatherUsageStats=false ^
    --server.headless=false ^
    --server.enableCORS=false ^
    --server.runOnSave=false ^
    --global.developmentMode=false ^
    --browser.serverAddress=localhost ^
    --browser.serverPort=8501 ^
    > streamlit_output.log 2> streamlit_error.log

REM Exit if Streamlit stops (e.g., browser closed)
IF %ERRORLEVEL% NEQ 0 (
    echo Streamlit has exited. Possibly the browser was closed.
    exit /b %ERRORLEVEL%
)
