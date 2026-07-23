"""
==========================================
Job Tracker Pro
Configuration File
Developer : Yogendra Kumar
==========================================
"""

import os

# Base Folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Project Folders
DATA_FOLDER = os.path.join(BASE_DIR, "Data")
LOG_FOLDER = os.path.join(BASE_DIR, "Logs")
RESUME_FOLDER = os.path.join(BASE_DIR, "Resume")
IMAGE_FOLDER = os.path.join(BASE_DIR, "Images")
ASSETS_FOLDER = os.path.join(BASE_DIR, "Assets")

# Excel Database
# NOTE: Single source of truth for the Excel file path. All screens
# (add_job, dashboard, view_jobs, search_jobs, reports) import
# EXCEL_FILE from here instead of hardcoding the filename, so every
# part of the app always reads/writes the SAME file.
EXCEL_FILE = os.path.join(BASE_DIR, "jobs.xlsx")

# Report Folder
REPORT_FOLDER = os.path.join(BASE_DIR, "Reports")

# Create folders if they don't exist
folders = [
    DATA_FOLDER,
    LOG_FOLDER,
    RESUME_FOLDER,
    IMAGE_FOLDER,
    ASSETS_FOLDER,
    REPORT_FOLDER
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Application Details
APP_NAME = "Job Tracker Pro"
VERSION = "1.0"
DEVELOPER = "Yogendra Kumar"

# ==========================================
# Developer Copy (transparent, opt-in only)
# ------------------------------------------
# If a user AGREES (see the consent popup on
# first launch, or the toggle in Settings),
# one copy of every saved job application is
# also emailed to this address. This address
# is fixed in the source code on purpose -
# so anyone reading this file can see exactly
# where their data would go, in plain sight.
# It is NEVER sent unless the user has said
# "Yes" to the consent prompt.
# ==========================================
DEVELOPER_EMAIL = "yogendra2020kr@gmail.com"