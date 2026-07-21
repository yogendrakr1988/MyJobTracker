"""
==========================================
Job Tracker Pro
WhatsApp Web Automation (Selenium)
Developer : Yogendra Kumar
==========================================

YEH FILE KYA KARTI HAI
-----------------------
Selenium ek real Chrome browser ko control karta hai — pyautogui ki tarah
"screen par blind click" nahi karta. Yeh browser ke andar ka HTML (DOM)
padhta hai aur usi se button/box dhoondta hai, isliye:
  - Screen resolution / zoom / window position se koi farak nahi padta
  - Login ek baar QR scan karne ke baad, agli baar se automatic hota hai
    (Chrome ek fixed "profile folder" use karta hai jisme session save
    rehta hai — bilkul waise hi jaise normal Chrome mein login yaad
    rehta hai)
  - Resume file bhi attach ho sakti hai (hidden <input type="file">
    element mein seedha path daal ke), na ki sirf text message

FLOW (send_whatsapp_message ke andar)
--------------------------------------
0) Sabse pehle check karta hai ki koi "automation-ready" Chrome pehle se
   khula hai ya nahi (isi tool se pehle khola gaya, ya Open_Chrome.bat
   se). Agar khula hai, toh USI Chrome mein ek nayi tab kholta hai —
   naya Chrome window nahi khulta, aur agar us Chrome mein WhatsApp Web
   pehle se login/open hai, toh woh disturb nahi hota.
   Agar koi aisa Chrome nahi mila, tabhi ek naya Chrome khulta hai — aur
   is baar isse hamesha khula chhod deta hai (band nahi karta), taaki
   agli baar wahi window mil jaaye aur phir se naya na khulna pade.
1) web.whatsapp.com/send?phone=...&text=... link kholta hai (isse
   contact search karne ki zaroorat nahi padti, seedha chat khul jaati
   hai aur message box mein text pehle se bhara hota hai)
2) Pehli baar hai toh QR scan hone ka wait karta hai (up to 2 minute)
3) Message box load hone ka wait karta hai, phir Send button dhoondh ke
   click karta hai
4) Agar resume path diya gaya hai: Paperclip -> Document -> hidden file
   input mein resume ka poora path daalta hai -> Send button click

IMPORTANT — "already open Chrome" wala sach
---------------------------------------------
Selenium sirf us Chrome se JUD (attach) sakta hai jo "debugging mode"
(--remote-debugging-port) ke saath khula ho — yeh Chrome/DevTools ki
apni limitation hai, koi bhi automation tool isse bypass nahi kar
sakta. Iska matlab: agar aapne Chrome apne normal Desktop icon se khola
hai (roz wali browsing wala), toh script us tab se seedhe jud NAHI
sakta.

Fix: is folder mein `Open_Chrome_For_WhatsApp.bat` file hai — usse
double-click karke Chrome kholein (ek hi baar), usi mein WhatsApp Web
login rehne dein, aur use hi apna "WhatsApp Chrome" bana lein (minimize
kar sakte hain, band mat karein). Agli baar se script isi Chrome mein
tab khol ke bhejega — na koi naya window, na dobara QR.

Agar yeh .bat file kabhi na chalayein, tab bhi sab kaam karega — script
khud apna alag Chrome window bana lega aur use hamesha khula chhod
dega, taaki agli baar wahi reuse ho.

==========================================
MAINTENANCE — IMPORTANT
==========================================
WhatsApp Web samay-samay par apna HTML/CSS badalta rehta hai (jab bhi
WhatsApp koi naya UI feature launch karta hai). Jab aisa hota hai, neeche
SELECTORS dictionary mein diye XPATHs kaam karna band kar sakte hain.

Kab pata chalega ki update chahiye:
  - Message to jaata hai lekin resume attach nahi hota (ya ulta)
  - Script "Timeout" ya "element not found" error deta hai
  - WhatsApp ka naya redesign aata hai (usually saal mein 2-4 baar)

Kaise fix karein (koi coding expert hone ki zaroorat nahi):
  1) Chrome mein web.whatsapp.com kholein, jis button mein dikkat aa rahi
     hai uspar right-click karke "Inspect" karein
  2) Uska naya attribute (data-icon, aria-label, title, ya class) note
     karein
  3) Neeche SELECTORS dict mein sirf wahi ek line update karni hai — baaki
     poori file waise hi rahegi

Sab selectors is ek hi jagah rakhe gaye hain (best practice), taaki future
mein sirf yahi dictionary dekhni/badalni pade.
"""

import os
import time
import urllib.parse
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Yahi folder Chrome ka "login memory" store karta hai. Isko delete karna
# = WhatsApp se logout karna (dobara QR scan karna padega).
CHROME_PROFILE_DIR = os.path.join(BASE_DIR, "Data", "whatsapp_chrome_profile")

