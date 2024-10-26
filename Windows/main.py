import tkinter as tk
from tkinter import messagebox

class BasicWindowsClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Windows Client")
        self.root.geometry("300x150")

        # Create a label
        self.label = tk.Label(root, text="", font=("Arial", 12))
        self.label.pack(pady=10)

        # Create a text entry
        self.entry = tk.Entry(root, width=30, font=("Arial", 12))
        self.entry.pack(pady=10)

        # Create a button
        self.button = tk.Button(root, text="Click Me", command=self.on_button_click, font=("Arial", 12))
        self.button.pack(pady=10)

    def on_button_click(self):
        user_input = self.entry.get().strip()
        if user_input:
            self.label.config(text=f"Hello, {user_input}! Welcome to the Basic Windows Client.")
        else:
            messagebox.showinfo("Info", "Please enter your name.")

def main():
    root = tk.Tk()
    app = BasicWindowsClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
