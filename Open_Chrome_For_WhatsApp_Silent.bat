@echo off
REM ==========================================
REM Job Tracker Pro
REM SILENT / AUTOSTART version of
REM Open_Chrome_For_WhatsApp.bat
REM
REM Yeh file khud se kabhi double-click NAHI
REM karni - isse "Install_AutoStart.bat" use
REM karta hai taaki Windows start hote hi
REM WhatsApp-ready Chrome minimized khud khul
REM jaaye, koi "pause" screen ya console
REM window dikhe bina.
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

REM Chrome nahi mila toh chup-chaap exit (autostart mein koi popup/pause
REM nahi dikhana chahte - agar chahiye toh normal
REM Open_Chrome_For_WhatsApp.bat manually chalayein, woh error dikhayega).
if not defined CHROME_PATH exit /b 1

start /min "" "%CHROME_PATH%" --remote-debugging-port=9222 --user-data-dir="%PROFILE_DIR%" --profile-directory=Default
