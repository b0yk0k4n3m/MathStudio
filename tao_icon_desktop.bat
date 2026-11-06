@echo off
setlocal enabledelayedexpansion
title Tao Bieu Tuong Math Studio Tren Desktop

echo ========================================================
echo   TAO BIEU TUONG (ICON) MATH STUDIO TREN MAN HINH DESKTOP
echo ========================================================
echo.

set PY_EXE=
if exist "venv\Scripts\python.exe" (
    set PY_EXE=venv\Scripts\python.exe
) else (
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PY_EXE=python
    ) else (
        py --version >nul 2>&1
        if %errorlevel% equ 0 (
            set PY_EXE=py
        )
    )
)

if "%PY_EXE%"=="" (
    for %%p in (
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        "%ProgramFiles%\Python312\python.exe"
        "%ProgramFiles%\Python311\python.exe"
        "%ProgramFiles%\Python310\python.exe"
        "C:\Python312\python.exe"
        "C:\Python311\python.exe"
        "C:\Python310\python.exe"
    ) do (
        if exist %%p (
            if "!PY_EXE!"=="" (
                set "PY_EXE=%%~p"
            )
        )
    )
)

if "%PY_EXE%"=="" (
    echo [ERROR] Chua tim thay Python de tao shortcut!
    echo Thay/Co hay chay install.bat truoc nhe.
    pause
    exit /b 1
)

"%PY_EXE%" create_desktop_shortcut.py
echo.
echo ========================================================
echo [HOAN TAT] Thay/Co hay ra man hinh Desktop de xem bieu tuong
echo 'Math Studio' voi icon toan hoc tuyet dep nhe!
echo Tu nay chi can nhap dup vao bieu tuong do de mo phan mem!
echo ========================================================
echo.
pause
