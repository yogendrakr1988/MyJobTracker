"""
==========================================
Job Tracker Pro
GUI File
Developer : Yogendra Kumar
==========================================
"""

import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

from screens.dashboard import DashboardScreen
from screens.add_job import AddJobScreen
from screens.view_jobs import ViewJobsScreen
from screens.search_jobs import SearchJobsScreen
from screens.reports import ReportsScreen
from screens.resume import ResumeScreen
from screens.settings import SettingsScreen
from settings_manager import load_settings, save_settings
from config import DEVELOPER, DEVELOPER_EMAIL


class JobTrackerGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Window Settings
        self.title("Job Tracker Pro")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Current Screen
        self.main_frame = None

        # Create Sidebar
        self.create_sidebar()

        # Open Dashboard
        self.show_dashboard()

        # Ask (once) whether the user agrees to send a copy of every
        # saved application to the developer. Fully optional, fully
        # visible - never happens silently. See maybe_ask_developer_consent.
        self.after(400, self.maybe_ask_developer_consent)

    # ==========================================
    # Developer Copy - one-time consent popup
    # ==========================================

    def maybe_ask_developer_consent(self):

        settings = load_settings()

        if settings.get("developer_copy_consent_asked"):
            return

        settings["developer_copy_consent_asked"] = True

        agreed = messagebox.askyesno(
            "Send a Copy to the Developer? (Optional)",
            f"This app was built by {DEVELOPER}.\n\n"
            f"Would you like to also send a COPY of every job application "
            f"you save to the developer's email ({DEVELOPER_EMAIL})? "
            f"This helps {DEVELOPER} see how the app is being used.\n\n"
            "This is completely OPTIONAL:\n"
            "  • If you choose 'No', nothing extra is ever sent - only your "
            "own HR email/WhatsApp messages go out as normal.\n"
            "  • You can turn this ON or OFF anytime later in Settings.\n\n"
            "Do you agree to send a copy to the developer?",
            parent=self
        )

        settings["developer_copy_consent"] = bool(agreed)

        save_settings(settings)

    # ==========================================
    # Sidebar
    # ==========================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        title = ctk.CTkLabel(
            self.sidebar,
            text="JOB TRACKER PRO",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=30)

        buttons = [
            "Dashboard",
            "Add Job",
            "View Jobs",
            "Search Jobs",
            "Reports",
            "Resume",
            "Settings",
            "Exit"
        ]

        for btn in buttons:

            button = ctk.CTkButton(
                self.sidebar,
                text=btn,
                width=180,
                height=40,
                command=lambda b=btn: self.menu_click(b)
            )

            button.pack(pady=8)

    # ==========================================
    # Dashboard Screen
    # ==========================================

    def show_dashboard(self):

        if self.main_frame is not None:
            self.main_frame.destroy()

        dashboard = DashboardScreen(self)
        self.main_frame = dashboard.show()

    # ==========================================
    # Add Job Screen
    # ==========================================

    def show_add_job(self, prefill=None):

        if self.main_frame is not None:
            self.main_frame.destroy()

        add_job = AddJobScreen(self)
        self.main_frame = add_job.show()

        if prefill:
            add_job.fill_form(prefill)

    # ==========================================
    # View Jobs Screen
    # ==========================================

    def show_view_jobs(self):

        if self.main_frame is not None:
            self.main_frame.destroy()

        view_jobs = ViewJobsScreen(self)
        self.main_frame = view_jobs.show()

    # ==========================================
    # Search Jobs Screen
    # ==========================================

    def show_search_jobs(self):

        if self.main_frame is not None:
            self.main_frame.destroy()

        search = SearchJobsScreen(self)
        self.main_frame = search.show()

    # ==========================================
    # Reports Screen
    # ==========================================

    def show_reports(self):

        if self.main_frame is not None:
            self.main_frame.destroy()

        reports = ReportsScreen(self)
        self.main_frame = reports.show()

    # ==========================================
    # Resume Screen
    # ==========================================

    def show_resume(self):

        if self.main_frame is not None:
            self.main_frame.destroy()

        resume = ResumeScreen(self)
        self.main_frame = resume.show()

    # ==========================================
    # Settings Screen
    # ==========================================

    def show_settings(self):

        if self.main_frame is not None:
            self.main_frame.destroy()

        settings = SettingsScreen(self)
        self.main_frame = settings.show()

    # ==========================================
    # Button Click Event
    # ==========================================

    def menu_click(self, button_name):

        print(f"{button_name} Button Clicked")

        if button_name == "Dashboard":

            self.show_dashboard()

        elif button_name == "Add Job":

            self.show_add_job()

        elif button_name == "View Jobs":

            self.show_view_jobs()

        elif button_name == "Search Jobs":

            self.show_search_jobs()

        elif button_name == "Reports":

            self.show_reports()

        elif button_name == "Resume":

            self.show_resume()

        elif button_name == "Settings":

            self.show_settings()

        elif button_name == "Exit":

            self.destroy()

    # ==========================================
    # Update Date & Time
    # ==========================================

    def update_datetime(self):

        try:

            current = datetime.now().strftime("%d-%b-%Y   %I:%M:%S %p")

            if hasattr(self, "datetime_label"):
                self.datetime_label.configure(
                    text=f"📅 {current}"
                )

            self.after(1000, self.update_datetime)

        except Exception:
            pass