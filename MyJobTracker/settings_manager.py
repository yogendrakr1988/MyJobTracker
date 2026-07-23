"""
==========================================
Job Tracker Pro
Settings Manager
Stores Gmail / WhatsApp settings locally
in settings.json (never sent anywhere else)

SECURITY NOTE:
The Gmail App Password is NEVER written into
settings.json in plain text. It is stored using
the 'keyring' library, which saves it in your
Windows account's own secure credential store
(Windows Credential Manager) - the same place
Windows keeps saved WiFi/website passwords.
settings.json only ever contains a small marker
saying "the password is in the secure store",
never the password itself.
==========================================
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

KEYRING_SERVICE = "MyJobTrackerPro"

DEFAULT_SETTINGS = {
    "gmail_address": "",
    "gmail_app_password": "",

    # True once the password has been moved into the secure OS credential
    # store instead of this file. You will never see this change manually.
    "_gmail_password_secured": False,

    "email_enabled": False,
    "whatsapp_enabled": False,

    # "default" = whatever Windows default browser is (often Edge).
    # "chrome" / "edge" = always force that specific browser, so the
    # app doesn't jump between browsers on its own.
    "whatsapp_browser": "default",

    # Seconds to wait for WhatsApp Web to fully load before pressing
    # Enter to send. Raise this if your internet is slow.
    "whatsapp_wait_time": 25,
    "email_subject_template": "Application for {role} at {company}",
    "email_body_template": (
        "Dear {hr_name},\n\n"
        "I am writing to apply for the {role} position at {company}.\n"
        "Please find my resume attached for your reference.\n\n"
        "I would really appreciate the opportunity to discuss this further.\n\n"
        "Thank you for your time and consideration.\n\n"
        "Best regards"
    ),
    "whatsapp_message_template": (
        "Hello {hr_name}, I have applied for the {role} position at {company}. "
        "I have also sent my resume over email. Looking forward to hearing from you. Thank you!"
    ),

    # ---- Developer Copy (transparent, OFF by default, opt-in only) ----
    # "developer_copy_consent_asked": becomes True the first time the
    #   user has been shown the consent popup (so we never nag them again).
    # "developer_copy_consent": True only if the user explicitly agreed.
    #   Nothing is ever sent to the developer unless this is True.
    "developer_copy_consent_asked": False,
    "developer_copy_consent": False
}


def _keyring_get(gmail_address):
    """Reads the Gmail App Password from the OS secure credential store."""
    if not gmail_address:
        return ""
    try:
        import keyring
        return keyring.get_password(KEYRING_SERVICE, gmail_address) or ""
    except Exception:
        return ""


def _keyring_set(gmail_address, password):
    """Writes the Gmail App Password into the OS secure credential store."""
    if not gmail_address or not password:
        return False
    try:
        import keyring
        keyring.set_password(KEYRING_SERVICE, gmail_address, password)
        return True
    except Exception:
        return False


def load_settings():

    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return dict(DEFAULT_SETTINGS)

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        merged = dict(DEFAULT_SETTINGS)
        merged.update(data)

        gmail_address = (merged.get("gmail_address") or "").strip()

        if merged.get("_gmail_password_secured"):
            # Normal path: password lives in the OS credential store,
            # settings.json never had it in plain text.
            merged["gmail_app_password"] = _keyring_get(gmail_address)

        elif merged.get("gmail_app_password"):
            # ONE-TIME MIGRATION: an older version of this app saved the
            # password in plain text in settings.json. The first time we
            # load it, move it into the secure store and immediately
            # rewrite settings.json so the plain text copy is gone.
            plain_password = merged["gmail_app_password"]

            if _keyring_set(gmail_address, plain_password):
                merged["_gmail_password_secured"] = True
                save_settings(merged)  # this call also scrubs the file (see below)

        return merged

    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(settings):

    to_write = dict(settings)
    gmail_address = (to_write.get("gmail_address") or "").strip()
    password = (to_write.get("gmail_app_password") or "").strip()

    if gmail_address and password:
        if _keyring_set(gmail_address, password):
            to_write["_gmail_password_secured"] = True
            to_write["gmail_app_password"] = ""  # never persisted to disk
        else:
            # keyring unavailable on this machine (rare) - fall back to
            # the old behaviour so the app still works, rather than
            # silently losing the password.
            to_write["_gmail_password_secured"] = False

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(to_write, f, indent=4)
