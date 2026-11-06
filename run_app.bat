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

if "%PY_EXE%"=="" (
    echo [ERROR] Chua co moi truong Python hoac venv!
    echo [TIP]   Vui long nhap dup file 'install.bat' de cai dat tu dong 1-click.
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
    echo [TIP] Neu muon khoi dong lai toan bo, hay chay stop_app.bat truoc.
    echo.
    pause
    exit /b 0
)

echo [INFO] Dang khoi dong may chu tai http://localhost:8080 ...
echo [TIP]  Nhan Ctrl+C de dung may chu.
echo.

"%PY_EXE%" app.py
pause
