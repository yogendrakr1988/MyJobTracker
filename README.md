# 📋 Job Tracker Pro

Ek desktop application jo job applications track karta hai, aur naya job save hote hi
automatically **HR ko Email + WhatsApp message** bhej deta hai — resume attach karke.

**Developer:** Yogendra Kumar
**Version:** 1.0

---

## ✨ Features

- Dashboard — total applications, status-wise count, aaj ke follow-ups
- Add Job — naya application add karo, resume attach karo
- Naya job save hote hi **Email (Gmail)** aur **WhatsApp** dono par automatically
  first message chala jaata hai (agar Settings me ON kiya ho)
- View Jobs — sab applications dekho, edit karo, delete karo, resume kholo
- Search Jobs — company / role / status se search
- Reports — Excel report export
- Settings — Gmail App Password, WhatsApp on/off, message templates

---

## 📁 Folder Structure

```
MyJobTracker/
├── main.py                  # App yahin se start hota hai
├── gui.py                   # Sidebar + screen switching
├── config.py                 # Folder paths, app name/version
├── notifier.py               # Email + WhatsApp bhejne wala code
├── settings_manager.py       # settings.json read/write
├── settings.json              # Aapke Gmail/WhatsApp settings (PRIVATE)
├── jobs.xlsx                  # Saari job applications yahin save hoti hain
├── requirements.txt
├── screens/
│   ├── dashboard.py
│   ├── add_job.py             # Add Job form + processing window (is release me update hua)
│   ├── view_jobs.py
│   ├── search_jobs.py
│   ├── reports.py
│   ├── resume.py
│   └── settings.py
├── Resume/                    # Apna resume yahan rakh sakte ho
├── Reports/                   # Exported reports yahan save hote hain
├── Data/, Logs/, Images/, Assets/   # Future use ke liye reserved folders
```

---

## ⚙️ Installation (Windows / Mac / Linux)

1. Python 3.10+ install hona chahiye.
2. Project folder me terminal khol kar:

   ```
   pip install -r requirements.txt
   ```

3. App run karo:

   ```
   python main.py
   ```

`requirements.txt` me ye libraries hain:

- `customtkinter` — GUI
- `openpyxl` — Excel read/write
- `selenium` — WhatsApp Web automation (browser control ke through)
- `keyring` — Gmail app password ko securely OS keychain me store karna

---

## 📧 Gmail Email Setup (App Password)

Gmail apna **normal password nahi**, ek **App Password** maangta hai:

1. Google Account → **Security**
2. **2-Step Verification** ON karo (agar pehle se ON nahi hai)
3. **App Passwords** section me jao → naya app password banao (type: "Mail")
4. Jo 16-letter code milega, usko App ke **Settings → Gmail App Password** field me paste karo
5. **Settings** screen me "Auto-send Email whenever a new job application is saved" ko ✅ karo
6. **Save Settings** dabao

---

## 💬 WhatsApp Setup

- Yeh feature **WhatsApp Web** use karta hai, ek dedicated Selenium-controlled Chrome
  profile (`Data/whatsapp_chrome_profile`) ke through — koi screen-click/keypress
  simulation (pyautogui) nahi hota, isliye zyada reliable hai
- Pehli baar `Open_Chrome_For_WhatsApp.bat` chala kar **web.whatsapp.com** khol kar
  QR code scan kar lo, taaki us profile me login-saved rahe
- Settings me "Auto-send WhatsApp message whenever a new job application is saved" ✅ karo
- Jab bhi naya job save hoga, Selenium khud us Chrome profile ko background me
  chalayega, message bhej kar band ho jayega (~15-20 second lagte hain)

> ⚠️ Automation ke dauraan apna normal Chrome window na chhedo agar wahi profile
> use ho raha ho — dedicated automation profile alag hai, isliye zyada tarah se
> aapke normal browsing me interfere nahi karega, lekin fir bhi is process ke
> dauraan system ko busy na rakhein.

---

## ➕ Add Job — Save + Notification Flow (Updated)

