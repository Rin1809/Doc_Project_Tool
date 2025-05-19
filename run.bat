@echo off

:: Tên môi trường ảo
set VENV_NAME=moitruongao

:: Kiểm tra xem môi trường ảo đã tồn tại chưas
IF EXIST "%VENV_NAME%\Scripts\activate" (
    echo Dang khoi dong moi truong ao...
    call "%VENV_NAME%\Scripts\activate"
) ELSE (
    echo Khong tim thay moi truong ao. Tu dong tao...
    python -m venv %VENV_NAME%
    IF ERRORLEVEL 1 (
        echo Loi: Khong the tao moi truong ao. Vui long kiem tra Python da duoc them vao PATH.
        pause
        exit /b 1
    )
    call "%VENV_NAME%\Scripts\activate"
    echo Dang Tai Thu Vien..
    pip install -r requirements.txt
    IF ERRORLEVEL 1 (
        echo Loi: Khong the tai thu vien. Vui long kiem tra ket noi mang va file requirements.txt.
        pause
        exit /b 1
    )
)

:: Chạy ứng dụng bằng pythonw.exe để không hiển thị console
echo Dang Chay Ung Dung...
start "DocProjectTool" /B "%VENV_NAME%\Scripts\pythonw.exe" -m Core.run_app