# Jab bhi WhatsApp send/resume-attach fail ho, is folder mein ek
# screenshot + page HTML save ho jaata hai — taaki EXACT us waqt WhatsApp
# Web screen par kya tha, wo baad mein dekha ja sake (guess na karna pade).
DEBUG_LOG_DIR = os.path.join(BASE_DIR, "Logs", "whatsapp_debug")

# "Automation-ready" Chrome dhoondhne/khilaane ke liye fixed debug port.
# Open_Chrome_For_WhatsApp.bat bhi isi port ka use karta hai, dono match
# hone chahiye.
DEBUG_HOST = "127.0.0.1"
DEBUG_PORT = "9222"


def _save_debug_snapshot(driver, tag):
    """
    Failure hote hi EXACT us waqt ka screenshot + page ka HTML save
    karta hai, taaki baad mein dekha ja sake ki WhatsApp Web screen par
    us waqt actually kya ho raha tha (resume dialog khula tha ya nahi,
    text kahan gaya, koi popup toh nahi aaya, waghera) — bina isके
    aage ki debugging sirf anuman par hi rehti.

    Best-effort hai: agar screenshot lene mein hi koi dikkat aa jaaye,
    chup-chaap skip kar deta hai — is wajah se asli error chhupna nahi
    chahiye.

    Returns: saved screenshot ka path (ya None agar save nahi ho paaya)
    """
    try:
        os.makedirs(DEBUG_LOG_DIR, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        png_path = os.path.join(DEBUG_LOG_DIR, f"{stamp}_{tag}.png")
        html_path = os.path.join(DEBUG_LOG_DIR, f"{stamp}_{tag}.html")

        driver.save_screenshot(png_path)
        try:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
        except Exception:
            pass  # screenshot ho gaya toh itna kaafi hai, HTML optional hai

        return png_path
    except Exception:
        return None


def _log_send_result(phone, resume_path, ok, note, driver=None):
    """
    HAR send attempt (success ho ya fail, dono) ka ek permanent record
    rakhta hai — ek text log file mein (append mode) aur agar driver
    diya gaya ho toh ek screenshot bhi.

    ISLIYE ki: sirf failure par screenshot lena kaafi nahi hai — agar
    app "success" bhi bataye lekin asal mein WhatsApp par kuch na jaaye
    (false-positive), toh humein VO cheez bhi dikhni chahiye jo app ke
    hisaab se "sahi" thi. Ab har attempt (chahe result kuch bhi ho) ka
    proof save hota hai, taaki kabhi bhi kuch miss na ho aur baar-baar
    manually screenshot dhoondhna na pade.

    Log file: Logs/whatsapp_debug/send_log.txt (simple, human-readable,
    ek line per attempt — Notepad mein khol kar seedha copy-paste kiya
    ja sakta hai).
    """
    try:
        os.makedirs(DEBUG_LOG_DIR, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "SUCCESS" if ok else "FAILED"
        resume_info = os.path.basename(resume_path) if resume_path else "(no resume)"

        shot = None
        if driver is not None:
            tag = "success_snapshot" if ok else "failure_snapshot"
            shot = _save_debug_snapshot(driver, tag)

        shot_info = os.path.relpath(shot, BASE_DIR) if shot else "(screenshot nahi le paaye)"

        log_line = (
            f"[{stamp}] {status} | phone={phone} | resume={resume_info} | "
            f"screenshot={shot_info} | note={note}\n"
        )

        log_path = os.path.join(DEBUG_LOG_DIR, "send_log.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception:
        pass  # logging khud kabhi bhi asli feature ko todni nahi chahiye


def _try_attach_existing():
    """
    Pehle se khule "debuggable" Chrome se jud-ne (attach) ki koshish
    karta hai. Milta hai toh usi Chrome window ko return karta hai
    (koi naya window nahi khulta). Nahi milta toh chup-chaap None
    return karta hai — yeh normal hai, error nahi.

    IMPORTANT FIX: Sirf port 9222 par kisi ne jawab de diya, iska matlab
    yeh NAHI ki wahan ek zinda/dikhne-wala Chrome window hai. Agar
    pichli baar Chrome crash hua ya galat tarike se band hua (Task
    Manager se, ya app force-close se), toh kabhi-kabhi ek "zombie"
    chrome.exe process peeche reh jaata hai jo abhi bhi us port par
    debug-connection accept kar leta hai, lekin uski koi visible window
    screen par nahi hoti (ya woh already-dead session hai). Pehle yeh
    function aisi zombie/dead state ko bhi "successfully attached" maan
    leta tha — isi wajah se screen par kuch nahi dikhta tha lekin script
    aage badhta rehta tha aur end mein "bubble confirm nahi hui" jaisi
    confusing error deta tha.

    Ab hum attach karne ke baad ek chhota sa "sanity check" karte hain:
    kam se kam ek REAL window handle hona chahiye aur uska current_url
    padh paana chahiye. Agar yeh check fail ho, toh is Chrome ko
    "usable nahi" maan kar None return karte hain, taaki caller ek
    NAYA, guaranteed-visible Chrome window khole.
    """
    try:
        print("Chrome khul raha hai (ya pehle se khula hua use ho raha hai)...")
        print("  [0/4] Pehle se koi 'attach-able' Chrome khula hai kya, check kar rahe hain...")
        options = webdriver.ChromeOptions()
        options.debugger_address = f"{DEBUG_HOST}:{DEBUG_PORT}"
        driver = webdriver.Chrome(options=options)

        # Sanity check: window handles milne chahiye aur unse baat ho
        # paani chahiye, warna yeh ek zombie/dead session hai.
        handles = driver.window_handles
        if not handles:
            raise WebDriverException("Attached Chrome has no window handles (zombie session).")
        driver.switch_to.window(handles[-1])
        _ = driver.current_url  # isse exception aayegi agar session dead hai

        print("  [0/4] Mil gaya — pehle se khula usable Chrome use kar rahe hain.")
        return driver
    except Exception:
        print("  [0/4] Koi pehle se khula usable Chrome nahi mila — naya Chrome kholenge.")
        return None


def _kill_zombie_chrome_for_profile():
    """
    Windows par: agar pichli baar automation-wala Chrome crash ho gaya
    tha ya force-close hua tha (Task Manager / app force-quit se), toh
    kabhi-kabhi uski process (chrome.exe) background mein zinda reh
    jaati hai — screen par koi window nahi dikhti, lekin woh process
    abhi bhi humare CHROME_PROFILE_DIR ko "lock" kiye rehti hai.

    Iska real-world asar: jab hum isi profile folder ke saath ek NAYA
    Chrome launch karne ki koshish karte hain, Windows/Chrome do
    instances ko ek hi profile share nahi karne dete — naya window ya
    toh bilkul nahi khulta, ya us purani zombie process ko hi silently
    activate kar deta hai (jiski koi visible window nahi hoti). Yehi
    asli wajah hai "Chrome khulta hi nahi, dikhta bhi nahi" wale
    symptom ki.

    Yeh function sirf tabhi chalta hai jab humein pehle se koi
    attach-able (zinda, usable) Chrome NAHI mila — matlab jo bhi
    process is profile ko pakde baithi hai, woh ya toh dead/zombie hai
    ya kisi wajah se attach nahi ho paayi. Isliye use surakshit tarike
    se khatam karke fresh start dena sahi hai.

    Best-effort hai: kisi bhi wajah se fail ho (permission, koi process
    na mile, non-Windows OS), chup-chaap aage badh jaata hai — Chrome
    ko normal tareeke se launch hone dete hain.
    """
    import platform
    import subprocess

    if platform.system() != "Windows":
        return

    print("  [1/4] Purani atki hui Chrome process check kar rahe hain...")
    try:
        # PowerShell se un chrome.exe processes ko dhoondhte hain jinki
        # command-line mein humara profile-folder path mention hai —
        # sirf unhi ko target karte hain, kisi aur/normal Chrome window
        # ko haath nahi lagate.
        ps_cmd = (
            "Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" "
            "| Where-Object { $_.CommandLine -and $_.CommandLine -like "
            f"'*{CHROME_PROFILE_DIR}*' }} "
            "| ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True,
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        time.sleep(1)  # process ko poori tarah exit hone ka thoda time
        print("  [1/4] Done — koi atki hui process mili toh band kar di.")
    except Exception as e:
        print(f"  [1/4] Skip kiya (best-effort check fail hua: {e})")


def _clear_stale_profile_lock():
    """
    Agar pichli baar automation-wala Chrome cleanly band nahi hua tha
    (crash ho gaya, ya Task Manager / app force-close se khatam kiya
    gaya), toh Chrome profile folder ke andar ek "SingletonLock" (aur
    kabhi "SingletonCookie" / "SingletonSocket") file reh jaati hai.

    Agla launch jab isी profile folder ke saath hota hai, Chrome dekhta
    hai ki lock file maujood hai aur maan leta hai ki profile "already
    in use" hai — is wajah se woh saved login/session use nahi karta,
    balki ek naya khaali/aisa session bana deta hai jismein WhatsApp Web
    dobara QR maangta hai. Yeh ASLI wajah hai jiski wajah se occasionally
    "naya window + dobara login" wala issue hota hai.

    Yeh function sirf tabhi chalta hai jab humein pehle se koi
    attach-able (zinda) debug-mode Chrome NAHI mila (_try_attach_existing
    fail ho chuka ho) - iska matlab hai ki koi bhi lock file jo mil rahi
    hai woh ek purani/mari hui process ki hai, kisi zinda Chrome ki nahi.
    Isliye ise safely delete karna theek hai.
    """
    stale_names = ("SingletonLock", "SingletonCookie", "SingletonSocket")
    for name in stale_names:
        path = os.path.join(CHROME_PROFILE_DIR, name)
        try:
            if os.path.islink(path) or os.path.exists(path):
                os.remove(path)
        except Exception:
            # Best-effort cleanup - agar delete na ho paaye (permission
            # wagera), Chrome ko normal tareeke se launch hone dete hain,
            # woh apne aap handle karne ki koshish karega.
            pass


def _launch_new_debuggable_chrome():
    """
    Koi attach-able Chrome nahi mila, isliye naya Chrome khulta hai —
    isi baar debug port bhi ON karke, taaki AGLI baar isी window se
    seedha jud saken (naya window na khulna pade).
    """
    os.makedirs(CHROME_PROFILE_DIR, exist_ok=True)

    # Sabse pehle: agar koi zombie/dead chrome.exe process is profile
    # folder ko lock kiye baithi hai (pichli crash/force-close se), use
    # khatam karte hain — warna naya Chrome ya toh khulega hi nahi, ya
    # invisible zombie ko hi silently activate karega.
    _kill_zombie_chrome_for_profile()

    # Pichli baar ka koi stale lock hoga toh hata dete hain (upar wala
    # docstring dekhein) - taaki saved WhatsApp login/session istemal ho
    # sake, dobara QR na maangna pade.
    print("  [2/4] Stale lock files check kar rahe hain...")
    _clear_stale_profile_lock()
    print("  [2/4] Done.")

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
    options.add_argument("--profile-directory=Default")
    options.add_argument(f"--remote-debugging-port={DEBUG_PORT}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # WhatsApp Web ko QR scan ke liye asli (non-headless) browser dikhna
    # zaroori hai, isliye headless kabhi use nahi karte.
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Selenium 4.10+ khud sahi chromedriver dhoondh/download kar leta hai
    # (Selenium Manager) — isliye alag se chromedriver install karne ki
    # zaroorat nahi hai, bas Chrome browser install hona chahiye.
    # NOTE: pehli baar (ya naya Chrome version aane par) Selenium Manager
    # ko sahi chromedriver dhoondhne/download karne ke liye INTERNET
    # chahiye hota hai — agar yahan atak jaaye, wajah aksar firewall/
    # antivirus hoti hai jo isse internet access nahi karne deta.
    print("  [3/4] Chrome + chromedriver setup ho raha hai "
          "(pehli baar internet chahiye ho sakta hai, ~10-30 sec)...")
    driver = webdriver.Chrome(options=options)
    print("  [3/4] Chrome successfully launch ho gaya.")
    return driver


def _build_driver():
    """
    Returns (driver, attached_to_existing: bool).

    attached_to_existing=True  -> Chrome pehle se khula tha, usi mein
                                   jud gaye (koi naya window nahi khula)
    attached_to_existing=False -> naya Chrome khola gaya hai (aur ise
                                   hamesha khula chhoda jaayega, taaki
                                   agli baar attach ho sake)
    """
    driver = _try_attach_existing()
    if driver is not None:
        return driver, True

    driver = _launch_new_debuggable_chrome()
    return driver, False

# ==========================================
# SELECTORS — WhatsApp UI badlein toh SABSE PEHLE yahi update karein
# ==========================================
SELECTORS = {
    # Left sidebar (chat list) — iske load hone ka matlab hai login ho
    # chuka hai (QR scan poora ho gaya)
    "logged_in_marker": "//div[@id='pane-side']",

    # QR code canvas — sirf pehli baar (ya logout ke baad) dikhta hai
    "qr_code": "//canvas[contains(@aria-label, 'Scan')] | //div[@data-ref]",

    # Chat ka message-typing box (neeche wali text bar)
    "message_box": "//footer//div[@contenteditable='true'][@data-tab]",

    # Message bhejne wala green arrow button
    "send_button": "//footer//button[.//span[@data-icon='send' or @data-icon='wds-ic-send-filled']]",

    # Paperclip / Attach icon
    "attach_button": (
        "//button[@title='Attach' or @aria-label='Attach']"
        " | //span[@data-icon='plus-rounded' or @data-icon='attach-menu-plus' or @data-icon='clip']/ancestor::button"
        " | //div[@title='Attach']"
    ),

    # "Document" option jo Attach menu khulne par dikhta hai
    "document_menu_item": (
        "//li[.//span[@data-icon='document']]"
        " | //div[@role='button'][.//span[text()='Document']]"
        " | //span[text()='Document']"
    ),

    # Hidden <input type="file"> jo Document option se juda hota hai
    # (accept attribute mein image/video nahi, general files hote hain).
    #
    # IMPORTANT FIX: WhatsApp Web ke Attach menu mein KAM SE KAM do
    # hidden file-inputs hote hain — ek "Photos & Videos"
    # (accept="image/*,video/*") aur ek "Document" (accept="*" ya
    # similar). Purana selector sirf "accept mein * hai ya nahi" check
    # karta tha — lekin "image/*,video/*" mein bhi '*' hota hai! Isliye
    # kabhi-kabhi PDF galti se Photos & Videos wale input mein chala
    # jaata tha, jise WhatsApp reject kar deta ("file not supported" —
    # isi wajah se yeh exact error aa raha tha). Ab explicitly "image"
    # wale input ko EXCLUDE karte hain.
    "document_file_input": (
        "//input[@type='file'][contains(@accept, '*')]"
        "[not(contains(@accept, 'image'))]"
    ),

    # Fallback: koi bhi file input agar upar wala specific na mile —
    # lekin yahan bhi image/video-only input ko exclude karte hain,
    # taaki fallback bhi galti se galat input na uthaye.
    "any_file_input": (
        "//input[@type='file'][not(contains(@accept, 'image'))]"
    ),

    # Preview screen (file select hone ke baad) ka Send button.
    # IMPORTANT FIX: [not(ancestor::footer)] zaroori hai — normal chat ka
    # Send button bhi isi tarah ke attributes (aria-label='Send', ya
    # data-icon='send') use karta hai aur woh <footer> ke andar hota hai.
    # Iske bina, agar preview dialog thoda slow load ho (bade PDF files
    # ke saath aam baat hai), toh yeh selector galti se NORMAL chat ka
    # Send button match kar sakta tha — jisse sirf caption text ek plain
    # message ki tarah chala jaata, aur resume kabhi attach hi nahi hota.
    "attach_send_button": (
        "//div[@role='button'][@aria-label='Send'][not(ancestor::footer)]"
        " | //span[@data-icon='send' or @data-icon='wds-ic-send-filled']"
        "/ancestor::div[@role='button'][not(ancestor::footer)]"
    ),

    # "Phone number shared via url is invalid" wala popup
    "invalid_number_popup": "//*[contains(text(), 'invalid') and contains(text(), 'Phone')]",

    # Resume/document preview khulne ke baad wala "Add a caption" box —
    # isi mein message type karke resume + text ek saath, ek hi Send
    # click se bhej sakte hain (do alag actions ki zaroorat nahi).
    #
    # IMPORTANT FIX: purana fallback "//footer//div[@contenteditable='true']"
    # yahan se HATA diya gaya hai — woh structurally normal chat ke
    # "message_box" jaisa hi hai, isliye galti se wahi match ho jaata
    # tha jab preview dialog abhi poora load nahi hua hota tha. Ab sirf
    # un attributes ko target karte hain jo sach mein sirf caption box
    # par hi milte hain (WhatsApp Web ke asli current/historical
    # markers) — agar future mein WhatsApp UI badle aur yeh sab fail
    # ho jaayein, error message clearly bataega ki caption box nahi
    # mila (silently galat jagah type nahi karega).
    "caption_box": (
        "//div[@contenteditable='true'][@data-tab='10'][not(ancestor::footer)]"
        " | //div[@contenteditable='true'][@aria-label='Add a caption']"
        " | //div[@contenteditable='true'][@aria-placeholder='Add a caption']"
        " | //div[@contenteditable='true'][@data-testid='media-caption-input']"
    ),

    # Chat ke andar har message-row ka ek STABLE, unique identifier —
    # "conv-msg-<id>" (data-testid attribute). Isse hum REAL confirmation
    # lete hain ki Send click ka koi asar hua ya nahi.
    #
    # IMPORTANT FIX: purana selector class="message-out" dhoondhta tha —
    # yeh WhatsApp Web ke CURRENT UI mein bilkul exist hi nahi karta
    # (aaj kal WhatsApp obfuscated/auto-generated CSS class names use
    # karta hai jo baar-baar badalte rehte hain). Isi wajah se resume
    # ACTUALLY chala jaata tha (user ke real WhatsApp chat screenshots
    # se confirm hua), lekin humara code use galti se "fail" bata deta
    # tha — jiski wajah se user baar-baar retry karta aur wahi resume
    # kai baar chala jaata.
    #
    # Naya approach: Send click se PEHLE saare maujooda "conv-msg-*"
    # IDs record kar lete hain, aur uske baad wait karte hain jab tak
    # koi NAYA ID na dikhe. "conv-msg-" prefix WhatsApp Web ke current
    # HTML mein consistently maujood hai (verified from real chat
    # dumps) aur class-name churn se affected nahi hota.
    "conv_msg_row": "//div[starts-with(@data-testid, 'conv-msg-')]",
}


def _get_conv_msg_ids(driver):
    """
    Chat mein abhi jitne bhi message-rows dikh rahe hain, unke unique
    "conv-msg-<id>" identifiers ka set return karta hai. Isse pehle aur
    baad ka comparison karke pata chalta hai ki koi NAYA message aaya
    ya nahi — yeh WhatsApp Web ke class-name churn se safe hai.
    """
    try:
        elements = driver.find_elements(By.XPATH, SELECTORS["conv_msg_row"])
        ids = set()
        for el in elements:
            try:
                tid = el.get_attribute("data-testid")
                if tid:
                    ids.add(tid)
            except Exception:
                continue
        return ids
    except Exception:
        return set()


def _wait_for_login(driver, first_run_timeout=120):
    """
    Agar QR code dikh raha hai (naya profile / logged out), user ko scan
    karne ke liye wait karta hai. Already logged-in ho toh turant aage
    badh jaata hai.
    """
    qr_present = driver.find_elements(By.XPATH, SELECTORS["qr_code"])
    already_loaded = driver.find_elements(By.XPATH, SELECTORS["logged_in_marker"])

    if already_loaded and not qr_present:
        return True, ""

    try:
        WebDriverWait(driver, first_run_timeout).until(
            EC.presence_of_element_located((By.XPATH, SELECTORS["logged_in_marker"]))
        )
        return True, ""
    except TimeoutException:
        return False, (
            f"QR code {first_run_timeout} second ke andar scan nahi hua. "
            "WhatsApp app kholein -> Linked Devices -> Link a Device -> "
            "khule Chrome window ka QR scan karein, phir dobara try karein."
        )


def _attach_resume_and_send(driver, resume_path, message):
    """
    Resume + message ko EK hi atomic action mein bhejta hai:
    Paperclip -> Document -> file input mein resume path -> caption box
    mein message type -> ek hi Send click.

    Pehle yeh do ALAG steps the: (1) text message bhejo + Send click,
    (2) phir se paperclip khol ke resume attach karo + dusra Send click.
    Do alag Send actions ke beech WhatsApp Web ka DOM/network kabhi
    settle nahi ho paata tha, jiski wajah se:
      - resume wala doosra step kabhi silently skip/fail ho jaata
        (isliye "resume nahi gaya")
      - pehla message wait/race ki wajah se late jaata ya kabhi
        bhejna hi reh jaata (isliye user ko khud resend karna padta)

    Ab dono ek hi preview screen + ek hi Send click mein jaate hain,
    isliye race/partial-failure ka chance kaafi kam ho jaata hai.

    Returns (success, note_string)
    """
    try:
        attach_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, SELECTORS["attach_button"]))
        )
        attach_btn.click()
        time.sleep(0.8)
    except Exception as e:
        shot = _save_debug_snapshot(driver, "attach_button_fail")
        extra = f" Screenshot: {os.path.relpath(shot, BASE_DIR)}" if shot else ""
        return False, f"Attach (📎) button nahi mila — WhatsApp UI badal gaya hoga. ({e}){extra}"

    file_input = None

    # Kai baar Attach click karte hi hidden file input directly DOM mein
    # aa jaata hai (Document menu click kiye bina bhi). Pehle wahi try
    # karte hain — agar nahi mila, toh "Document" menu item click karte
    # hain.
    try:
        file_input = driver.find_element(By.XPATH, SELECTORS["document_file_input"])
    except NoSuchElementException:
        try:
            doc_item = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS["document_menu_item"]))
            )
            doc_item.click()
            time.sleep(0.6)
        except Exception:
            pass  # shayad already khula ho, aage try karte hain

        try:
            file_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, SELECTORS["any_file_input"]))
            )
        except TimeoutException:
            shot = _save_debug_snapshot(driver, "file_input_fail")
            extra = f" Screenshot: {os.path.relpath(shot, BASE_DIR)}" if shot else ""
            return False, f"Document option / file input nahi mila — SELECTORS update karne ki zaroorat ho sakti hai.{extra}"

    try:
        file_input.send_keys(os.path.abspath(resume_path))
    except Exception as e:
        return False, f"Resume path file input mein daalte waqt error: {e}"

    # File preview load hone ka thoda wait (file size ke hisaab se —
    # bade PDF resumes ke liye margin badhaya gaya hai)
    time.sleep(3.5)

    # Preview khulne ke baad, caption box mein hi poora message type
    # karte hain — taaki resume + text ek hi Send click se jaayein.
    caption_typed = False
    if message:
        try:
            caption_box = WebDriverWait(driver, 12).until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS["caption_box"]))
            )
            caption_box.click()
            # Multi-line message: har line ke beech Shift+Enter (naya
            # line), sirf normal Enter dabane se WhatsApp turant bhej
            # deta — isliye Enter ka istemal yahan nahi karte, Send
            # button hi click karenge.
            lines = message.split("\n")
            actions = ActionChains(driver)
            for i, line in enumerate(lines):
                if line:
                    caption_box.send_keys(line)
                if i != len(lines) - 1:
                    # Shift+Enter = naya line (normal Enter turant bhej
                    # deta), isliye Shift ko theek se "hold" karke Enter
                    # dabana zaroori hai — ActionChains isse reliably
                    # karta hai.
                    actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                    actions = ActionChains(driver)
            caption_typed = True
        except Exception:
            # Caption box na mile toh bhi resume to bhej dete hain —
            # message caller ke paas fallback ke roop mein reh jaata
            # hai (neeche return note mein bataya jaata hai).
            caption_typed = False

    # Yahan ek snapshot le lete hain — isse pata chal jaayega ki text
    # (agar type hua) kis box mein gaya, aur preview dialog kaisa dikh
    # raha tha Send click se theek pehle.
    _save_debug_snapshot(driver, "before_attach_send_click")

    # REAL confirmation shuru hone se pehle abhi tak chat mein jo bhi
    # message-IDs dikh rahe hain, unka set record kar lete hain - Send
    # click ke baad agar koi NAYA ID nahi aata, toh iska matlab hai
    # click ka koi asar nahi hua, chahe click khud exception ke bina ho
    # gaya ho.
    initial_ids = _get_conv_msg_ids(driver)

    try:
        send_doc_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, SELECTORS["attach_send_button"]))
        )
        send_doc_btn.click()
    except Exception as e:
        shot = _save_debug_snapshot(driver, "attach_send_btn_fail")
        extra = f" Screenshot: {os.path.relpath(shot, BASE_DIR)}" if shot else ""
        return False, f"Resume preview ka Send button nahi mila: {e}{extra}"

    try:
        WebDriverWait(driver, 20).until(
            lambda d: len(_get_conv_msg_ids(d) - initial_ids) > 0
        )
    except TimeoutException:
        shot = _save_debug_snapshot(driver, "bubble_not_confirmed")
        extra = f" Screenshot: {os.path.relpath(shot, BASE_DIR)}" if shot else ""
        return False, (
            "Send button click toh hua, lekin chat mein resume/message ki koi "
            "nayi bubble confirm nahi hui — matlab yeh ACTUALLY nahi gaya "
            "(sirf click hona kaafi nahi hai). WhatsApp Web khud kholkar check "
            f"karke dobara try karein.{extra}"
        )

    time.sleep(1)

    if caption_typed:
        return True, " Resume + message ek saath bhej diye (chat mein confirm ho gaya)."
    return True, " Resume bhej diya, confirm ho gaya (caption box nahi mila, message alag se bhejna pad sakta hai)."


