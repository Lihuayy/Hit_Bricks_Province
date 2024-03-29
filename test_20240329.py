"""
class Student:
    grdae='大一'
    def __init__(self, sname, sage):
        self.name = sname
        self.age = sage
    def print_info(self):
        print(f"我的名字{self.name},我的年龄是{self.age}")
student_01 = Student('Nike',19)
student_01.print_info()
student_02 = Student('Tom',18)
student_02.print_info()
"""
"""
class Student:
    grdae='大一'
    def __init__(self, sname, sage):
        self.name = sname
        self.age = sage
    def __str__(self):
        return "我的姓名:{}--我的年龄:{}".format(self.name,self.age)
    def __lt__(self,age):
        print("__lt__")
        if self.age <
student_01 = Student('Nike',19)
student_02 = Student('Tom',18)
print(student_01)
print(student_02)
"""

"""
class Student:
    grade = '大一'  

    def __init__(self, sname, sage):
        self.name = sname
        self.age = sage

    def __str__(self):
        return "我的姓名:{}--我的年龄:{}".format(self.name, self.age)

    def __lt__(self, other):  # 另一个Student对象作为参数
        print("__lt__方法被调用")
        return self.age < other.age  # 比较当前对象的年龄与另一个对象的年龄


student_01 = Student('Nike', 20)
student_02 = Student('Tom', 18)

print(student_01)  # 输出student_01的字符串表示
print(student_02)  # 输出student_02的字符串表示

# 使用__lt__方法比较两个学生的年龄
if student_01 < student_02:
    print("student_01的年龄小于student_02的年龄")
else:
    print("student_01的年龄大于student_02的年龄")
"""
"""
class Student:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __str__(self):
        return f"Student(name: {self.name}, age: {self.age})"
    def __lt__(self,other):
        return self.age < other.age
    def __le__(self, other):
        return self.age <= other.age
    def __eq__(self, other):
        return self.age == other.age
    def __del__(self):
        print('对象被销毁')
#使用str方法表示
student1 = Student('Ben',18)
student2 = Student('lily',20)
print(student1)
student2 = Student('Lily',20)
student3 = Student('Lily',19)
print(student2)
#比较学生年龄大小-le方法
print(student1 < student2)
print(student1 > student2)
#eq方法比较
print(student1 <= student2)
print(student1 >= student2)
print(student1 == student2)

print(student1 == student3)
#销毁对象
del student1
print(student1)
"""

"""
class Student:
    grade = '大一'

    def __init__(self, sname, sage):
        self.name = sname
        self.age = sage

    def __str__(self):
        return "我的姓名:{}--我的年龄:{}".format(self.name, self.age)

    def __lt__(self, other):
        return self.age < other.age

    def __le__(self, other):
        return self.age <= other.age

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.name == other.name and self.age == other.age
        return False

    def __del__(self):
        print(f"学生 {self.name} 的对象被销毁了")

    # 创建学生对象


student_01 = Student('Nike', 19)
student_02 = Student('Tom', 18)

# 输出学生信息
print(student_01)
print(student_02)

# 使用__lt__和__le__方法比较学生年龄
print(student_01 < student_02)  # 使用__lt__方法
print(student_01 <= student_02)  # 使用__le__方法

# 使用__eq__方法比较两个学生对象是否相等
print(student_01 == student_02)  # 使用__eq__方法

# 当对象不再被引用时，__del__方法会被调用
# 此为演示，我们手动将对象引用设为None
student_01 = None
student_02 = None

# 强制销毁对象
import gc

gc.collect()
"""



