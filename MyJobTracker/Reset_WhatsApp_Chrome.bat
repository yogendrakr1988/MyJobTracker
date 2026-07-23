@echo off
REM ==========================================
REM Job Tracker Pro
REM WhatsApp automation "stuck/invisible Chrome" ka ONE-CLICK fix
REM
REM KAB USE KAREIN:
REM   Agar "Save & Send" karne par Chrome na khulta dikhe, na koi
REM   error window aaye, ya WhatsApp message bhejne mein baar-baar
REM   "bubble confirm nahi hui" jaisi error aaye — iska matlab
REM   pichli baar ka ek "zombie" chrome.exe process background mein
REM   atka hua hai jo profile folder ko lock kiye baithha hai.
REM
REM YEH KYA KARTA HAI:
REM   1) Us profile folder se juda koi bhi chrome.exe process force-
REM      close karta hai (sirf automation wala Chrome, aapka normal
REM      roz wala Chrome iससे बिल्कुल touch nahi hota)
REM   2) Stale lock files (SingletonLock waghera) hata deta hai
REM   3) Aapka WhatsApp login/session SAFE rehta hai — dobara QR
REM      scan nahi karna padega, sirf atka hua process saaf hota hai
REM
REM Iske baad app ko dobara chalayein aur "Save & Send" try karein.
REM ==========================================

setlocal

set "PROFILE_DIR=%~dp0Data\whatsapp_chrome_profile"

echo Automation-wale Chrome ko dhoondh kar band kar rahe hain...
echo (Aapka normal/roz wala Chrome isse touch nahi hoga)
echo.

powershell -NoProfile -Command ^
    "Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | Where-Object { $_.CommandLine -and $_.CommandLine -like '*whatsapp_chrome_profile*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force; Write-Host ('Band kiya: PID ' + $_.ProcessId) }"

echo.
echo Stale lock files saaf kar rahe hain...

if exist "%PROFILE_DIR%\SingletonLock" del /f /q "%PROFILE_DIR%\SingletonLock"
if exist "%PROFILE_DIR%\SingletonCookie" del /f /q "%PROFILE_DIR%\SingletonCookie"
if exist "%PROFILE_DIR%\SingletonSocket" del /f /q "%PROFILE_DIR%\SingletonSocket"

echo.
echo Ho gaya! Aapka WhatsApp login session safe hai (dobara QR nahi
echo maangega). Ab Job Tracker Pro app ko dobara chalayein aur
echo "Save & Send" try karein.
echo.
pause
