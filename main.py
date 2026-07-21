import customtkinter as ctk
from gui import JobTrackerGUI


def main():

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = JobTrackerGUI()
    app.mainloop()


if __name__ == "__main__":
    main()