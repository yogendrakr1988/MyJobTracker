@echo off
REM ==========================================
REM Job Tracker Pro
REM Uninstall AutoStart
REM
REM Isse chalane par Windows Startup se woh
REM shortcut hata di jaati hai jo
REM Install_AutoStart.bat ne banaya tha. Uske
REM baad PC start hone par Chrome khud nahi
REM khulega - manually Open_Chrome_For_WhatsApp.bat
REM chalana padega.
REM ==========================================

setlocal

set "SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\JobTracker_WhatsApp_AutoStart.lnk"

if exist "%SHORTCUT%" (
    del "%SHORTCUT%"
    echo.
    echo  Auto-start hata diya gaya. Ab PC start hone par Chrome khud nahi khulega.
    echo.
) else (
    echo.
    echo  Auto-start pehle se set nahi tha - hatane ke liye kuch nahi hai.
    echo.
)

pause
