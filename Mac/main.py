import tkinter as tk
from tkinter import messagebox
from src.utils.api_client import APIClient
from src.models.users import User
from src.ui.login_ui import LoginUI
from src.ui.dashboard_ui import DashboardUI

class MainApp:
    def __init__(self):
        """
        Initializes the Main Application for EZPark Windows Client.
        """
        self.api_client = APIClient()
        self.current_user = None  # 用于存储登录用户信息
        self.root = tk.Tk()
        self.root.title("EZPark")
        self.root.geometry("400x300")

        # 显示登录界面
        self.show_login_ui()

    def show_login_ui(self):
        """
        Displays the login UI.
        """
        self.clear_window()
        LoginUI(self.root)

    def show_dashboard_ui(self):
        """
        Displays the dashboard UI.
        """
        self.clear_window()
        DashboardUI(self.root, self.current_user, self.api_client)

    def on_login_success(self, user):
        """
        Callback function triggered after a successful login.

        Parameters:
        - user (User): The logged-in user.
        """
        self.current_user = user
        messagebox.showinfo("登录成功", f"欢迎 {user.name}!")
        self.show_dashboard_ui()

    def clear_window(self):
        """
        Clears the root window of all widgets.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        """
        Starts the main application loop.
        """
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("错误", f"发生未处理的错误: {str(e)}")
            self.root.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.run()
