# screens/bulk_send.py
"""
==========================================
Job Tracker Pro
Bulk Send — Email / WhatsApp
==========================================

View Jobs screen mein jitni applications tick(✓) ki gayi hain, unko
EK KE BAAD EK Email ya WhatsApp bhejta hai — ek live-progress window
ke saath, taaki HR ko manually ek-ek karke message na bhejna pade.

IMPORTANT — WhatsApp bulk sending ka RISK:
WhatsApp Web par bahut jaldi-jaldi bahut saare messages bhejna
WhatsApp ki apni spam-detection ko trigger kar sakta hai aur number
ko temporarily/permanently restrict/block kar sakta hai. Isse poori
tarah bachne ka koi 100% guaranteed tareeka nahi hai. Isliye:

  - Har WhatsApp send ke beech ek jaan-bujh kar diya gaya delay hai
    (WHATSAPP_DELAY_RANGE seconds, random) — taaki yeh "normal
    insaan jaisi" activity ke zyada kareeb rahe, ek machine-gun jaisi
    burst na ho
  - Bulk WhatsApp send shuru karne se pehle UI mein ek clear warning
    dikhayi jaati hai, final decision user ka hi hota hai
  - Email ke liye yeh risk practically nahi hota (Gmail SMTP ek
    normal "send mail" hai), isliye email ka delay bahut chhota hai
"""

import time
import random
import threading

import customtkinter as ctk

import notifier

EMAIL_DELAY_SECONDS = 2            # Gmail sends ke beech chhota gap
WHATSAPP_DELAY_RANGE = (10, 18)    # WhatsApp sends ke beech jaan-bujh kar bada gap


def run_bulk_send(parent, rows, mode):
    """
    rows : list of job_data dicts (ViewJobsScreen.FIELDS ki keys ke
           saath) — sirf woh applications jo user ne tick ki hain
    mode : "email" ya "whatsapp"

    Ek naya window kholta hai jisme live progress dikhta hai — kaunsi
    company/HR ko bheja jaa raha hai, result kya aaya (✅/⚠️), aur end
    mein total summary.
    """

    is_email = (mode == "email")

    win = ctk.CTkToplevel(parent)
    win.title("Bulk Email Send" if is_email else "Bulk WhatsApp Send")
    win.geometry("580x500")
    win.grab_set()
    win.resizable(False, False)

    ctk.CTkLabel(
        win,
        text=("📧 Sending Emails to Selected HRs..." if is_email
              else "💬 Sending WhatsApp Messages to Selected HRs..."),
        font=("Segoe UI", 17, "bold"),
        wraplength=520,
    ).pack(pady=(15, 5))

    progress_label = ctk.CTkLabel(win, text=f"0 / {len(rows)} done", font=("Segoe UI", 13))
    progress_label.pack(pady=(0, 10))

    log_box = ctk.CTkTextbox(win, width=540, height=340, font=("Consolas", 11))
    log_box.pack(padx=15, pady=5, fill="both", expand=True)
    log_box.configure(state="disabled")

    close_btn = ctk.CTkButton(win, text="Close", width=140, state="disabled", command=win.destroy)
    close_btn.pack(pady=12)

    def log(line):
        log_box.configure(state="normal")
        log_box.insert("end", line + "\n")
        log_box.see("end")
        log_box.configure(state="disabled")

    def set_progress(text):
        progress_label.configure(text=text)

    def worker():
        ok_count = 0
        fail_count = 0
        total = len(rows)

        for i, job_data in enumerate(rows, start=1):
            company = job_data.get("Company", "") or "(no company)"
            hr_name = job_data.get("HR Name", "") or "HR"

            if is_email:
                target = job_data.get("HR Email", "") or "(no email)"
            else:
                target = job_data.get("HR Mobile", "") or "(no mobile)"

            win.after(0, log, f"[{i}/{total}] {company} — {hr_name} -> {target} ... sending")

            try:
                if is_email:
                    success, message = notifier.send_email(job_data)
                else:
                    success, message = notifier.send_whatsapp(job_data)
            except Exception as e:
                success, message = False, f"Unexpected error: {e}"

            if success:
                ok_count += 1
                win.after(0, log, f"    ✅ {message}")
            else:
                fail_count += 1
                win.after(0, log, f"    ⚠️ {message}")

            win.after(0, set_progress, f"{i} / {total} done  (✅ {ok_count}  ⚠️ {fail_count})")

            if i < total:
                delay = EMAIL_DELAY_SECONDS if is_email else random.uniform(*WHATSAPP_DELAY_RANGE)
                time.sleep(delay)

        win.after(0, log, "")
        win.after(0, log, f"Done — ✅ {ok_count} sent, ⚠️ {fail_count} failed/skipped.")
        win.after(0, set_progress, f"Finished: {ok_count} sent, {fail_count} failed/skipped")
        win.after(0, lambda: close_btn.configure(state="normal"))

    threading.Thread(target=worker, daemon=True).start()
