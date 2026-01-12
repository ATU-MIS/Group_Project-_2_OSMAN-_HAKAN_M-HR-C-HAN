import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from src.services.plant_service import PlantService

class DetailView(tk.Frame):
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
        
        self.plant = getattr(self.controller, 'selected_plant', None)
        if self.plant:
            self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Frame(self, bg="white", padx=20, pady=10)
        header.pack(fill=tk.X)
        tk.Button(header, text="< Back", command=lambda: self.controller.show_frame("DashboardView"), bg="#f0f2f5", relief=tk.FLAT).pack(side=tk.LEFT)
        tk.Label(header, text=self.plant.name, font=("Arial", 16, "bold"), bg="white").pack(side=tk.LEFT, padx=20)

        main_content = tk.Frame(self, bg="#f0f2f5")
        main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Details & Actions
        top_frame = tk.Frame(main_content, bg="#f0f2f5")
        top_frame.pack(fill=tk.X)
        
        # Info Card
        info_card = tk.LabelFrame(top_frame, text="Plant Info", bg="white", padx=10, pady=10)
        info_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Reload full details including schedule
        plant, water_sch, fert_sch = self.plant_service.get_plant_details(self.plant.plant_id)
        
        tk.Label(info_card, text=f"Species: {plant.species}", bg="white").pack(anchor=tk.W)
        tk.Label(info_card, text=f"Type: {plant.type}", bg="white").pack(anchor=tk.W)
        if water_sch:
             tk.Label(info_card, text=f"Next Water: {water_sch.next_date}", bg="white", fg="blue").pack(anchor=tk.W)
        if fert_sch:
             tk.Label(info_card, text=f"Next Fertilize: {fert_sch.next_date}", bg="white", fg="green").pack(anchor=tk.W)

        # Actions Card
        action_card = tk.LabelFrame(top_frame, text="Quick Actions", bg="white", padx=10, pady=10)
        action_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Button(action_card, text="💧 Water Plant", command=self.do_water, bg="#2196f3", fg="white", width=20).pack(pady=5)
        tk.Button(action_card, text="🧪 Fertilize", command=self.do_fertilize, bg="#4caf50", fg="white", width=20).pack(pady=5)

        # History
        history_frame = tk.LabelFrame(main_content, text="Care History", bg="white", padx=10, pady=10)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Treeview
        columns = ("Date", "Type", "Notes")
        tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Type", text="Type")
        tree.heading("Notes", text="Notes")
        
        tree.column("Date", width=100)
        tree.column("Type", width=100)
        tree.column("Notes", width=300)
        
        history = self.plant_service.get_care_history(self.plant.plant_id)
        for h in history:
            tree.insert("", tk.END, values=(h.date, h.care_type, h.notes))
            
        tree.pack(fill=tk.BOTH, expand=True)

    def do_water(self):
        notes = simpledialog.askstring("Watering", "Add notes (optional):")
        if notes is None: return
        self.plant_service.water_plant(self.plant.plant_id, notes)
        messagebox.showinfo("Success", "Plant watered!")
        self.refresh()

    def do_fertilize(self):
        notes = simpledialog.askstring("Fertilizing", "Add notes (optional):")
        if notes is None: return
        self.plant_service.fertilize_plant(self.plant.plant_id, notes)
        messagebox.showinfo("Success", "Plant fertilized!")
        self.refresh()
