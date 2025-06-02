@echo off
setlocal enabledelayedexpansion

title "Doc Project Tool - Setup & Launch (DEBUG NGAM)"

echo.
echo  =====================================================
echo    DOC PROJECT TOOL - KHOI DONG VA CAI DAT (WINDOWS)
echo  =====================================================
echo  [DEBUG NGAM MODE - PAUSE SAU TUNG LENH NHO]
echo.

set "SCRIPT_DIR=%~dp0"
cd /D "%SCRIPT_DIR%.."
echo.

set "VENV_NAME=moitruongao"
set "PYTHON_EXE_FOUND=" 
set "PYTHONW_EXE_TO_USE=pythonw" REM Mac dinh
echo.



call :checkPython
if "!PYTHON_EXE_FOUND!"=="" (
    echo  [LOI] Subroutine khong tim thay Python hoac loi.
    exit /b 1
)

echo  [OK] Da tim thay Python: !PYTHON_EXE_FOUND!

set "PYTHON_EXE=!PYTHON_EXE_FOUND!"
if "!PYTHON_EXE!"=="python3" (
    set "PYTHONW_EXE_TO_USE=pythonw3"
)


echo  [KTR] Kiem tra moi truong ao '%VENV_NAME%'...
if not exist "%VENV_NAME%\Scripts\activate.bat" (
    echo  [THONG TIN] Moi truong ao '%VENV_NAME%' chua co. Dang tao...
    !PYTHON_EXE! -m venv "%VENV_NAME%"
    if %errorlevel% neq 0 (
        echo  [LOI] Tao moi truong ao that bai.
        pause; exit /b 1
    )
    echo  [OK] Da tao moi truong ao '%VENV_NAME%'.
) else (
    echo  [OK] Moi truong ao '%VENV_NAME%' da ton tai.
)
echo.

echo  [THUC HIEN] Kich hoat moi truong ao va cai dat thu vien...
call "%VENV_NAME%\Scripts\activate.bat"

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo  [LOI] Cai dat thu vien that bai.
    pause; call "%VENV_NAME%\Scripts\deactivate.bat"; exit /b 1
)
echo  [OK] Thu vien da duoc cai dat/kiem tra.
echo.


start "DocProjectToolApp_Test1" /B !PYTHON_EXE! -m Core.run_app


!PYTHONW_EXE_TO_USE! -m Core.run_app


echo [DEBUG CMD - TEST 3] start "DocProjectToolApp_Test3" /B !PYTHONW_EXE_TO_USE! -m Core.run_app
start "DocProjectToolApp_Test3" /B !PYTHONW_EXE_TO_USE! -m Core.run_app


echo [DEBUG CMD] call "%VENV_NAME%\Scripts\deactivate.bat"
call "%VENV_NAME%\Scripts\deactivate.bat"


endlocal
goto :eof

REM ==================================================================
:checkPython
setlocal
set "_py_exe_to_check=python"
%_py_exe_to_check% --version >nul 2>&1
if %errorlevel% equ 0 (
    endlocal & set "PYTHON_EXE_FOUND=%_py_exe_to_check%"
    goto :eof
)

set "_py_exe_to_check=python3"
%_py_exe_to_check% --version >nul 2>&1
if %errorlevel% equ 0 (
    endlocal & set "PYTHON_EXE_FOUND=%_py_exe_to_check%"
    goto :eof
)

endlocal & set "PYTHON_EXE_FOUND="
goto :eof
REM ==================================================================
