# ui/register_ui.py
import tkinter as tk
from tkinter import messagebox
from ..controllers.auth_controller import AuthController
from ..utils.api_client import APIClient


class RegisterUI:
    def __init__(self, master):
        self.master = master
        self.master.title("注册")
        self.master.geometry("300x250")

        # 初始化APIClient和AuthController
        api_client = APIClient()
        self.auth_controller = AuthController(api_client)

        # 创建GUI组件
        self.create_widgets()

    def create_widgets(self):
        # 名字标签和输入框
        tk.Label(self.master, text="名字").pack(pady=5)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.pack(pady=5)

        # 邮箱标签和输入框
        tk.Label(self.master, text="邮箱").pack(pady=5)
        self.email_entry = tk.Entry(self.master)
        self.email_entry.pack(pady=5)

        # 密码标签和输入框
        tk.Label(self.master, text="密码").pack(pady=5)
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack(pady=5)

        # 注册按钮
        tk.Button(self.master, text="注册", command=self.register).pack(pady=20)

        # 返回登录按钮
        tk.Button(self.master, text="返回登录", command=self.go_back).pack()

    def register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not name or not email or not password:
            messagebox.showwarning("警告", "请填写所有字段")
            return

        success, message = self.auth_controller.register(email, password, name)
        if success:
            messagebox.showinfo("成功", message)
            self.master.destroy()
            import login_ui
            login_ui.LoginUI(tk.Tk())
        else:
            messagebox.showerror("错误", message)

    def go_back(self):
        self.master.destroy()
        import login_ui
        login_ui.LoginUI(tk.Tk())


if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterUI(root)
    root.mainloop()
