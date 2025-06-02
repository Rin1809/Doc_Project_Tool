@echo off
setlocal

:: Duong dan den thu muc chua script nay
set SCRIPT_DIR=%~dp0
:: Di chuyen len thu muc goc cua du an (Doc_Project_Tool)
cd /D "%SCRIPT_DIR%\" 

:: Ten moi truong ao
set VENV_NAME=moitruongao
set PYTHON_EXE_IN_VENV=%VENV_NAME%\Scripts\python.exe
set PYTHONW_EXE_IN_VENV=%VENV_NAME%\Scripts\pythonw.exe

:: Kiem tra Python he thong
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python khong duoc cai dat hoac khong co trong PATH. Vui long cai dat Python.
    pause
    exit /b 1
)

:: Kiem tra va tao moi truong ao neu chua co
IF NOT EXIST "%VENV_NAME%\Scripts\activate.bat" (
    echo Tao moi truong ao: %VENV_NAME%...
    python -m venv %VENV_NAME%
    IF ERRORLEVEL 1 (
        echo Loi: Khong the tao moi truong ao.
        pause
        exit /b 1
    )
    echo Moi truong ao da duoc tao.
)

:: Kich hoat moi truong ao
echo Kich hoat moi truong ao...
call "%VENV_NAME%\Scripts\activate.bat"
IF ERRORLEVEL 1 (
    echo Loi: Khong the kich hoat moi truong ao.
    pause
    exit /b 1
)

:: Cai dat cac thu vien
echo Dang tai cac thu vien tu requirements.txt...
pip install -r requirements.txt
IF ERRORLEVEL 1 (
    echo Loi: Khong the tai thu vien. Vui long kiem tra ket noi mang va file requirements.txt.
    pause
    exit /b 1
)

:: Chay ung dung
echo Dang chay ung dung Doc_Project_Tool (PySide6)...
IF EXIST "%PYTHONW_EXE_IN_VENV%" (
    start "DocProjectTool" /B "%PYTHONW_EXE_IN_VENV%" -m Core.run_app
) ELSE (
    echo Warning: Khong tim thay pythonw.exe, su dung python.exe (console se hien thi).
    start "DocProjectTool" "%PYTHON_EXE_IN_VENV%" -m Core.run_app
)

:: Khong can pause o day, start /B se chay nen

endlocal
exit /b 0