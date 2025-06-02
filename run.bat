@echo off
setlocal

:: Duong dan den thu muc chua script nay
set SCRIPT_DIR=%~dp0
:: Di chuyen len thu muc goc cua du an (Doc_Project_Tool)
echo Script directory: %SCRIPT_DIR%
cd /D "%SCRIPT_DIR%" 
echo Current directory set to: %CD%

:: Ten moi truong ao
set VENV_NAME=moitruongao
set PYTHON_EXE_PATH_IN_VENV=%CD%\%VENV_NAME%\Scripts\python.exe
set PYTHONW_EXE_PATH_IN_VENV=%CD%\%VENV_NAME%\Scripts\pythonw.exe

:: Kiem tra Python he thong
echo Checking for system Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not found in system PATH.
    echo Please install Python (3.8+ recommended) and ensure it's added to PATH.
    pause
    exit /b 1
)
echo System Python found.

:: Kiem tra va tao moi truong ao neu chua co
IF NOT EXIST "%CD%\%VENV_NAME%\Scripts\activate.bat" (
    echo Virtual environment '%VENV_NAME%' not found. Creating...
    python -m venv %VENV_NAME%
    IF ERRORLEVEL 1 (
        echo ERROR: Failed to create virtual environment '%VENV_NAME%'.
        pause
        exit /b 1
    )
    echo Virtual environment '%VENV_NAME%' created successfully.
) ELSE (
    echo Virtual environment '%VENV_NAME%' already exists.
)

:: Kich hoat moi truong ao
echo Activating virtual environment '%VENV_NAME%'...
call "%CD%\%VENV_NAME%\Scripts\activate.bat"
IF ERRORLEVEL 1 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)
echo Virtual environment activated.

:: Cai dat cac thu vien
echo Installing required libraries from requirements.txt...
"%CD%\%VENV_NAME%\Scripts\pip.exe" install -r requirements.txt
IF ERRORLEVEL 1 (
    echo ERROR: Failed to install libraries from requirements.txt.
    echo Please check your internet connection and the content of requirements.txt.
    pause
    exit /b 1
)
echo Libraries installed successfully.

:: Chay ung dung
echo Starting Doc_Project_Tool (PySide6)...
IF EXIST "%PYTHONW_EXE_PATH_IN_VENV%" (
    echo Using pythonw.exe (no console window).
    start "DocProjectTool" "%PYTHONW_EXE_PATH_IN_VENV%" -m Core.run_app
) ELSE (
    echo WARNING: pythonw.exe not found in virtual environment.
    echo Using python.exe (a console window will remain open).
    start "DocProjectTool" "%PYTHON_EXE_PATH_IN_VENV%" -m Core.run_app
)

IF ERRORLEVEL 1 (
    echo ERROR: Failed to start the application using the 'start' command.
    echo This might indicate an issue with the Python environment or the application itself.
    pause
    exit /b 1
)

echo Application launch initiated. If it does not appear, check for errors in any new console windows.
endlocal
exit /b 0