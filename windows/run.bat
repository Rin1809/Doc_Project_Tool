@echo off
setlocal

set SCRIPT_DIR=%~dp0
cd /D "%SCRIPT_DIR%.."

set VENV_NAME=moitruongao
set PYTHON_EXE_IN_VENV=%VENV_NAME%\Scripts\python.exe
set PYTHONW_EXE_IN_VENV=%VENV_NAME%\Scripts\pythonw.exe
set MAIN_SCRIPT=run_app.py

echo ===========================================================
echo Doc_Project_Tool Setup & Run Script for Windows
echo ===========================================================
echo Project Root: %CD%
echo Virtual Environment: %VENV_NAME%
echo Main Script: %MAIN_SCRIPT%
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ===========================================================
    echo ERROR: Python is not installed or not found in PATH.
    echo Please install Python and ensure it's added to your PATH.
    echo ===========================================================
    pause
    exit /b 1
)
echo Python installation found.
echo.

if not exist "%VENV_NAME%\Scripts\activate.bat" (
    echo ===========================================================
    echo Creating virtual environment: %VENV_NAME%...
    echo ===========================================================
    python -m venv %VENV_NAME%
    if %errorlevel% neq 0 (
        echo ===========================================================
        echo ERROR: Failed to create virtual environment.
        echo Please check your Python installation and permissions.
        echo ===========================================================
        pause
        exit /b 1
    )
    echo ===========================================================
    echo Virtual environment created successfully.
    echo ===========================================================
    echo.
) else (
    echo Virtual environment '%VENV_NAME%' already exists.
    echo.
)

echo ===========================================================
echo Activating virtual environment...
echo ===========================================================
call "%VENV_NAME%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo ===========================================================
    echo ERROR: Failed to activate virtual environment.
    echo ===========================================================
    pause
    exit /b 1
)
echo Virtual environment activated.
echo.

echo ===========================================================
echo Installing dependencies from requirements.txt...
echo ===========================================================
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ===========================================================
    echo ERROR: Failed to install dependencies.
    echo Please check requirements.txt and your internet connection.
    echo ===========================================================
    pause
    exit /b 1
)
echo Dependencies installed successfully.
echo.

echo ===========================================================
echo Running Doc_Project_Tool application...
echo (This terminal window will close shortly)
echo ===========================================================

if exist "%PYTHONW_EXE_IN_VENV%" (
    start "DocProjectTool" /B "%PYTHONW_EXE_IN_VENV%" "%MAIN_SCRIPT%"
) else if exist "%PYTHON_EXE_IN_VENV%" (
    start "DocProjectTool" /B "%PYTHON_EXE_IN_VENV%" "%MAIN_SCRIPT%"
) else (
    echo ===========================================================
    echo ERROR: Python executable not found in virtual environment.
    echo %PYTHON_EXE_IN_VENV%
    echo ===========================================================
    pause
    exit /b 1
)

timeout /t 2 /nobreak > nul

endlocal
exit /b 0