# ui/login_ui.py
import tkinter as tk
from tkinter import messagebox
from ..controllers.auth_controller import AuthController
from ..utils.api_client import APIClient


class LoginUI:
    def __init__(self, master):
        self.master = master
        self.master.title("登录")
        self.master.geometry("300x200")

        # 初始化APIClient和AuthController
        api_client = APIClient()
        self.auth_controller = AuthController(api_client)

        # 创建GUI组件
        self.create_widgets()

    def create_widgets(self):
        # 邮箱标签和输入框
        tk.Label(self.master, text="邮箱").pack(pady=5)
        self.email_entry = tk.Entry(self.master)
        self.email_entry.pack(pady=5)

        # 密码标签和输入框
        tk.Label(self.master, text="密码").pack(pady=5)
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack(pady=5)

        # 登录按钮
        tk.Button(self.master, text="登录", command=self.login).pack(pady=20)

        # 注册按钮
        tk.Button(self.master, text="注册", command=self.open_register).pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showwarning("警告", "请填写所有字段")
            return

        success, message = self.auth_controller.login(email, password)
        if success:
            messagebox.showinfo("成功", message)
            # 这里可以打开主应用窗口或执行其他操作
        else:
            messagebox.showerror("错误", message)

    def open_register(self):
        self.master.withdraw()  # 隐藏登录窗口
        register_window = tk.Toplevel()
        import register_ui
        register_ui.RegisterUI(register_window)
        register_window.protocol("WM_DELETE_WINDOW", self.master.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginUI(root)
    root.mainloop()
