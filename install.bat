@echo off
setlocal enabledelayedexpansion
title Cai Dat Tu Dong - Antigravity Math Studio (THPT 2026)

echo ====================================================================
echo    CAI DAT TU DONG ANTIGRAVITY MATH STUDIO (ONE-CLICK INSTALLER)
echo ====================================================================
echo.

:: ----------------------------------------------------------------------
:: BUOC 1: KIEM TRA PYTHON TREN HE THONG
:: ----------------------------------------------------------------------
echo [BUOC 1/5] Dang kiem tra moi truong Python...

set PYTHON_CMD=
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    py --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=py
    )
)

if "%PYTHON_CMD%"=="" (
    echo [CANH BAO] Khong tim thay Python trong PATH he thong!
    echo [INFO] Dang thu cai dat Python 3.11 bang cong cu Windows winget...
    winget --version >nul 2>&1
    if %errorlevel% equ 0 (
        winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
        echo.
        echo [THONG BAO] Da cai dat xong Python qua winget.
        echo [CHU Y] Vui long dong cua so nay va chay lai install.bat de he thong nhan dien PATH moi!
        pause
        exit /b 0
    ) else (
        echo [ERROR] May tinh chua co Python va khong co winget!
        echo Vui long tai va cai dat Python 3.10+ tu trang chu: https://www.python.org/downloads/
        echo (Nho tich chon: "Add Python to PATH" khi cai dat)
        echo.
        pause
        exit /b 1
    )
)

for /f "tokens=*" %%v in ('%PYTHON_CMD% --version') do set PY_VER=%%v
echo [OK] Phat hien: %PY_VER%
echo.

:: ----------------------------------------------------------------------
:: BUOC 2: TAO MOI TRUONG AO (VIRTUAL ENVIRONMENT)
:: ----------------------------------------------------------------------
echo [BUOC 2/5] Dang thiet lap moi truong ao (venv)...

if not exist "venv\Scripts\python.exe" (
    echo [INFO] Dang khoi tao thu muc venv rieng biet cho du an...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Khong the tao virtual environment. Vui long kiem tra quyen ghi thu muc!
        pause
        exit /b 1
    )
    echo [OK] Da khoi tao moi truong ao thanh cong.
) else (
    echo [OK] Da ton tai moi truong ao venv san co.
)
echo.

:: ----------------------------------------------------------------------
:: BUOC 3: CAI DAT CAC THU VIEN PHU THUOC (REQUIREMENTS)
:: ----------------------------------------------------------------------
echo [BUOC 3/5] Dang cai dat/nang cap cac thu vien can thiet...
echo (Qua trinh nay mat khoang 1 - 2 phut tuy toc do mang, vui long doi...)
echo.

set VENV_PY=venv\Scripts\python.exe
set VENV_PIP=venv\Scripts\pip.exe

"%VENV_PY%" -m pip install --upgrade pip --quiet
"%VENV_PY%" -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo.
    echo [CANH BAO] Co canh bao khi cai dat, dang thu lai che do chi tiet...
    "%VENV_PY%" -m pip install -r requirements.txt
)
echo [OK] Toan bo thu vien Toan hoc, NiceGUI, SymPy, Docx da cai dat xong!
echo.

:: ----------------------------------------------------------------------
:: BUOC 4: KHOI TAO CAU TRUC THU MUC VA BIEN MOI TRUONG
:: ----------------------------------------------------------------------
echo [BUOC 4/5] Dang kiem tra va khoi tao cau truc thu muc du an...

if not exist "input" mkdir input
if not exist "input\blueprint_images" mkdir input\blueprint_images
if not exist "output" mkdir output
if not exist "output\images" mkdir output\images
if not exist "output\history" mkdir output\history
if not exist "output\scripts" mkdir output\scripts

if not exist ".env" (
    if exist ".env.example" (
        copy /y ".env.example" ".env" >nul
        echo [INFO] Da tu dong tao file cau hinh .env tu .env.example.
    )
)
echo [OK] Thu muc lam viec da san sang!
echo.

:: ----------------------------------------------------------------------
:: BUOC 5: KIEM TRA TINH TOAN VEN (SANITY CHECK)
:: ----------------------------------------------------------------------
echo [BUOC 5/5] Dang kiem tra tinh toan ven cua he thong...

"%VENV_PY%" -c "import nicegui, sympy, docx, matplotlib, numpy, markdown2; print('   -> All core packages imported successfully!')"
if %errorlevel% neq 0 (
    echo [ERROR] Phat hien loi khi nap thu vien. Vui long kiem tra log o tren!
    pause
    exit /b 1
)

echo.
echo ====================================================================
echo   CHUC MUNG! CAI DAT HOAN TAT 100%% VA HOAN TOAN KHONG CO LOI!
echo ====================================================================
echo.
echo Ban co the bat dau su dung he thong ngay:
echo  1. Dung Antigravity CLI: go 'agy' roi nhap '/tao-de' de tao de tu dong.
echo  2. Dung Giao dien Web:   nhap dup file 'run_app.bat' (http://localhost:8080).
echo.

set /p START_NOW="Ban co muon khoi dong ung dung Web ngay bay gio khong? (Y/N, Mac dinh Y): "
if /i "%START_NOW%"=="N" (
    echo Da hoan tat. Ban co the chay run_app.bat bat cu luc nao.
    pause
    exit /b 0
)

echo [INFO] Dang mo Antigravity Math Studio...
call run_app.bat
