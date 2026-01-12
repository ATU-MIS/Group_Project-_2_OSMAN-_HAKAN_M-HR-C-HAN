import tkinter as tk
from src.services.report_service import ReportService

class ReportView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.report_service = ReportService()
        self.configure(bg="#f0f2f5")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh()

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def create_widgets(self):
         # Header
        header = tk.Frame(self, bg="white", padx=20, pady=10)
        header.pack(fill=tk.X)
        tk.Button(header, text="< Back", command=lambda: self.controller.show_frame("DashboardView"), bg="#f0f2f5", relief=tk.FLAT).pack(side=tk.LEFT)
        tk.Label(header, text="Reports", font=("Arial", 16, "bold"), bg="white").pack(side=tk.LEFT, padx=20)

        container = tk.Frame(self, bg="white", padx=20, pady=20, relief=tk.RAISED)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        if self.controller.current_user:
            report_text = self.report_service.generate_report(self.controller.current_user.user_id)
            
            text_widget = tk.Text(container, font=("Consolas", 12), padx=10, pady=10)
            text_widget.insert(tk.END, report_text)
            text_widget.config(state=tk.DISABLED)
            text_widget.pack(fill=tk.BOTH, expand=True)