def send_whatsapp_message(phone, message, resume_path=None, wait_time=25,
                           first_run_timeout=120, keep_open=True):
    """
    Main entry point. Ek WhatsApp number par message bhejta hai, aur agar
    resume_path diya gaya ho (aur file exist karti ho) toh usse bhi
    attach karke bhejta hai.

    phone         : "+91XXXXXXXXXX" format mein
    message       : bhejne wala text
    resume_path   : resume file ka poora path (ya None)
    wait_time     : chat/message-box load hone ke liye max wait (seconds)
    first_run_timeout : pehli baar QR scan ke liye max wait (seconds)
    keep_open     : True (default) -> Chrome window band nahi hota, taaki
                    agli baar dobara khulne ki zaroorat na pade aur
                    WhatsApp Web session/tab reuse ho sake

    Returns (success: bool, message: str)
    """

    if not phone:
        return False, "Phone number khaali hai, WhatsApp skip kiya."

    driver = None

    def finish(ok, note):
        """
        Har return point isi se hoke guzarta hai - taaki result kuch bhi
        ho (success ya failure), woh hamesha permanently log ho jaaye
        (text log + screenshot), bina kisi extra manual step ke. Isse
        false-positive bhi pakde ja sakte hain - agar app "success"
        bole lekin screenshot mein resume/message dikh hi na raha ho.
        """
        _log_send_result(phone, resume_path, ok, note, driver=driver)
        return ok, note

    try:
        driver, attached = _build_driver()
    except WebDriverException as e:
        return finish(False, (
            "Chrome browser start nahi ho paaya. Chrome install hai ya "
            f"nahi check karein. ({e})"
        ))

    opened_new_tab = False

    try:
        if attached:
            # Chrome pehle se khula tha (Open_Chrome_For_WhatsApp.bat se,
            # ya pichle run se) - usmein jo bhi tabs khule hain (jaise
            # WhatsApp Web already logged in), unhe chhedte nahi. Bas ek
            # nayi tab kholte hain isi window mein.
            #
            # IMPORTANT FIX: pehle "window.open()" (JavaScript ke through)
            # use karke tab khola jaata tha, phir turant switch kiya
            # jaata tha - is beech ek race condition thi: kabhi-kabhi
            # naya tab poori tarah register hone se pehle hi switch/use
            # ho jaata, ya popup-blocker jaisi kisi wajah se khulta hi
            # nahi tha - jisse "target window already closed" jaisi
            # error aati thi. Ab Selenium ka apna official, reliable
            # switch_to.new_window() method use karte hain, jo
            # guarantee deta hai ki tab poori tarah ban kar register ho
            # chuka hai tab hi hum aage badhte hain. Agar phir bhi fail
            # ho (rare), ek retry karte hain.
            new_tab_ok = False
            for attempt in range(2):
                try:
                    driver.switch_to.new_window("tab")
                    _ = driver.current_url  # sanity check - window sach mein usable hai
                    new_tab_ok = True
                    break
                except Exception:
                    time.sleep(1)
            if not new_tab_ok:
                return finish(False, (
                    "Naya browser tab nahi khul paya (Chrome window "
                    "beech mein band ho gayi hogi). Chrome window ko "
                    "band mat karein jab tak app process kar rahi ho, "
                    "phir dobara try karein."
                ))
            opened_new_tab = True

        phone_for_url = phone.lstrip("+")
        url = (
            "https://web.whatsapp.com/send?phone="
            + phone_for_url
            + "&text="
            + urllib.parse.quote(message)
        )
        driver.get(url)

        logged_in, login_err = _wait_for_login(driver, first_run_timeout=first_run_timeout)
        if not logged_in:
            return finish(False, login_err)

        # Invalid number check
        if driver.find_elements(By.XPATH, SELECTORS["invalid_number_popup"]):
            return finish(False, f"WhatsApp ke mutabik yeh number invalid hai: {phone}")

        try:
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, SELECTORS["message_box"]))
            )
        except TimeoutException:
            return finish(False, (
                "Chat load nahi hua tay time mein — internet check karein "
                "ya Settings mein 'WhatsApp Wait Time' badhayein."
            ))

        time.sleep(1.5)  # text pre-fill fully settle hone dein

        resume_available = bool(resume_path and os.path.exists(resume_path))

        if resume_available:
            # Resume hai: text message aur resume ko EK hi atomic action
            # mein bhejte hain (attach -> caption box mein message ->
            # ek hi Send). Pehle jo text pre-fill URL se message box
            # mein aaya tha, use clear kar dete hain taaki woh khaali
            # duplicate message ban ke na reh jaaye.
            try:
                msg_box = driver.find_element(By.XPATH, SELECTORS["message_box"])
                msg_box.send_keys(Keys.CONTROL, "a")
                msg_box.send_keys(Keys.BACKSPACE)
            except Exception:
                pass  # koi baat nahi, pre-filled text harmless hai

            ok, note = _attach_resume_and_send(driver, resume_path, message)
            if not ok:
                return finish(False, f"Resume + message bhejne mein dikkat: {note}")
            return finish(True, f"{phone} ko bhej diya.{note}")

        # Resume nahi hai (ya file disk par nahi mili) -> sirf text
        # message bhejte hain, purane single-step tareeke se.
        initial_ids = _get_conv_msg_ids(driver)

        try:
            send_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, SELECTORS["send_button"]))
            )
            send_btn.click()
        except Exception as e:
            return finish(False, f"Send button nahi mila — WhatsApp UI badal gaya hoga. ({e})")

        # REAL confirmation: sirf click hona kaafi nahi - jab tak chat
        # mein ek NAYA message-ID na dikhe, tab tak "sent" nahi maanenge.
        try:
            WebDriverWait(driver, 15).until(
                lambda d: len(_get_conv_msg_ids(d) - initial_ids) > 0
            )
        except TimeoutException:
            return finish(False, (
                "Send button click toh hua, lekin chat mein message ki koi nayi "
                "bubble confirm nahi hui — matlab yeh ACTUALLY nahi gaya. "
                "WhatsApp Web khud kholkar check karke dobara try karein."
            ))

        resume_note = " (Resume file disk par nahi mili.)" if resume_path else ""
        return finish(True, f"Message {phone} ko bhej diya (chat mein confirm ho gaya).{resume_note}")

    except Exception as e:
        return finish(False, f"WhatsApp Selenium error: {e}")

    finally:
        try:
            if opened_new_tab:
                # Sirf woh tab band karte hain jo humne khud khola tha —
                # baaki saari tabs (jaise pehle se khula WhatsApp Web)
                # bilkul waise hi rehti hain, chhedi nahi jaati.
                driver.close()
                if driver.window_handles:
                    driver.switch_to.window(driver.window_handles[0])
            elif not keep_open:
                # Sirf tab tab quit() karte hain jab humne khud yeh
                # Chrome launch kiya tha AUR caller ne explicitly
                # keep_open=False bola ho. Default mein hum ise khula hi
                # chhodte hain taaki agli baar dobara login/QR na karna
                # pade.
                time.sleep(1.5)
                driver.quit()
        except Exception:
            pass


