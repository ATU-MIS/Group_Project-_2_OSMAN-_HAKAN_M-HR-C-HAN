import tkinter as tk
from tkinter import ttk
from src.services.plant_service import PlantService
from src.services.notification_service import NotificationService

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.plant_service = PlantService()
        self.notification_service = NotificationService()
        
        self.configure(bg="#f0f2f5")
        
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh_data()

    def refresh_data(self):
        # Clear existing
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def create_widgets(self):
        user = self.controller.current_user
        if not user:
            return

        # Header
        header = tk.Frame(self, bg="#2e7d32", height=60)
        header.pack(fill=tk.X)
        
        tk.Label(header, text=f"Welcome, {user.name}", bg="#2e7d32", fg="white", font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Button(header, text="Logout", command=lambda: self.controller.show_frame("AuthView"), bg="#d32f2f", fg="white").pack(side=tk.RIGHT, padx=10, pady=10)
        tk.Button(header, text="+ Add Plant", command=lambda: self.controller.show_frame("PlantForm"), bg="white", fg="#2e7d32").pack(side=tk.RIGHT, padx=10, pady=10)

        # Content
        content = tk.Frame(self, bg="#f0f2f5")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Notifications Area
        notifs = self.notification_service.check_due_dates(user.user_id)
        if notifs:
            notif_frame = tk.LabelFrame(content, text="Notifications", bg="white", fg="red", font=("Arial", 10, "bold"), padx=10, pady=10)
            notif_frame.pack(fill=tk.X, pady=(0, 20))
            for n in notifs:
                tk.Label(notif_frame, text=f"• {n['message']} ({n['date']})", bg="white", fg="#d32f2f").pack(anchor=tk.W)
        
        # Plant List
        list_frame = tk.Frame(content, bg="#f0f2f5")
        list_frame.pack(fill=tk.BOTH, expand=True)

        plants = self.plant_service.get_plants_by_user(user.user_id)
        
        if not plants:
            tk.Label(list_frame, text="No plants found. Add one to get started!", bg="#f0f2f5", font=("Arial", 14)).pack(pady=40)
        else:
            # Scrollable Frame could be better but for MVP simple pack
            for plant in plants:
                self.create_plant_card(list_frame, plant)

    def create_plant_card(self, parent, plant):
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, borderwidth=1, padx=10, pady=10)
        card.pack(fill=tk.X, pady=5)
        
        # Icon (Placeholder)
        tk.Label(card, text="🌿", font=("Arial", 24), bg="white").pack(side=tk.LEFT, padx=10)
        
        # Info
        info = tk.Frame(card, bg="white")
        info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(info, text=plant.name, font=("Arial", 14, "bold"), bg="white", anchor=tk.W).pack(fill=tk.X)
        tk.Label(info, text=f"{plant.species} • {plant.type}", font=("Arial", 10), fg="gray", bg="white", anchor=tk.W).pack(fill=tk.X)

        # Action
        tk.Button(card, text="Details", command=lambda p=plant: self.open_details(p), bg="#1976d2", fg="white").pack(side=tk.RIGHT)

    def open_details(self, plant):
        self.controller.selected_plant = plant
        self.controller.show_frame("DetailView")
