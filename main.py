import customtkinter as ctk
from src.app import TaskTrackerApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = TaskTrackerApp(root)
    root.mainloop()