import tkinter as tk
from tkinter import messagebox
from ..controllers.parkingController import ParkingController
from ..models.users import User

class DashboardUI:
    def __init__(self, master, user, api_client):
        """
        Initializes the dashboard UI.

        Parameters:
        - master (tk.Tk or tk.Toplevel): The parent window.
        - user (User): The currently logged-in user.
        - api_client (APIClient): The API client for backend interactions.
        """
        self.master = master
        self.master.title("停车仪表盘")
        self.master.geometry("600x400")

        self.user = user
        self.parking_controller = ParkingController(api_client)

        # 初始化界面
        self.create_widgets()

    def create_widgets(self):
        # 欢迎标签
        tk.Label(self.master, text=f"欢迎, {self.user.name}", font=("Arial", 14)).pack(pady=10)

        # 停车位列表框
        self.parking_listbox = tk.Listbox(self.master, width=80, height=15)
        self.parking_listbox.pack(pady=10)

        # 获取停车位按钮
        tk.Button(self.master, text="刷新停车位", command=self.fetch_parking_spaces).pack(pady=5)

        # 预订按钮
        tk.Button(self.master, text="预订选中停车位", command=self.book_selected_space).pack(pady=5)

        # 退出按钮
        tk.Button(self.master, text="退出", command=self.master.quit).pack(pady=20)

    def fetch_parking_spaces(self):
        """
        Fetches available parking spaces from the backend and updates the listbox.
        """
        try:
            parking_spaces = self.parking_controller.get_available_spaces()
            self.parking_listbox.delete(0, tk.END)  # 清空列表框

            if not parking_spaces:
                messagebox.showinfo("信息", "目前没有可用的停车位。")
                return

            for space in parking_spaces:
                self.parking_listbox.insert(tk.END, f"ID: {space['id']} - 位置: {space['location']} - 状态: {space['status']}")

        except Exception as e:
            messagebox.showerror("错误", f"获取停车位时出错: {str(e)}")

    def book_selected_space(self):
        """
        Books the parking space selected in the listbox.
        """
        try:
            # 获取选中的停车位信息
            selected = self.parking_listbox.curselection()
            if not selected:
                messagebox.showwarning("警告", "请先选择一个停车位。")
                return

            selected_text = self.parking_listbox.get(selected[0])
            parking_id = selected_text.split(" ")[1].replace("ID:", "")

            # 预订停车位
            result = self.parking_controller.book_space(parking_id, self.user)

            if result:
                messagebox.showinfo("成功", f"停车位 {parking_id} 预订成功！")
                self.fetch_parking_spaces()  # 刷新停车位列表
            else:
                messagebox.showwarning("失败", f"停车位 {parking_id} 预订失败，请重试。")
        except Exception as e:
            messagebox.showerror("错误", f"预订停车位时出错: {str(e)}")


if __name__ == "__main__":
    from utils.api_client import APIClient
    from models.user import User

    # 创建测试窗口
    root = tk.Tk()
    api_client = APIClient()

    # 假设当前用户登录成功
    mock_user = User(user_id=1, name="测试用户", email="test@example.com", is_verified=True)

    app = DashboardUI(root, mock_user, api_client)
    root.mainloop()
