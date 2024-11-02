import tkinter as tk
from tkinter import messagebox


class RegisterUI(tk.Frame):
    def __init__(self, master, auth_controller):
        super().__init__(master)
        self.auth_controller = auth_controller
        self.create_widgets()

    def create_widgets(self):
        # Email Label and Entry
        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=0, column=0, padx=10, pady=10)

        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password Label and Entry
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)

        self.password_entry = tk.Entry(self, show="*", width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Login Button
        self.login_button = tk.Button(self, text="Register", command=self.register)
        self.login_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

    def register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password.")
            return

        # success, message = self.auth_controller.register(email, password)
        success, message = True, "none"
        if success:
            messagebox.Message(title="Success", message="Register successful! Check YOUR EMAIL to activate the Account", icon=None).show()
            # TODO: Transition to the dashboard UI
        else:
            messagebox.showerror("Error", message)
