import tkinter as tk
from tkinter import ttk, messagebox
from src.services.plant_service import PlantService
from datetime import datetime

class PlantForm(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.plant_service = PlantService()
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
        tk.Label(header, text="Add New Plant", font=("Arial", 16, "bold"), bg="white").pack(side=tk.LEFT, padx=20)

        # Form Container
        container = tk.Frame(self, bg="white", padx=40, pady=20, relief=tk.RAISED)
        container.pack(pady=20)

        # Basic Info
        tk.Label(container, text="Basic Information", font=("Arial", 12, "bold"), bg="white", fg="#2e7d32").grid(row=0, columnspan=2, pady=10, sticky="w")
        
        tk.Label(container, text="Name:", bg="white").grid(row=1, column=0, sticky="e", pady=5)
        self.name_entry = tk.Entry(container, width=30)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(container, text="Species:", bg="white").grid(row=2, column=0, sticky="e", pady=5)
        self.species_entry = tk.Entry(container, width=30)
        self.species_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(container, text="Type:", bg="white").grid(row=3, column=0, sticky="e", pady=5)
        self.type_combo = ttk.Combobox(container, values=["Indoor", "Outdoor", "Succulent", "Vegetable"], width=27)
        self.type_combo.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(container, text="Planting Date (YYYY-MM-DD):", bg="white").grid(row=4, column=0, sticky="e", pady=5)
        self.date_entry = tk.Entry(container, width=30)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=4, column=1, padx=10, pady=5)

        # Schedule
        tk.Label(container, text="Care Schedule", font=("Arial", 12, "bold"), bg="white", fg="#2e7d32").grid(row=5, columnspan=2, pady=10, sticky="w")

        tk.Label(container, text="Water Every (days):", bg="white").grid(row=6, column=0, sticky="e", pady=5)
        self.water_freq = tk.Spinbox(container, from_=1, to=365, width=28)
        self.water_freq.grid(row=6, column=1, padx=10, pady=5)
        
        tk.Label(container, text="Water Amount (ml):", bg="white").grid(row=7, column=0, sticky="e", pady=5)
        self.water_amt = tk.Entry(container, width=30)
        self.water_amt.grid(row=7, column=1, padx=10, pady=5)

        tk.Label(container, text="Fertilize Every (days):", bg="white").grid(row=8, column=0, sticky="e", pady=5)
        self.fert_freq = tk.Spinbox(container, from_=1, to=365, width=28)
        self.fert_freq.grid(row=8, column=1, padx=10, pady=5)

        tk.Label(container, text="Fertilizer Type:", bg="white").grid(row=9, column=0, sticky="e", pady=5)
        self.fert_type = tk.Entry(container, width=30)
        self.fert_type.grid(row=9, column=1, padx=10, pady=5)

        # Submit
        tk.Button(container, text="Save Plant", command=self.save_plant, bg="#2e7d32", fg="white", font=("Arial", 12), width=20).grid(row=10, columnspan=2, pady=20)

    def save_plant(self):
        user = self.controller.current_user
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Error", "Name is required")
            return

        try:
            plant_id = self.plant_service.add_plant(
                user.user_id,
                name,
                self.species_entry.get(),
                self.type_combo.get(),
                self.date_entry.get()
            )

            self.plant_service.set_schedules(
                plant_id,
                int(self.water_freq.get()),
                int(self.fert_freq.get()),
                self.water_amt.get(),
                self.fert_type.get()
            )

            messagebox.showinfo("Success", "Plant added successfully!")
            self.controller.show_frame("DashboardView")
        except Exception as e:
            messagebox.showerror("Error", str(e))
