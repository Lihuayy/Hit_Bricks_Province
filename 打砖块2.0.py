import pygame
import random
import time

# 游戏初始化
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('打砖块游戏')

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 游戏变量
lives = 3
score = 0
level = 1

# 排行榜模拟数据
leaderboard = []

# 游戏循环控制变量
running = True
paused = False

# 游戏对象类定义（这里只是示例，需要你根据游戏需要来完善）
class Paddle:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = color
        self.speed = 7
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        if direction == 'left':
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        elif direction == 'right':
            self.x += self.speed
            if self.x > width - self.width:
                self.x = width - self.width
        self.rect.x = self.x

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    # 实例化球拍对象


paddle = Paddle(x=width // 2, y=height - 30, w=100, h=10, color=BLUE)

class Brick:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.alive = True

    def hit(self):
        # 当砖块被球撞击时调用此函数
        self.alive = False

    def draw(self, surface):
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)


def create_bricks(rows, cols, brick_width, brick_height):
    bricks = []
    padding = 5
    offset_x = (width - (cols * (brick_width + padding))) // 2
    offset_y = 50  # 距离屏幕顶部的偏移
    for row in range(rows):
        for col in range(cols):
            x = offset_x + col * (brick_width + padding)
            y = offset_y + row * (brick_height + padding)
            color = random.choice([RED, GREEN, BLUE])  # 随机选择颜色
            brick = Brick(x, y, brick_width, brick_height, color)
            bricks.append(brick)
    return bricks

    # 初始化砖块


brick_rows = 5
brick_cols = 10
brick_width = 70
brick_height = 20
bricks = create_bricks(brick_rows, brick_cols, brick_width, brick_height)

class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed
        self.speed_y = -speed
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

        # 撞墙检测
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.speed_x = -self.speed_x
        if self.y - self.radius <= 0:
            self.speed_y = -self.speed_y

        # 球拍碰撞检测
        if self.rect.colliderect(paddle.rect):
            self.speed_y = -self.speed_y

        # 砖块碰撞检测
        for brick in bricks:
            if brick.alive and self.rect.colliderect(brick.rect):
                brick.hit()
                self.speed_y = -self.speed_y
                break  # 只处理一个碰撞，防止同时撞击多个砖块

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    # 实例化球对象


ball = Ball(x=width // 2, y=height // 2, radius=8, color=RED, speed=5)


class PowerUp:
    def __init__(self, x, y, w, h, color,effect):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = color
        self.effect = effect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.falling = False

    def start_falling(self):
        self.falling = True

    def move(self):
        if self.falling:
            self.y += 2  # 道具下落速度
            self.rect.y = self.y

    def activate(self):
        if self.effect == "extra_life":
            global lives
            lives += 1
        self.falling = False  # 道具激活后停止下落

    def draw(self, surface):
        if self.falling:
            pygame.draw.rect(surface, self.color, self.rect)

    # 在适当的时候，例如砖块被击中时，可以随机生成道具


def generate_power_up(brick):
    effect = random.choice(["extra_life"])  # 随机选择一个效果
    power_up = PowerUp(brick.x + brick.width // 2, brick.y, 20, 10, GREEN, effect)
    power_up.start_falling()
    return power_up

# 游戏对象实例化（这里只是示例）
paddle = Paddle(x=width // 2 - 50, y=height - 20, w=100, h=10, color=BLUE)
ball = ball = Ball(x=width // 2, y=paddle.y - 10, radius=8, color=RED, speed=5)
#bricks = [Brick(x=i*(brick_width+padding), y=100, w=brick_width, h=brick_height, color=RED) for i in range(brick_cols)]
power_ups = [PowerUp(x=100, y=200, w=20, h=10, color=GREEN, effect="extra_life")]

# 游戏主循环
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_r:
                # 重置游戏变量来重新开始
                lives = 3
                score = 0
                level = 1
                # 需要添加重置游戏对象的代码
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move('left')
    if keys[pygame.K_RIGHT]:
        paddle.move('right')
        # 处理道具
    for power_up in power_ups:
        power_up.move()
        if power_up.falling and power_up.rect.colliderect(paddle.rect):
            power_up.activate()
            power_ups.remove(power_up)  # 激活后移除道具

    if not paused:
        # 更新游戏对象状态
        #paddle.update()
        #ball.update()

        # 移动球
        ball.move()
        # 碰撞检测和处理
        # ...

        # 渲染所有对象
        screen.fill(WHITE)
        paddle.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        for power_up in power_ups:
            power_up.draw(screen)
        ball.draw(screen)
        # for brick in bricks:
        #     brick.draw(screen)
        # for power_up in power_ups:
        #     power_up.draw(screen)

        # 显示得分和生命值
        # ...

        pygame.display.flip()
    else:
        # 游戏暂停
        # 显示暂停菜单（如果有的话）
        pass

    # 控制游戏刷新率
    pygame.time.Clock().tick(60)

# 退出游戏
pygame.quit()