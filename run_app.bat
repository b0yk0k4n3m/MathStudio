@echo off
setlocal
title Antigravity Math Studio (THPT 2026)

echo ========================================================
echo   KHOI DONG ANTIGRAVITY MATH STUDIO (THPT 2026)
echo ========================================================
echo.

:: 1. Uu tien dung moi truong ao venv neu co
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

:: Neu chua co venv va PATH chua nhan, tu dong tim trong cac thu muc cai dat mac dinh
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
    echo ====================================================================
    echo [THONG BAO CHO THAY CO]
    echo May tinh chua cai dat Python hoac chua thiet lap moi truong Math Studio.
    echo.
    echo Thay/Co hay nhap dup chuot vao file 'install.bat' de he thong tu dong
    echo cai dat moi truong trong 1-2 phut nhe!
    echo ====================================================================
    echo.
    pause
    exit /b 1
)

:: 2. Kiem tra xem ung dung da dang chay tren port 8080 chua
netstat -ano | findstr :8080 | findstr LISTENING >nul 2>&1
if %errorlevel% equ 0 (
    echo [THONG BAO] Ung dung dang chay san tai http://localhost:8080 !
    echo [INFO] Dang mo trinh duyet...
    start http://localhost:8080
    exit /b 0
)

echo [INFO] Dang khoi dong may chu tai http://localhost:8080 ...
echo [TIP]  Nhan Ctrl+C de dung may chu.
echo.

"%PY_EXE%" app.py
pause
