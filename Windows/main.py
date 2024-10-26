import tkinter as tk
from tkinter import messagebox
import os
import json

# 文件名用于存储用户凭据
CREDENTIALS_FILE = "credentials.json"

class LoginWindow:
    def __init__(self, master, on_login_success):
        self.master = master
        self.on_login_success = on_login_success
        self.master.title("Login")
        self.master.geometry("300x200")

        # 用户名标签和输入框
        self.label_username = tk.Label(master, text="Username:", font=("Arial", 12))
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(master, width=30, font=("Arial", 12))
        self.entry_username.pack(pady=5)

        # 密码标签和输入框
        self.label_password = tk.Label(master, text="Password:", font=("Arial", 12))
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(master, width=30, show="*", font=("Arial", 12))
        self.entry_password.pack(pady=5)

        # "记住我"复选框
        self.remember_var = tk.BooleanVar()
        self.check_remember = tk.Checkbutton(master, text="Remember Me", variable=self.remember_var, font=("Arial", 10))
        self.check_remember.pack(pady=5)

        # 登录按钮
        self.button_login = tk.Button(master, text="Login", command=self.login, font=("Arial", 12))
        self.button_login.pack(pady=10)

        # 加载存储的凭据（如果有）
        self.load_credentials()

    def load_credentials(self):
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, "r") as f:
                try:
                    creds = json.load(f)
                    self.entry_username.insert(0, creds.get("username", ""))
                    self.entry_password.insert(0, creds.get("password", ""))
                    self.remember_var.set(True)
                except json.JSONDecodeError:
                    pass  # 如果文件内容无效，则忽略

    def save_credentials(self, username, password):
        creds = {
            "username": username,
            "password": password
        }
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(creds, f)

    def clear_credentials(self):
        if os.path.exists(CREDENTIALS_FILE):
            os.remove(CREDENTIALS_FILE)

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        # 简单的凭据验证
        valid_credentials = {
            "user1": "password1",
            "admin": "admin123",
            "newUser": "newpassword"
        }

        if username in valid_credentials and valid_credentials[username] == password:
            if self.remember_var.get():
                self.save_credentials(username, password)
            else:
                self.clear_credentials()
            self.master.destroy()
            self.on_login_success(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

class BasicWindowsClient:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Basic Windows Client")
        self.root.geometry("300x200")

        # 创建欢迎标签
        self.label = tk.Label(root, text=f"Welcome, {self.username}!", font=("Arial", 12))
        self.label.pack(pady=10)

        # 创建一个文本输入
        self.entry = tk.Entry(root, width=30, font=("Arial", 12))
        self.entry.pack(pady=10)

        # 创建一个按钮
        self.button = tk.Button(root, text="Click Me", command=self.on_button_click, font=("Arial", 12))
        self.button.pack(pady=10)

        # 创建一个注销按钮
        self.button_logout = tk.Button(root, text="Logout", command=self.logout, font=("Arial", 12), fg="red")
        self.button_logout.pack(pady=10)

    def on_button_click(self):
        user_input = self.entry.get().strip()
        if user_input:
            self.label.config(text=f"Hello, {user_input}! Welcome to the Basic Windows Client.")
        else:
            messagebox.showinfo("Info", "Please enter your name.")

    def logout(self):
        # 删除存储的凭据（如果不需要记住）
        if not os.path.exists(CREDENTIALS_FILE):
            pass  # 如果没有记住凭据，什么也不做
        else:
            pass  # 如果有记住凭据，可以选择清除或保留
        self.root.destroy()
        main()  # 重新启动登录过程

def main():
    # 创建主应用程序窗口
    login_root = tk.Tk()
    # 初始化登录窗口
    login_app = LoginWindow(login_root, on_login_success=launch_main_app)
    login_root.mainloop()

def launch_main_app(username):
    main_root = tk.Tk()
    app = BasicWindowsClient(main_root, username)
    main_root.mainloop()

if __name__ == "__main__":
    main()


