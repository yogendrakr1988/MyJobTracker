@echo off
REM ==========================================
REM Job Tracker Pro
REM Chrome ko "automation-ready" mode mein kholta hai
REM (remote-debugging-port ON), taaki whatsapp_selenium.py
REM isse JUD (attach) sake — naya window na khole.
REM
REM ISTEMAAL:
REM   1) Isse double-click karke Chrome kholein
REM   2) Usmein WhatsApp Web login kar lein (ek baar)
REM   3) Ise minimize kar sakte hain, lekin BAND NA KAREIN
REM   4) Ab jab bhi app se "Save & Send" karenge, message/resume
REM      isi Chrome mein nayi tab khol ke bheja jaayega
REM ==========================================

setlocal

set "PROFILE_DIR=%~dp0Data\whatsapp_chrome_profile"

if not exist "%PROFILE_DIR%" mkdir "%PROFILE_DIR%"

set "CHROME_PATH="

if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    set "CHROME_PATH=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
)

if not defined CHROME_PATH if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    set "CHROME_PATH=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
)

if not defined CHROME_PATH if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" (
    set "CHROME_PATH=%LocalAppData%\Google\Chrome\Application\chrome.exe"
)

if not defined CHROME_PATH (
    echo Chrome nahi mila is PC par. Pehle Google Chrome install karein.
    pause
    exit /b 1
)

echo Chrome khul raha hai (automation-ready mode)...
start "" "%CHROME_PATH%" --remote-debugging-port=9222 --user-data-dir="%PROFILE_DIR%" --profile-directory=Default

echo.
echo Ho gaya. Is Chrome window mein WhatsApp Web (web.whatsapp.com) login kar lein
echo (agar pehle se login nahi hai). Iske baad ise minimize kar sakte hain,
echo lekin band mat karein — Job Tracker Pro se sends isi mein/isi se jaayenge.
echo.
pause
