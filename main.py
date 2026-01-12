import tkinter as tk
import sys
import os

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ui.auth_view import AuthView
from src.ui.dashboard_view import DashboardView
from src.ui.plant_form import PlantForm
from src.ui.detail_view import DetailView
from src.ui.report_view import ReportView

class PlantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plant Tracking System")
        self.geometry("800x600")
        
        self.current_user = None
        self.selected_plant = None
        
        # Container for all views
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Define all pages
        for F in (AuthView, DashboardView, PlantForm, DetailView, ReportView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("AuthView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def set_current_user(self, user):
        self.current_user = user

if __name__ == "__main__":
    app = PlantApp()
    app.mainloop()