#调料部分使用AI修正，并增加错误纠正
class RoastedSweetPotato:
    def __init__(self, weight):
        self.weight = weight  # 红薯的重量
        self.cooking_status = '生的'  # 烤制状态：生的、半生不熟、熟了
        self.seasonings = []  # 已加的调料列表

    def start_roasting(self, cooking_time=None):
        if cooking_time is None:
            cooking_time = int(input("请输入烤制时间（分钟）："))
        print(f"开始烤制{self.weight}克的红薯，预计需要{cooking_time}分钟。")
        # 烤制过程的不同阶段
        for minute in range(cooking_time):
            if minute < cooking_time // 3:
                self.cooking_status = '生的'
            elif minute < cooking_time * 2 // 3:
                self.cooking_status = '半生不熟'
            else:
                self.cooking_status = '熟了'
                break
        print("烤制结束，红薯现在是{}的。".format(self.cooking_status))

    def add_seasoning(self):
        if self.cooking_status == '熟了':
            seasonings = ["蜂蜜", "黄油", "芝士", "烧烤酱", "盐", "胡椒粉"]
            print("可选以下调料：")
            for i, seasoning in enumerate(seasonings):
                print(f"{i + 1}. {seasoning}")
            selected_seasonings = input("请输入要添加的调料编号（用逗号分隔，或直接输入'全部'以添加所有调料）：").strip()
            if selected_seasonings.lower() == '全部':
                self.seasonings.extend(seasonings)
            else:
                try:
                    selected_seasonings = [int(s) - 1 for s in selected_seasonings.split(',')]
                    valid_seasonings = [seasonings[i] for i in selected_seasonings if 0 <= i < len(seasonings)]
                    self.seasonings.extend(valid_seasonings)
                except (ValueError, IndexError):
                    print("无效的调料编号，请重新输入。")
            if self.seasonings:
                print(f"为烤熟的红薯添加了调料：{', '.join(self.seasonings)}。")
        else:
            print("红薯还没烤熟，不要加调料！！")

    def __str__(self):
        status = self.cooking_status
        if self.seasonings:
            status += "，已加调料：{}".format(', '.join(self.seasonings))
        return f"一个{status}的红薯，重量为{self.weight}克。"

weight = int(input("请输入红薯的重量（克）："))
sweet_potato = RoastedSweetPotato(weight)

# 红薯的初始状态
print(sweet_potato)

# 开始烤制红薯
sweet_potato.start_roasting()

# 再次打印红薯的状态
print(sweet_potato)

# 加调料
sweet_potato.add_seasoning()

# 加调料后的红薯状态
print(sweet_potato)


"""""
class RoastedSweetPotato:
    def __init__(self, weight):
        self.weight = weight  # 红薯的重量
        self.cooking_status = '生的'  # 烤制状态：生的、半生不熟、熟了
        self.seasonings = []  # 已加的调料列表

    def start_roasting(self, cooking_time=None):
        if cooking_time is None:
            cooking_time = int(input("请输入烤制时间（分钟）："))
        print(f"开始烤制重量为{self.weight}克的红薯，预计需要{cooking_time}分钟。")
        # 模拟烤制过程的不同阶段和进度显示
        for minute in range(cooking_time + 1):  # +1 是为了确保最后一次进度也能被打印出来
            progress = (minute / cooking_time) * 100  # 计算进度百分比
            if minute < cooking_time // 3:
                self.cooking_status = '生的'
            elif minute < cooking_time * 2 // 3:
                self.cooking_status = '半生不熟'
            else:
                self.cooking_status = '熟了'
                # 显示烤制进度
            print(f"烤制进度：{progress:.2f}%，红薯现在是{self.cooking_status}的。")
            # 休眠一段时间以模拟烤制过程（可选）
            # time.sleep(1)
        print("烤制结束，红薯现在是{}的。".format(self.cooking_status))

    def add_seasoning(self):
        if self.cooking_status == '熟了':
            seasonings = ["蜂蜜", "黄油", "芝士", "肉桂粉", "盐", "胡椒粉"]
            print("以下调料可供选择：")
            for i, seasoning in enumerate(seasonings):
                print(f"{i + 1}. {seasoning}")
            selected_seasonings = input("请输入要添加的调料编号（用逗号分隔，或直接输入'全部'以添加所有调料）：").strip()
            if selected_seasonings.lower() == '全部':
                self.seasonings.extend(seasonings)
            else:
                try:
                    selected_seasonings = [int(s) - 1 for s in selected_seasonings.split(',')]
                    valid_seasonings = [seasonings[i] for i in selected_seasonings if 0 <= i < len(seasonings)]
                    self.seasonings.extend(valid_seasonings)
                except (ValueError, IndexError):
                    print("无效的调料编号，请重新输入。")
            if self.seasonings:
                print(f"为烤熟的红薯添加了调料：{', '.join(self.seasonings)}。")
        else:
            print("红薯还没烤熟，不能加调料！")

    def __str__(self):
        status = self.cooking_status
        if self.seasonings:
            status += "，已加调料：{}".format(', '.join(self.seasonings))
        return f"一个{status}的红薯，重量为{self.weight}克。"

    # 创建烤红薯对象，允许用户自定义重量


weight = int(input("请输入红薯的重量（克）："))
sweet_potato = RoastedSweetPotato(weight)

# 打印红薯的初始状态
print(sweet_potato)

# 开始烤制红薯
sweet_potato.start_roasting()

# 为红薯加调料（如果红薯已经熟了）
if sweet_potato.cooking_status == '熟了':
    sweet_potato.add_seasoning()

# 打印加调料后的红薯状态
print(sweet_potato)
"""""