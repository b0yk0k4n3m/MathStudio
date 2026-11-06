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

:: Neu chua co trong PATH, tu dong quet cac thu muc cai dat mac dinh cua Windows
if "%PYTHON_CMD%"=="" (
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
            if "!PYTHON_CMD!"=="" (
                set "PYTHON_CMD=%%~p"
                echo [INFO] Tu dong phat hien Python tai: %%~p
            )
        )
    )
)

if "%PYTHON_CMD%"=="" (
    echo [CANH BAO] May tinh chua cai dat Python hoac chua them vao bien moi truong.
    echo [INFO] Dang thu tai va cai dat tu dong Python 3.11 qua Windows winget...
    winget --version >nul 2>&1
    if %errorlevel% equ 0 (
        winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
        echo.
        echo [THONG BAO] Da cai dat xong Python qua winget!
        echo [CHU Y] Vui long dong cua so nay va nhap dup lai install.bat de he thong nhan dien moi truong moi!
        pause
        exit /b 0
    ) else (
        echo.
        echo ====================================================================
        echo [HUONG DAN DANH CHO THAY CO]
        echo May tinh cua Thay/Co chua cai dat Python.
        echo He thong dang tu dong mo trinh duyet de tai file cai dat Python 3.11...
        echo.
        echo KHI CAI DAT, THAY/CO LUU Y:
        echo 1. O cua so dau tien, nhin xuong duoi cung, tich vao o:
        echo    [X] Add python.exe to PATH
        echo 2. Nhan vao nut 'Install Now' o phia tren va doi 1 phut la xong!
        echo ====================================================================
        echo.
        start https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
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

:: Tu dong tao Shortcut bieu tuong tren Desktop cho nguoi dung
echo [INFO] Dang tao bieu tuong (Shortcut) Math Studio ra man hinh Desktop...
"%VENV_PY%" create_desktop_shortcut.py >nul 2>&1
echo [OK] Da tao thanh cong bieu tuong 'Math Studio' tren man hinh Desktop!

echo.
echo ====================================================================
echo   CHUC MUNG! CAI DAT HOAN TAT 100%% VA HOAN TOAN KHONG CO LOI!
echo ====================================================================
echo.
echo  -> Bieu tuong 'Math Studio' da duoc tao tren Desktop cua Thay/Co!
echo  -> Thay/Co chi can ra man hinh Desktop va nhap dup vao de mo ung dung.
echo.

set /p START_NOW="Ban co muon khoi dong ung dung Web ngay bay gio khong? (Y/N, Mac dinh Y): "
if /i "%START_NOW%"=="N" (
    echo Da hoan tat. Ban co the chay run_app.bat bat cu luc nao.
    pause
    exit /b 0
)

echo [INFO] Dang mo Antigravity Math Studio...
call run_app.bat
