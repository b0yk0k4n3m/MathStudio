@echo off
setlocal
echo ========================================================
echo   TAT TIEN TRINH MATH STUDIO (GIAI PHONG PORT 8080)
echo ========================================================
echo.

set FOUND=0
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do (
    set PID=%%a
    set FOUND=1
)

if "%FOUND%"=="1" (
    echo [INFO] Tim thay tien trinh dang chiem port 8080 (PID: %PID%).
    echo [INFO] Dang dung tien trinh...
    taskkill /F /PID %PID%
    echo [THANH CONG] Da giai phong port 8080 thanh cong!
) else (
    echo [THONG BAO] Port 8080 hien dang trong, khong co tien trinh nao chiem dung.
)

echo.
pause
