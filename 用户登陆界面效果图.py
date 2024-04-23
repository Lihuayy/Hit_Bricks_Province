import tkinter as tk


class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("弹出新高度")
        master.geometry("800x600")

        # 尝试加载背景图片
        self.background = tk.PhotoImage(file="background.png")

        # 创建Canvas作为背景，并填充整个窗口
        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 如果图片加载成功，将其画在Canvas上，覆盖整个Canvas
        if self.background:
            self.canvas.create_image(0, 0, anchor="nw", image=self.background)

        # 在Canvas上直接添加组件
        self.label = tk.Label(self.canvas, text="启程砖块乐园", font=("Arial", 16), bg="white")
        self.canvas.create_window(400, 100, window=self.label)  # 将标签放在Canvas的指定位置

        # 创建账号输入框
        self.username_label = tk.Label(self.canvas, text="账号:", bg="white")
        self.canvas.create_window(300, 200, window=self.username_label)
        self.username_entry = tk.Entry(self.canvas, font=("Arial", 12), borderwidth=2, bg="white")
        self.canvas.create_window(400, 200, window=self.username_entry)

        # 创建密码输入框
        self.password_label = tk.Label(self.canvas, text="密码:", bg="white")
        self.canvas.create_window(300, 250, window=self.password_label)
        self.password_entry = tk.Entry(self.canvas, font=("Arial", 12), borderwidth=2, bg="white", show="*")
        self.canvas.create_window(400, 250, window=self.password_entry)

        # 创建登录按钮
        self.login_button = tk.Button(self.canvas, text="登录", command=self.login, bg="white")
        self.canvas.create_window(300, 300, window=self.login_button)

        # 创建退出按钮
        self.quit_button = tk.Button(self.canvas, text="退出", command=self.master.quit, bg="white")
        self.canvas.create_window(400, 300, window=self.quit_button)

    def login(self):
        # 登录逻辑
        print("登录按钮被按下，账号：", self.username_entry.get())
        print("密码：", self.password_entry.get())


# 创建主窗口
root = tk.Tk()

# 创建登录窗口实例
login_window = LoginWindow(root)

# 运行主循环
root.mainloop()
