"""
==========================================
Job Tracker Pro
Notifier
Sends the FIRST application email (Gmail)
and the FIRST WhatsApp message + resume
(WhatsApp Web, via Selenium) when a new
job is saved.

IMPORTANT:
This module only SENDS messages. It never
reads or replies to anything. Any reply from
HR (email or WhatsApp) must be answered by
you, manually.
==========================================
"""

import os
import ssl
import smtplib
from email.message import EmailMessage

from settings_manager import load_settings
from config import DEVELOPER_EMAIL, DEVELOPER
from whatsapp_selenium import send_whatsapp_message


def format_template(template, data):

    try:
        return template.format(
            company=data.get("Company", "") or "",
            role=data.get("Role", "") or "",
            hr_name=data.get("HR Name", "") or "Hiring Manager",
            location=data.get("Location", "") or ""
        )
    except Exception:
        return template


def format_phone(phone):

    phone = phone.strip().replace(" ", "").replace("-", "")

    if phone.startswith("+"):
        return phone

    digits = "".join(ch for ch in phone if ch.isdigit())

    if len(digits) == 10:
        return "+91" + digits

    return "+" + digits


def send_email(job_data):
    """
    Sends the application email via Gmail (App Password).
    Returns (success: bool, message: str)
    """

    settings = load_settings()

    if not settings.get("email_enabled"):
        return False, "Email auto-send is OFF (enable it in Settings)"

    sender = settings.get("gmail_address", "").strip()
    password = settings.get("gmail_app_password", "").strip()
    to_email = (job_data.get("HR Email") or "").strip()

    if not sender or not password:
        return False, "Gmail address / App Password not set in Settings"

    if not to_email:
        return False, "HR Email is empty, email skipped"

    subject = format_template(settings.get("email_subject_template", ""), job_data)
    body = format_template(settings.get("email_body_template", ""), job_data)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email
    msg.set_content(body)

    resume_path = (job_data.get("Resume") or "").strip()

    if resume_path and os.path.exists(resume_path):

        with open(resume_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(resume_path)

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=file_name
        )

    try:

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender, password)
            server.send_message(msg)

        return True, f"Email sent to {to_email}"

    except smtplib.SMTPAuthenticationError:
        return False, "Email failed: Gmail login rejected (check App Password in Settings)"

    except Exception as e:
        return False, f"Email failed: {e}"


def send_whatsapp(job_data):
    """
    Sends the application message + resume via WhatsApp Web, using a
    real Chrome browser controlled by Selenium (see whatsapp_selenium.py
    for the full flow and maintenance notes).

    IMPORTANT - things this function still CANNOT control:

    1) WHICH NUMBER the message is sent FROM is decided entirely by
       which WhatsApp account is logged in inside the automated Chrome
       profile. First time, a Chrome window will open and wait for you
       to scan the QR code (WhatsApp app > Linked Devices > Link a
       Device) using the 8077693361 phone. After that, it stays logged
       in automatically - you won't need to scan again unless you log
       out from your phone.

    2) WhatsApp occasionally changes its web page's HTML. If sends
       start failing with a "button not found" style error, the
       SELECTORS dictionary at the top of whatsapp_selenium.py needs a
       small update (see the MAINTENANCE notes in that file).

    Returns (success: bool, message: str)
    """

    settings = load_settings()

    if not settings.get("whatsapp_enabled"):
        return False, "WhatsApp auto-send is OFF (enable it in Settings)"

    phone_raw = (job_data.get("HR Mobile") or "").strip()

    if not phone_raw:
        return False, "HR Mobile is empty, WhatsApp skipped"

    phone = format_phone(phone_raw)
    message = format_template(settings.get("whatsapp_message_template", ""), job_data)
    wait_time = int(settings.get("whatsapp_wait_time", 25))
    resume_path = (job_data.get("Resume") or "").strip()

    try:
        return send_whatsapp_message(
            phone=phone,
            message=message,
            resume_path=resume_path or None,
            wait_time=wait_time,
        )
    except Exception as e:
        return False, f"WhatsApp failed (unexpected): {e}"


def send_developer_copy(job_data):
    """
    OPT-IN ONLY. Sends a small text summary of the saved job application
    to the app developer's email (config.DEVELOPER_EMAIL).

    This function does nothing unless the user has explicitly agreed to
    it - either via the first-launch consent popup, or by turning on
    "Send a copy to the developer" in Settings. If the user never agreed,
    this always returns False immediately without sending anything.

    Only a text SUMMARY is sent - the resume file is NOT attached, to
    keep the amount of personal data shared to the minimum needed.
    Returns (success: bool, message: str)
    """

    settings = load_settings()

    if not settings.get("developer_copy_consent"):
        return False, "Developer copy is OFF (you can enable it in Settings)"

    sender = settings.get("gmail_address", "").strip()
    password = settings.get("gmail_app_password", "").strip()

    if not sender or not password:
        return False, "Developer copy skipped: Gmail address / App Password not set in Settings"

    subject = f"[Job Tracker Pro] New application copy - {job_data.get('Company', '')}"

    body = (
        f"A Job Tracker Pro user ({sender}) saved a new application.\n"
        f"This copy was sent because the user opted in to 'Send a copy to the developer' in Settings.\n\n"
        f"Company     : {job_data.get('Company', '')}\n"
        f"Role        : {job_data.get('Role', '')}\n"
        f"Location    : {job_data.get('Location', '')}\n"
        f"HR Name     : {job_data.get('HR Name', '')}\n"
        f"HR Email    : {job_data.get('HR Email', '')}\n"
        f"HR Mobile   : {job_data.get('HR Mobile', '')}\n"
        f"Job Portal  : {job_data.get('Job Portal', '')}\n"
        f"Job Link    : {job_data.get('Job Link', '')}\n"
        f"Applied Date: {job_data.get('Applied Date', '')}\n"
        f"Status      : {job_data.get('Status', '')}\n"
        f"Notes       : {job_data.get('Notes', '')}\n"
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = DEVELOPER_EMAIL
    msg.set_content(body)

    try:

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender, password)
            server.send_message(msg)

        return True, f"Copy sent to developer ({DEVELOPER})"

    except smtplib.SMTPAuthenticationError:
        return False, "Developer copy failed: Gmail login rejected (check App Password in Settings)"

    except Exception as e:
        return False, f"Developer copy failed: {e}"
