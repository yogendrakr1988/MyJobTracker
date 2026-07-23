import os
import shutil
import subprocess
import sys

import customtkinter as ctk
from tkinter import filedialog, messagebox

from config import RESUME_FOLDER


class ResumeScreen:

    def __init__(self, parent):
        self.parent = parent
        self.list_frame = None

    def open_file(self, path):

        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.call(["open", path])
            else:
                subprocess.call(["xdg-open", path])

        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")

    def upload_resume(self):

        file = filedialog.askopenfilename(
            filetypes=[
                ("PDF Files", "*.pdf"),
                ("Word Files", "*.doc *.docx"),
                ("All Files", "*.*")
            ]
        )

        if not file:
            return

        dest = os.path.join(RESUME_FOLDER, os.path.basename(file))

        try:
            shutil.copy(file, dest)
            messagebox.showinfo("Success", "Resume uploaded successfully.")
            self.refresh()

        except Exception as e:
            messagebox.showerror("Error", f"Could not upload file:\n{e}")

    def refresh(self):

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        files = []

        if os.path.exists(RESUME_FOLDER):
            files = [
                f for f in os.listdir(RESUME_FOLDER)
                if os.path.isfile(os.path.join(RESUME_FOLDER, f))
            ]

        if not files:

            ctk.CTkLabel(
                self.list_frame,
                text="No resumes found. Click 'Upload Resume' to add one.",
                font=("Segoe UI", 14),
                text_color="#1a1a1a"
            ).pack(pady=20)

            return

        for f in files:

            row = ctk.CTkFrame(self.list_frame, fg_color="#f5f5f5", corner_radius=10)
            row.pack(fill="x", pady=6, padx=5)

            ctk.CTkLabel(
                row,
                text=f"📄  {f}",
                font=("Segoe UI", 13),
                text_color="#1a1a1a",
                anchor="w"
            ).pack(side="left", padx=15, pady=10, fill="x", expand=True)

            ctk.CTkButton(
                row,
                text="Open",
                width=90,
                command=lambda path=os.path.join(RESUME_FOLDER, f): self.open_file(path)
            ).pack(side="right", padx=10, pady=8)

    def show(self):

        frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame,
            text="📁 Resume Manager",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=(0, 15), anchor="w")

        ctk.CTkButton(
            frame,
            text="⬆️  Upload Resume",
            command=self.upload_resume,
            width=200,
            height=40,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 15))

        card = ctk.CTkFrame(frame, fg_color="white", corner_radius=15)
        card.pack(fill="both", expand=True)

        self.list_frame = ctk.CTkFrame(card, fg_color="white")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.refresh()

        return frame