def one_time_login():
    """
    Sirf pehli baar chalane ke liye (ya jab kabhi logout ho jaaye).
    Chrome kholta hai (ya pehle se khula hua reuse karta hai), QR scan
    hone ka wait karta hai — koi message nahi bhejta. Iske baad Chrome
    khula hi rehta hai (band nahi hota), taaki saare aage ke sends isi
    window mein/isi se attach ho ke chalein.

    Terminal mein chalayein:  python whatsapp_selenium.py
    """
    driver, attached = _build_driver()

    if attached:
        print("Pehle se khula automation-ready Chrome mil gaya, isi mein "
              "nayi tab khol rahe hain.")
        driver.switch_to.new_window("tab")
        driver.get("https://web.whatsapp.com")
    else:
        driver.get("https://web.whatsapp.com")

    print("Agar QR code dikhe toh: WhatsApp app > Linked Devices > "
          "Link a Device se scan karein.")

    ok, err = _wait_for_login(driver, first_run_timeout=180)
    if ok:
        print("✅ Login safal! Yeh Chrome window ab khuli hi rahegi (isse "
              "band mat karein) — aage se saare sends isi mein/isi se "
              "attach ho ke jaayenge, dobara QR nahi maangega.")
    else:
        print("❌", err)


if __name__ == "__main__":
    one_time_login()