Pehle processing background me chhupi hui chalti thi. **Ab pura process screen par
dikhta hai — kuch bhi hidden nahi chalta:**

1. **Save** button dabao (Company aur Role dena zaroori hai)
2. Data **Excel me ek hi baar** save hota hai — Save button turant disable ho jaata hai
   taaki double-click se ek hi application do baar save na ho jaaye
3. Turant ek **"Application Progress"** window khulti hai jisme dikhta hai:
   - ✅ Data saved to jobs.xlsx
   - 📧 Email: ⏳ Sending... → phir ✅ ya ⚠️ ke saath poora result
   - 💬 WhatsApp: ⏳ Sending... → phir ✅ ya ⚠️ ke saath poora result
4. Email aur WhatsApp **do alag independent popups** dikhate hain — jaise hi Email
   ka result aata hai uska popup turant aa jaata hai, WhatsApp ka result thodi der baad
   (~20 sec) aata hai to uska popup alag se aata hai. Dono kabhi ek saath merge nahi hote.
5. Jab dono complete ho jaate hain, form apne aap clear ho jaata hai aur **Close** button
   enable ho jaata hai.
6. Agar Email ya WhatsApp OFF hai (Settings me), ya HR Email/Mobile khaali hai, to us
   channel ka status turant **⚠️** ke saath reason dikhayega (e.g. "Email auto-send is OFF").

---

## 📱 Kya main isse Phone (Android / iPhone) par use kar sakta hoon?

**Seedha jawab: Nahi, is form me nahi.**

Yeh app **desktop GUI (customtkinter/Tkinter)** se bana hai, jo sirf **Windows, Mac, aur
Linux** par chalta hai. Yeh Android/iPhone ke liye install-able (.apk / App Store) app
nahi hai, aur phone par seedha run nahi hoga.

Kya options hain:

| Option | Kaam karega? | Kyun |
|---|---|---|
| Phone par `.exe`/`.py` chalana | ❌ Nahi | Android/iOS Tkinter support nahi karte |
| Termux + VNC (Android hack) | ⚠️ Bahut unreliable | Slow, WhatsApp/Gmail automation break ho sakta hai |
| **jobs.xlsx ko Google Drive/OneDrive me sync karna** | ✅ Sirf **dekhne** ke liye | Phone se Excel/Sheets app me apni applications list dekh sakte ho, lekin naya job add ya notification phone se nahi bhej sakte |
| **App ko Web version me convert karna** | ✅ Sabse best solution | Flask/FastAPI backend bana kar isi jobs.xlsx/logic ko web app bana diya jaaye, jise phone ke browser se bhi khola ja sake (same WiFi par ya online deploy karke) |

**Recommendation:** Abhi ke liye laptop/PC par hi use karo (kyunki Gmail SMTP aur WhatsApp
Web automation dono ko ek real browser aur desktop chahiye). Agar aapko sach me phone se
bhi naya job add karna hai, to iska ek **separate Web version** banwana sabse sahi rasta
hoga — chaho to woh alag se bana sakte hain.

---

## 🧑‍💻 Developer Copy (naya, transparent, opt-in feature)

Agar aap yeh code kisi aur ko de rahe ho aur unke saved application ka **ek copy aapke
(developer ke) email par bhi aaye**, iske liye ek naya feature add kiya gaya hai —
lekin yeh **poori tarah transparent aur opt-in** hai, chupke se kabhi kuch nahi jaata:

- Jab bhi koi user app **pehli baar** kholega, ek popup aayega jisme saaf-saaf poocha
  jaayega: *"Kya aap har saved application ka copy developer ko bhejna chahte ho?"*
- User **Yes** ya **No** chun sakta hai. Agar No chuna, to future me kabhi bhi kuch extra
  nahi bhejega.
- Yeh setting **Settings screen** me bhi dikhti hai ("🧑‍💻 Developer Copy" section) — user
  chaahe jab isse ON/OFF kar sakta hai.
