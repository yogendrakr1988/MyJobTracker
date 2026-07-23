import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from settings_manager import load_settings, save_settings
from config import DEVELOPER, DEVELOPER_EMAIL


class SettingsScreen:

    def __init__(self, parent):
        self.parent = parent
        self.settings = load_settings()

    def show(self):

        frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="⚙️  Settings",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=(0, 15), anchor="w")

        scroll = ctk.CTkScrollableFrame(frame, fg_color="white", corner_radius=15)
        scroll.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(scroll, fg_color="white")
        inner.pack(fill="both", expand=True, padx=30, pady=25)

        label_font = ("Segoe UI", 14, "bold")
        entry_font = ("Segoe UI", 13)

        # ---------------- Email Section ----------------

        ctk.CTkLabel(
            inner,
            text="📧 Email Settings (Gmail)",
            font=("Segoe UI", 17, "bold"),
            text_color="#1a1a1a"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        ctk.CTkLabel(inner, text="Gmail Address", font=label_font, text_color="#1a1a1a").grid(
            row=1, column=0, sticky="w", pady=8
        )
        self.email_var = tk.StringVar(value=self.settings.get("gmail_address", ""))
        ctk.CTkEntry(inner, textvariable=self.email_var, width=340, font=entry_font).grid(
            row=1, column=1, pady=8, padx=10
        )

        ctk.CTkLabel(inner, text="Gmail App Password", font=label_font, text_color="#1a1a1a").grid(
            row=2, column=0, sticky="w", pady=8
        )
        self.password_var = tk.StringVar(value=self.settings.get("gmail_app_password", ""))
        ctk.CTkEntry(inner, textvariable=self.password_var, width=340, font=entry_font, show="*").grid(
            row=2, column=1, pady=8, padx=10
        )

        howto = ctk.CTkLabel(
            inner,
            text=(
                "How to get an App Password: Google Account → Security → 2-Step Verification\n"
                "(turn ON) → App Passwords → create one for 'Mail' → paste the 16-letter code above.\n"
                "(This is NOT your normal Gmail password.)"
            ),
            font=("Segoe UI", 11),
            text_color="#666666",
            justify="left"
        )
        howto.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.email_enabled_var = tk.BooleanVar(value=self.settings.get("email_enabled", False))
        ctk.CTkCheckBox(
            inner,
            text="Auto-send Email whenever a new job application is saved",
            variable=self.email_enabled_var,
            font=entry_font,
            text_color="#1a1a1a"
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 25))

        # ---------------- WhatsApp Section ----------------

        ctk.CTkLabel(
            inner,
            text="💬 WhatsApp Settings",
            font=("Segoe UI", 17, "bold"),
            text_color="#1a1a1a"
        ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(0, 12))

        wa_note = ctk.CTkLabel(
            inner,
            text=(
                "Uses WhatsApp Web — your browser must already be logged in to WhatsApp\n"
                "(scan the QR code once at web.whatsapp.com). When a job is saved, a browser\n"
                "tab will open and send the message automatically.\n\n"
                "IMPORTANT: the message is sent FROM whichever WhatsApp account is logged\n"
                "in inside that browser — the app cannot choose the number for you. If it\n"
                "keeps sending from the wrong number, open the browser below, go to\n"
                "web.whatsapp.com, log out, and scan the QR code again using 8077693361.\n\n"
                "The resume CANNOT be attached automatically (WhatsApp Web has no way to\n"
                "receive a file link) — its file path is copied to your clipboard instead,\n"
                "so attaching it is just: click 📎 → Document → Ctrl+V → Enter."
            ),
            font=("Segoe UI", 11),
            text_color="#666666",
            justify="left"
        )
        wa_note.grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.whatsapp_enabled_var = tk.BooleanVar(value=self.settings.get("whatsapp_enabled", False))
        ctk.CTkCheckBox(
            inner,
            text="Auto-send WhatsApp message whenever a new job application is saved",
            variable=self.whatsapp_enabled_var,
            font=entry_font,
            text_color="#1a1a1a"
        ).grid(row=7, column=0, columnspan=2, sticky="w", pady=(0, 12))

        ctk.CTkLabel(inner, text="Browser to use", font=label_font, text_color="#1a1a1a").grid(
            row=8, column=0, sticky="w", pady=8
        )
        browser_display = {"default": "Default (System)", "chrome": "Google Chrome", "edge": "Microsoft Edge"}
        current_browser = self.settings.get("whatsapp_browser", "default")
        self.browser_var = tk.StringVar(value=browser_display.get(current_browser, "Default (System)"))
        ctk.CTkOptionMenu(
            inner,
            variable=self.browser_var,
            values=["Default (System)", "Google Chrome", "Microsoft Edge"],
            width=340,
            font=entry_font
        ).grid(row=8, column=1, pady=8, padx=10, sticky="w")

        ctk.CTkLabel(inner, text="WhatsApp Wait Time (seconds)", font=label_font, text_color="#1a1a1a").grid(
            row=9, column=0, sticky="w", pady=8
        )
        self.wait_time_var = tk.StringVar(value=str(self.settings.get("whatsapp_wait_time", 25)))
        ctk.CTkEntry(inner, textvariable=self.wait_time_var, width=100, font=entry_font).grid(
            row=9, column=1, pady=8, padx=10, sticky="w"
        )
        ctk.CTkLabel(
            inner,
            text="Raise this (e.g. 30-35) if your internet is slow and the message isn't sending.",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).grid(row=10, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ctk.CTkButton(
            inner,
            text="🔍 Open WhatsApp Web to check / switch login",
            command=self.test_whatsapp_login,
            width=340,
            height=36,
            fg_color="#075e54",
            hover_color="#054c44",
            font=("Segoe UI", 13, "bold")
        ).grid(row=11, column=0, columnspan=2, pady=(0, 25))

        # ---------------- Developer Copy (transparent, opt-in) ----------------

        ctk.CTkLabel(
            inner,
            text="🧑‍💻 Developer Copy",
            font=("Segoe UI", 17, "bold"),
            text_color="#1a1a1a"
        ).grid(row=12, column=0, columnspan=2, sticky="w", pady=(0, 12))

        dev_note = ctk.CTkLabel(
            inner,
            text=(
                f"If turned ON, a short TEXT SUMMARY (no resume file) of every application you save\n"
                f"is also emailed to the app developer ({DEVELOPER}) at {DEVELOPER_EMAIL}.\n"
                f"This is completely optional and OFF by default. Turning it off stops it immediately."
            ),
            font=("Segoe UI", 11),
            text_color="#666666",
            justify="left"
        )
        dev_note.grid(row=13, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.dev_copy_var = tk.BooleanVar(value=self.settings.get("developer_copy_consent", False))
        ctk.CTkCheckBox(
            inner,
            text="Send a copy of every saved application to the developer (optional)",
            variable=self.dev_copy_var,
            font=entry_font,
            text_color="#1a1a1a"
        ).grid(row=14, column=0, columnspan=2, sticky="w", pady=(0, 25))

        # ---------------- Message Templates ----------------

        ctk.CTkLabel(
            inner,
            text="✏️ Message Templates",
            font=("Segoe UI", 17, "bold"),
            text_color="#1a1a1a"
        ).grid(row=15, column=0, columnspan=2, sticky="w", pady=(0, 12))

        ctk.CTkLabel(
            inner,
            text="You can use {company}, {role}, {hr_name}, {location} as placeholders.",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).grid(row=16, column=0, columnspan=2, sticky="w", pady=(0, 10))

        ctk.CTkLabel(inner, text="Email Subject", font=label_font, text_color="#1a1a1a").grid(
            row=17, column=0, sticky="nw", pady=8
        )
        self.subject_box = ctk.CTkEntry(inner, width=340, font=entry_font)
        self.subject_box.insert(0, self.settings.get("email_subject_template", ""))
        self.subject_box.grid(row=17, column=1, pady=8, padx=10)

        ctk.CTkLabel(inner, text="Email Body", font=label_font, text_color="#1a1a1a").grid(
            row=18, column=0, sticky="nw", pady=8
        )
        self.body_box = ctk.CTkTextbox(inner, width=340, height=120, font=entry_font)
        self.body_box.insert("1.0", self.settings.get("email_body_template", ""))
        self.body_box.grid(row=18, column=1, pady=8, padx=10)

        ctk.CTkLabel(inner, text="WhatsApp Message", font=label_font, text_color="#1a1a1a").grid(
            row=19, column=0, sticky="nw", pady=8
        )
        self.whatsapp_box = ctk.CTkTextbox(inner, width=340, height=90, font=entry_font)
        self.whatsapp_box.insert("1.0", self.settings.get("whatsapp_message_template", ""))
        self.whatsapp_box.grid(row=19, column=1, pady=8, padx=10)

        reply_note = ctk.CTkLabel(
            inner,
            text=(
                "Note: This only sends the FIRST message. If HR replies by email or WhatsApp,\n"
                "you will reply to them yourself — this app never auto-replies."
            ),
            font=("Segoe UI", 12, "bold"),
            text_color="#b45309",
            justify="left"
        )
        reply_note.grid(row=20, column=0, columnspan=2, sticky="w", pady=(15, 15))

        ctk.CTkButton(
            inner,
            text="💾 Save Settings",
            command=self.save,
            width=220,
            height=42,
            fg_color="#28a745",
            hover_color="#218838",
            font=("Segoe UI", 14, "bold")
        ).grid(row=21, column=0, columnspan=2, pady=10)

        return frame

    def save(self):

        self.settings["gmail_address"] = self.email_var.get().strip()
        self.settings["gmail_app_password"] = self.password_var.get().strip()
        self.settings["email_enabled"] = bool(self.email_enabled_var.get())
        self.settings["whatsapp_enabled"] = bool(self.whatsapp_enabled_var.get())

        browser_map = {"Default (System)": "default", "Google Chrome": "chrome", "Microsoft Edge": "edge"}
        self.settings["whatsapp_browser"] = browser_map.get(self.browser_var.get(), "default")

        try:
            self.settings["whatsapp_wait_time"] = max(10, int(self.wait_time_var.get().strip()))
        except ValueError:
            self.settings["whatsapp_wait_time"] = 25
        self.settings["developer_copy_consent"] = bool(self.dev_copy_var.get())
        self.settings["developer_copy_consent_asked"] = True
        self.settings["email_subject_template"] = self.subject_box.get().strip()
        self.settings["email_body_template"] = self.body_box.get("1.0", "end").strip()
        self.settings["whatsapp_message_template"] = self.whatsapp_box.get("1.0", "end").strip()

        save_settings(self.settings)

        messagebox.showinfo("Settings", "Settings saved successfully.")

    def test_whatsapp_login(self):
        """
        Opens web.whatsapp.com in the currently selected browser (WITHOUT
        sending anything) so the user can check which number is logged in,
        or log out and re-scan the QR code with the correct phone
        (8077693361), before saving a job and triggering an actual send.
        """
        from notifier import open_whatsapp_web

        browser_map = {"Default (System)": "default", "Google Chrome": "chrome", "Microsoft Edge": "edge"}
        temp_settings = dict(self.settings)
        temp_settings["whatsapp_browser"] = browser_map.get(self.browser_var.get(), "default")

        try:
            warning = open_whatsapp_web("https://web.whatsapp.com", temp_settings)

            base_msg = (
                "Opening WhatsApp Web. Check the top-left — if it's not "
                "logged in as 8077693361, click the 3 dots (or profile "
                "icon) → Log out, then scan the QR code again using that "
                "phone's WhatsApp > Linked Devices."
            )

            if warning:
                messagebox.showwarning("WhatsApp Web", warning.strip() + "\n\n" + base_msg)
            else:
                messagebox.showinfo("WhatsApp Web", base_msg)

        except Exception as e:
            messagebox.showerror("WhatsApp Web", f"Could not open browser: {e}")
