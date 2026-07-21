@echo off
REM ==========================================
REM Job Tracker Pro
REM Install AutoStart
REM
REM Isse ek hi baar double-click karein - yeh
REM Windows ke "Startup" folder mein ek shortcut
REM daal deta hai jo har PC-restart/login par
REM khud-ba-khud WhatsApp-ready Chrome (minimized)
REM khol dega. Ab dobara manually
REM Open_Chrome_For_WhatsApp.bat chalane ki
REM zaroorat NAHI padegi.
REM
REM Hatana ho toh: Uninstall_AutoStart.bat chalayein.
REM ==========================================

setlocal

set "SCRIPT_DIR=%~dp0"
set "TARGET=%SCRIPT_DIR%Open_Chrome_For_WhatsApp_Silent.bat"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP_DIR%\JobTracker_WhatsApp_AutoStart.lnk"
set "VBS=%TEMP%\_jobtracker_make_shortcut.vbs"

if not exist "%TARGET%" (
    echo Error: Open_Chrome_For_WhatsApp_Silent.bat isi folder mein nahi mili.
    echo Is Install_AutoStart.bat ko MyJobTracker folder ke andar hi rakh kar chalayein.
    pause
    exit /b 1
)

> "%VBS%" echo Set oWS = WScript.CreateObject("WScript.Shell")
>> "%VBS%" echo sLinkFile = "%SHORTCUT%"
>> "%VBS%" echo Set oLink = oWS.CreateShortcut(sLinkFile)
>> "%VBS%" echo oLink.TargetPath = "%TARGET%"
>> "%VBS%" echo oLink.WorkingDirectory = "%SCRIPT_DIR%"
>> "%VBS%" echo oLink.WindowStyle = 7
>> "%VBS%" echo oLink.Description = "Job Tracker Pro - Auto-open WhatsApp Chrome at startup"
>> "%VBS%" echo oLink.Save

cscript //nologo "%VBS%" >nul 2>&1
del "%VBS%" >nul 2>&1

if exist "%SHORTCUT%" (
    echo.
    echo  Ho gaya! Ab jab bhi is PC ko start/restart karoge ya login karoge,
    echo  WhatsApp-ready Chrome khud-ba-khud (minimized) khul jaayega.
    echo.
    echo  Bas ek baar, uske andar WhatsApp Web login kar lena hai (agar
    echo  pehle se logged in nahi hai) - uske baad sab automatic chalega.
    echo.
    echo  Isse hatana ho toh: Uninstall_AutoStart.bat chalayein.
    echo.
) else (
    echo.
    echo  Kuch gadbad hui, shortcut nahi ban paaya. Manually bhi kar sakte
    echo  hain: Open_Chrome_For_WhatsApp_Silent.bat ka shortcut bana kar
    echo  isi folder mein paste karein -
    echo  %STARTUP_DIR%
    echo.
)

pause
