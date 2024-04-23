import tkinter as tk
from PIL import Image, ImageTk

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("弹出新高度")
        master.geometry("800x600")

        # 设置宋体字体和16号字号
        self.font_style = ("SimSun", 16)

        # 尝试加载背景图片
        self.original_image = self.load_image("background.png")
        self.background = ImageTk.PhotoImage(self.original_image)

        # 创建Canvas作为背景，并填充整个窗口
        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 绑定窗口大小变化事件
        master.bind("<Configure>", self.resize_background)

        # 将背景图片绘制到Canvas上
        self.update_background()

        # 在Canvas上添加组件
        self.add_widgets()

    def load_image(self, path):
        # 使用PIL加载图片
        try:
            return Image.open(path)
        except IOError as e:
            print("图片加载失败: ", e)
            return None

    def update_background(self):
        # 清除Canvas上的所有元素
        self.canvas.delete("all")

        # 根据窗口大小调整图片大小
        if self.original_image:
            self.resize_background(None)

        # 重新绘制背景图片
        if self.background:
            self.canvas.create_image(0, 0, anchor="nw", image=self.background)

        # 重新添加组件
        self.add_widgets()

    def resize_background(self, event):
        if not self.original_image:
            return

        # 获取窗口的宽度和高度
        width = self.master.winfo_width()
        height = self.master.winfo_height()

        # 确保窗口尺寸大于0
        if width <= 0 or height <= 0:
            return

        # 计算缩放比例
        scale_width = width / self.original_image.width
        scale_height = height / self.original_image.height

        # 使用较小的缩放比例以保持图片的宽高比
        scale = min(scale_width, scale_height)

        # 计算新的图片尺寸
        new_width = int(self.original_image.width * scale)
        new_height = int(self.original_image.height * scale)

        # 确保新的尺寸大于0
        if new_width > 0 and new_height > 0:
            # 调整图片大小，使用ANTIALIAS作为抗锯齿选项
            resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 更新背景图片
            self.background = ImageTk.PhotoImage(resized_image)
            self.canvas.config(width=width, height=height)
            self.canvas.create_image(0, 0, anchor="nw", image=self.background)
        else:
            print("无法调整图片大小，因为新尺寸不大于0。")

    def add_widgets(self):
        # 将组件放置在Canvas中心
        canvas_width = self.master.winfo_width()
        canvas_height = self.master.winfo_height()
        label_x = canvas_width // 2 - 100  # 根据实际情况调整偏移量
        entry_x = label_x + 100  # 根据实际情况调整偏移量

        # 添加账号标签和输入框
        self.username_label = tk.Label(self.canvas, text="账号:", font=self.font_style, bg="white")
        self.canvas.create_window(label_x, canvas_height // 2 - 100, window=self.username_label)
        self.username_entry = tk.Entry(self.canvas, font=self.font_style, bg="lightgray", borderwidth=2)
        self.canvas.create_window(entry_x, canvas_height // 2 - 100, window=self.username_entry)

        # 添加密码标签和输入框
        self.password_label = tk.Label(self.canvas, text="密码:", font=self.font_style, bg="white")
        self.canvas.create_window(label_x, canvas_height // 2 - 40, window=self.password_label)
        self.password_entry = tk.Entry(self.canvas, font=self.font_style, bg="lightgray", borderwidth=2, show="*")
        self.canvas.create_window(entry_x, canvas_height // 2 - 40, window=self.password_entry)

        # 调整登录和退出按钮的位置
        self.login_button = tk.Button(self.canvas, text="登录", command=self.login, font=self.font_style, bg="white")
        self.canvas.create_window(canvas_width // 2 - 50, canvas_height // 2 + 40, window=self.login_button)

        self.quit_button = tk.Button(self.canvas, text="退出", command=self.master.quit, font=self.font_style, bg="white")
        self.canvas.create_window(canvas_width // 2 + 50, canvas_height // 2 + 40, window=self.quit_button)

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