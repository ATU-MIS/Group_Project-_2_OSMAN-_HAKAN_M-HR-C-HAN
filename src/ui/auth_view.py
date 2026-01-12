import tkinter as tk
from tkinter import messagebox
from src.services.auth_service import AuthService

class AuthView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.auth_service = AuthService()
        
        self.configure(bg="#f0f2f5")
        self.create_widgets()

    def create_widgets(self):
        # Container
        container = tk.Frame(self, bg="white", padx=40, pady=40, relief=tk.RAISED, borderwidth=1)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title
        tk.Label(container, text="Plant Tracker", font=("Helvetica", 24, "bold"), bg="white", fg="#2e7d32").pack(pady=(0, 20))

        # Email
        tk.Label(container, text="Email", bg="white", font=("Arial", 10)).pack(anchor=tk.W)
        self.email_entry = tk.Entry(container, width=30, font=("Arial", 12))
        self.email_entry.pack(pady=(0, 10))

        # Password
        tk.Label(container, text="Password", bg="white", font=("Arial", 10)).pack(anchor=tk.W)
        self.password_entry = tk.Entry(container, width=30, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=(0, 20))

        # Buttons
        btn_frame = tk.Frame(container, bg="white")
        btn_frame.pack()

        tk.Button(btn_frame, text="Login", command=self.login, bg="#2e7d32", fg="white", font=("Arial", 12), width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Register", command=self.register, bg="#1976d2", fg="white", font=("Arial", 12), width=10).pack(side=tk.LEFT, padx=5)
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        user = self.auth_service.login(email, password)
        if user:
            self.controller.set_current_user(user)
            self.controller.show_frame("DashboardView")
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        # Simple registration dialog or switch to register view
        # For simplicity, we'll just check fields and register right here if not empty
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showwarning("Warning", "Please fill valid email and password")
            return

        # Basic prompt for name
        top = tk.Toplevel(self)
        top.title("Complete Registration")
        top.geometry("300x200")
        
        tk.Label(top, text="Name").pack()
        name_entry = tk.Entry(top)
        name_entry.pack()
        
        tk.Label(top, text="Surname").pack()
        surname_entry = tk.Entry(top)
        surname_entry.pack()
        
        def complete():
            name = name_entry.get()
            surname = surname_entry.get()
            if name and surname:
                user = self.auth_service.register(name, surname, email, password)
                if user:
                    messagebox.showinfo("Success", "Registration successful! Please login.")
                    top.destroy()
                else:
                    messagebox.showerror("Error", "Registration failed (Email might be taken)")
            else:
                messagebox.showwarning("Warning", "All fields required")

        tk.Button(top, text="Submit", command=complete).pack(pady=10)
