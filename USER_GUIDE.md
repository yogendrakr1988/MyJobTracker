# 🎬 Job Tracker Pro — User Guide (aur khud video banane ki script)

Main directly video file nahi bana sakta, lekin yeh guide follow karke aap khud **5-6
minute ka demo video** bana sakte ho — free screen recorder se (Windows: **Xbox Game Bar**
`Win + G`, Mac: **QuickTime Player → New Screen Recording**, ya free tool **OBS Studio**).

Neeche har step ke saath ek "🎙️ Bolne ke liye" line di gayi hai — usko bolte hue record
karo, video khud-ba-khud ek acchi tutorial ban jayegi.

---

## Part 1 — Setup (ek baar karna hai)

### Step 1: App install & run

```
pip install -r requirements.txt
python main.py
```

🎙️ **Bolne ke liye:** "Sabse pehle terminal khol kar requirements install karo, phir
`python main.py` se app open karo."

### Step 2: First-launch popup

App khulte hi ek popup aayega — **"Send a Copy to the Developer?"**

- Agar aap chahte ho ki har saved application ka copy developer ko bhi jaaye → **Yes**
- Nahi chahiye → **No**
- Yeh baad me bhi Settings se change ho sakta hai

🎙️ **Bolne ke liye:** "Jaise hi app khulta hai, yeh popup poochta hai ki kya aap apna
data developer ke saath bhi share karna chahte ho — poori tarah optional hai, main abhi
'No/Yes' choose kar raha hoon."

### Step 3: Settings bharo

Sidebar se **Settings** par click karo:

1. **Gmail Address** — apna Gmail ID
2. **Gmail App Password** — normal password nahi, App Password (README me steps hain)
3. "Auto-send Email..." checkbox ✅ karo (agar email bhejna hai)
4. "Auto-send WhatsApp..." checkbox ✅ karo (agar WhatsApp bhejna hai)
5. Templates check kar lo (Subject/Body/WhatsApp message)
6. **💾 Save Settings** dabao

🎙️ **Bolne ke liye:** "Settings me apna Gmail address aur App Password daalo, Email aur
WhatsApp auto-send ON karo, aur Save Settings dabao."

---

## Part 2 — Naya Job Application Add karna (main demo)

### Step 4: Add Job

Sidebar se **Add Job** click karo. Form bharo:

- Company, Role (yeh dono zaroori hain)
- HR Name, HR Email, HR Mobile
- Applied Date, Follow-up Date, Job Portal, Job Link
- Resume attach karo (Attach button)
- Status select karo (Applied / Interview / Selected / Rejected)

🎙️ **Bolne ke liye:** "Ab main ek naya job application add kar raha hoon — Company aur
Role dena zaroori hai, baaki fields optional hain, resume bhi attach kar sakte ho."

### Step 5: Save dabao aur Processing dekho

**💾 Save** button dabate hi:

1. Data turant Excel me save ho jaata hai
2. Ek **"Application Progress"** window khulti hai jisme live dikhta hai:
   - ✅ Data saved
   - 📧 Email: Sending → ✅/⚠️ result apne popup ke saath
   - 💬 WhatsApp: Sending → ✅/⚠️ result apne popup ke saath (isme ~20 sec lag sakte hain)
   - 📨 Developer Copy: (agar ON hai to yeh bhi)

🎙️ **Bolne ke liye:** "Save dabate hi dekho — pura processing screen par live dikh raha
hai, chhupa hua kuch nahi hai. Email ka result pehle aata hai, WhatsApp ka thodi der baad,
dono ka alag popup aata hai."

> ⚠️ WhatsApp bhejte waqt browser khud khulega — is dauran keyboard/mouse mat chhedo.

---

## Part 3 — Baaki Screens

### Step 6: Dashboard
Sidebar → **Dashboard**: total applications, status-wise count, aaj ke follow-ups dikhte hain.

🎙️ "Dashboard par apna overall progress dikh jaata hai."

### Step 7: View Jobs
Sidebar → **View Jobs**: saari applications table me, **Edit / Delete / Open Resume /
Load in Add Job** buttons ke saath.

🎙️ "Yahan saari applications list me hain, edit ya delete bhi kar sakte ho."

### Step 8: Search Jobs
Sidebar → **Search Jobs**: company/role/status se filter karo.

🎙️ "Kisi bhi company ya status se search kar sakte ho."

### Step 9: Reports
Sidebar → **Reports**: summary + **Export Report (Excel)** button se ek fresh Excel
report `Reports/` folder me ban jaata hai.

🎙️ "Yahan se ek summary report Excel me export kar sakte ho."

---

## Recording Tips

- Screen recorder start karne se pehle app already band kar do, taaki "app open hona"
  bhi record ho jaaye.
- Har step ke beech 2-3 second ruko taaki editing me kaatna aasan ho.
- Sensitive info (Gmail App Password, real phone numbers) recording se pehle test/dummy
  data se replace kar lo.
- End me bata do: *"Poora code aur README GitHub/ZIP me available hai."*

Bas — isi order me record karke aap 5-6 minute ka clean tutorial bana sakte ho.