- Jab ON ho, to "Application Progress" window me ek teesri line dikhti hai —
  **📨 Developer Copy: ⏳ Sending... → ✅/⚠️** — bilkul Email/WhatsApp ki tarah, apna alag
  popup ke saath. Jab OFF ho, wahi line seedha bata degi **"⏸ Off"**.
- Sirf ek **text summary** (Company, Role, HR details, Status, Notes) jaata hai —
  **resume file attach nahi hoti**, taaki jitna zaroori ho utna hi data share ho.
- Developer ka fixed email (`config.py` → `DEVELOPER_EMAIL`) source code me khule taur par
  likha hai, taaki koi bhi is code ko padh kar exactly dekh sake ki data kahan jaata hai.

**Important:** Yeh feature user ke apne configured Gmail SMTP (Settings me diya gaya Gmail
address + App Password) se hi email bhejta hai — koi alag/hidden mechanism nahi hai.

---

## 🔐 Security Note — Zaroor Padho

`settings.json` file me aapka **Gmail App Password plain text me** save hota hai. Yeh file
kabhi:

- GitHub/GitLab par public repo me push mat karo
- kisi ke saath share mat karo
- agar galti se kahin share ho gaya ho (jaise ismein pehle se ek real password saved tha),
  to turant Google Account → Security → App Passwords me jaakar **us App Password ko
  revoke/delete** kar do aur naya bana lo.

Agar aap is project ko Git me daalna chahte ho, to `.gitignore` me `settings.json` aur
`jobs.xlsx` ko add kar dena (dono me personal data hota hai).

---

## 🛠️ Is Update Me Kya Fix Hua

1. **Processing ab hidden nahi chalti** — "Application Progress" window me Save, Email,
   aur WhatsApp teeno steps live dikhte hain.
2. **Email aur WhatsApp ke success/warning messages ab alag-alag** popup me aate hain
   (pehle dono ek hi combined popup me aate the).
3. **Ek application sirf ek hi baar Excel me save hoti hai** — Save button double-click
   guard ke saath disable ho jaata hai jab tak process poora na ho.
4. README.md poora likha gaya (pehle khaali tha).
5. Phone/mobile use ke baare me upar clear jawab diya gaya hai.
6. **Developer Copy** — naya, transparent aur opt-in feature: agar user agree kare, to har
   saved application ka ek text-summary copy developer ko bhi jaata hai (upar section dekho).
7. `USER_GUIDE.md` add ki gayi — app use karne ka poora step-by-step guide + video-recording
   script, taaki app ka demo video khud bana sako.

---

## 🚀 WhatsApp Chrome ko PC start hote hi khud khulwana (AutoStart)

Baar-baar `Open_Chrome_For_WhatsApp.bat` manually chalane/QR scan karne se
bachne ke liye, ab ek permanent setup available hai:

1. **`Install_AutoStart.bat`** ko ek baar double-click karo
2. Yeh Windows ke Startup folder mein ek shortcut daal deta hai
3. Ab jab bhi PC start/restart/login hoga, WhatsApp-ready Chrome
   **apne aap (minimized)** khul jaayega — manually .bat chalane ki
   zaroorat khatam
4. Pehli baar us Chrome window mein WhatsApp Web login karna hai (ek
   baar QR scan) — uske baad session save rehta hai, dobara QR nahi
   maangega

Hatana ho (autostart band karna ho) toh **`Uninstall_AutoStart.bat`**
chalao — bas.

**Note:** Yeh window ko PC restart hone tak khula/minimized hi chhodna
hai (band mat karna) — tabhi Job Tracker Pro isी mein tab khol kar
message/resume bhej payega, koi naya window ya dobara login nahi hoga.

---

## ❓ Troubleshooting

- **"Email failed: Gmail login rejected"** → App Password galat hai, dobara generate karo.
- **WhatsApp tab khulta hai par message nahi jaata** → Internet slow ho sakta hai;
  `notifier.py` me `wait_time=20` badha sakte ho.
- **Excel file "permission denied" error** → `jobs.xlsx` file Excel me khuli hui hogi,
  pehle usko band karo phir Save karo.
