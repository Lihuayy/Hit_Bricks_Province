import tkinter as tk

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("弹出新高度")
        master.geometry("800x600")  # 设置窗口大小为800x600

        # 创建一个标签显示消息
        self.label = tk.Label(master, text="启程砖块乐园", font=("Arial", 16))
        self.label.pack(pady=20)  # 垂直间距调整为20

        # 创建账号输入框
        self.username_label = tk.Label(master, text="账号:")
        self.username_label.pack()
        self.username_entry = tk.Entry(master, font=("Arial", 12), borderwidth=2)
        self.username_entry.pack(pady=10)  # 垂直间距调整为10

        # 创建密码输入框
        self.password_label = tk.Label(master, text="密码:")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, font=("Arial", 12), borderwidth=2, show="*")
        self.password_entry.pack(pady=10)  # 垂直间距调整为10

        # 创建一个空的frame用于放置登录和退出按钮
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=20)  # 垂直间距调整为20

        # 创建登录按钮并添加到frame中
        self.login_button = tk.Button(self.button_frame, text="登录", command=self.login)
        self.login_button.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)  # 左右间距和内边距

        # 创建退出按钮并添加到frame中
        self.quit_button = tk.Button(self.button_frame, text="退出", command=master.quit)
        self.quit_button.pack(side=tk.LEFT)  # 与登录按钮水平排列

    def login(self):
        # 这里可以添加登录验证逻辑
        print("登录按钮被按下，账号：", self.username_entry.get())
        print("密码：", self.password_entry.get())

# 创建主窗口
root = tk.Tk()

# 创建登录窗口实例
login_window = LoginWindow(root)

# 运行主循环
root.mainloop()