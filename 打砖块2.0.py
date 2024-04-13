import pygame
import random
import time

# 游戏初始化
pygame.init()
pygame.font.init()
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
high_score = 10000

# 假设所有砖块的宽度和高度均为固定值
BRICK_WIDTH = 50
BRICK_HEIGHT = 20

# 用颜色名称创建一个颜色映射
color_map = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0)
}

# 更新关卡布局，包括宽度和高度
level_1_layout = [
    [(50, 50, BRICK_WIDTH, BRICK_HEIGHT, color_map['red']), (150, 50, BRICK_WIDTH, BRICK_HEIGHT, color_map['green']), (250, 50, BRICK_WIDTH, BRICK_HEIGHT, color_map['blue']), None, (450, 50, BRICK_WIDTH, BRICK_HEIGHT, color_map['yellow'])],
    [(50, 100, BRICK_WIDTH, BRICK_HEIGHT, color_map['blue']), None, (250, 100, BRICK_WIDTH, BRICK_HEIGHT, color_map['red']), (350, 100, BRICK_WIDTH, BRICK_HEIGHT, color_map['green']), (450, 100, BRICK_WIDTH, BRICK_HEIGHT, color_map['red'])],
    # 更多行
]

# Level 类和 create_bricks 方法保持不变
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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def reset_position(self, screen_height):
        # 假设我们想要将挡板重置到屏幕中央的垂直位置
        self.rect.centery = screen_height // 2
        # 你可能还需要重置其他属性，比如速度等
    def set_width(self, new_width):
        self.width = new_width
        self.rect.width = new_width

    def update(self, screen_height, keys):
        # 如果按下向上的键，且挡板顶部没有超出屏幕顶端，则向上移动
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        # 如果按下向下的键，且挡板底部没有超出屏幕底端，则向下移动
        if keys[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.y += self.speed
    # 实例化球拍对象


paddle = Paddle(x=width // 2, y=height - 30, w=200, h=10, color=BLUE)


new_width = 500
paddle.set_width(new_width)


class Brick:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
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
    def __init__(self, x, y, radius, color, speed_x, speed_y):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self, screen_width, screen_height):
        # 移动球
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 检查左右边缘碰撞并反弹
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.speed_x *= -1
            # 确保球不会卡在屏幕边缘
            self.rect.x = max(self.rect.x, 0)
            self.rect.x = min(self.rect.x, screen_width - self.rect.width)

        # 检查上边缘碰撞并反弹
        if self.rect.top <= 0:
            self.speed_y *= -1
            # 确保球不会卡在屏幕边缘
            self.rect.y = max(self.rect.y, 0)

        def reset_position(self):
            # 重置球的位置和速度到初始状态
            self.rect.x = self.initial_x
            self.rect.y = self.initial_y
            self.speed_x = self.initial_speed_x
            self.speed_y = self.initial_speed_y

        # 球拍碰撞检测
        if self.rect.colliderect(paddle.rect):
            self.speed_y = -self.speed_y

        # 砖块碰撞检测
        for brick in bricks:
            if brick.alive and self.rect.colliderect(brick.rect):
                brick.hit()
                self.speed_y = -self.speed_y
                break  # 只处理一个碰撞，防止同时撞击多个砖块

    def reset_position(self, screen_width, screen_height, speed_x, speed_y):
        # 将球的位置重置到屏幕中心
        self.rect.centerx = screen_width // 2
        self.rect.centery = screen_height // 2
        # 重置球的速度
        self.speed_x = speed_x
        self.speed_y = speed_y
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)

    def update(self, screen_width, screen_height, player):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.y <= 0 or self.y >= screen_height:
            self.speed_y *= -1

        if self.y >= screen_height:
            # 如果球碰到底部边界，则减少生命值并重置球的位置
            player.lives -= 1
            self.reset_position(screen_width, screen_height)

    def reset_position(self, screen_width, screen_height):
        self.x = screen_width // 2
        self.y = screen_height // 2

    def bounce_on_paddle(self):
        # 当球碰到球拍时调用此方法来反转水平速度
        self.speed_x *= -1

    # 实例化球对象


initial_speed_x = 5  # 设置球在 x 方向的初始速度
initial_speed_y = -5  # 设置球在 y 方向的初始速度（负值表示向上）

ball = Ball(x=width // 2, y=height // 2, radius=8, color=RED, speed_x=initial_speed_x, speed_y=initial_speed_y)


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
ball_speed = 5  # 假设这是你想要的速度值
#ball = Ball(x=width // 2, y=paddle.y - 10, radius=8, color=RED, speed_x=ball_speed, speed_y=-ball_speed)
#bricks = [Brick(x=i*(brick_width+padding), y=100, w=brick_width, h=brick_height, color=RED) for i in range(brick_cols)]
power_ups = [PowerUp(x=100, y=200, w=20, h=10, color=GREEN, effect="extra_life")]


class Level:
    def __init__(self, bricks_layout):
        self.bricks = self.create_bricks(bricks_layout)

    def create_bricks(self, layout):
        bricks = []
        for row in layout:
            for brick_data in row:
                if brick_data:  # 如果 brick_data 不是 None 或 False
                    brick = Brick(*brick_data)
                    bricks.append(brick)
        return bricks

    def draw(self, surface):
        for brick in self.bricks:
            if brick.alive:
                brick.draw(surface)

    def is_completed(self):
        return all(not brick.alive for brick in self.bricks)

class Player:
    def __init__(self, lives):
        self.lives = lives
        self.score = 0

    def lose_life(self):
        self.lives -= 1

    def is_alive(self):
        return self.lives > 0

    def draw_lives(self, surface, font, lives):
        text = f"Lives: {lives}"
        text_surface = font.render(text, True, (255, 80, 255))  # 白色文本
        surface.blit(text_surface, (10, 10))  # 绘制在屏幕左上角

class Leaderboard:
    def __init__(self):
        self.high_score = 0  # 初始化最高分为 0 或从文件/数据库读取


    def load_scores(self):
        # 这里可以从文件中加载分数
        try:
            with open('scores.txt', 'r') as f:
                scores = [int(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            scores = []
        return scores

    def save_scores(self):
        with open('scores.txt', 'w') as f:
            for score in self.scores:
                f.write(f"{score}\n")

    def add_score(self, score):
        self.scores.append(score)
        self.scores.sort(reverse=True)
        self.scores = self.scores[:10]  # 保留前10个最高分
        self.save_scores()

    def draw(self, surface, font):
        text = f"High Score: {self.high_score}"
        text_surface = font.render(text, True, (255, 56, 0))  # 白色文本
        surface.blit(text_surface, (surface.get_width() - text_surface.get_width() - 10, 10))  # 绘制在屏幕右上角

    def update_high_score(self, new_score):
        # 如果有新的高分，更新它
        if new_score > self.high_score:
            self.high_score = new_score
        # 可以在此处添加代码将最高分保存到文件或数据库

class PowerUp:
    def __init__(self, x, y, effect):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.effect = effect

    def apply(self, paddle, ball):
        # 在这里根据 effect 类型来修改 paddle 或 ball 的状态
        if self.effect == 'expand_paddle':
            paddle.rect.inflate_ip(20, 0)
        elif self.effect == 'shrink_paddle':
            paddle.rect.inflate_ip(-20, 0)
        elif self.effect == 'speed_up_ball':
            ball.speed_x *= 1.2
            ball.speed_y *= 1.2
        # 其他效果...

    def draw(self, surface):
        # 绘制道具的代码
        pygame.draw.ellipse(surface, (255, 0, 0), self.rect)


# 初始化玩家、关卡、排行榜和道具
player = Player(lives=3)
current_level = Level(level_1_layout)
leaderboard = Leaderboard()
powerups = []  # 暂时为空列表

screen_width = screen.get_width()
screen_height = screen.get_height()
ball = Ball(screen_width // 2, screen_height // 2, 10, (255, 255, 255), 5, 5)
font = pygame.font.SysFont("Arial", 30)

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
                current_level = Level(level_1_layout)  # 重置关卡
                power_ups = []  # 清空道具列表
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

        # 更新球拍的位置...
    paddle.update(screen.get_height(), keys)

    # 更新球的位置
    #ball.update()

    # 检测球和球拍之间的碰撞
    if ball.rect.colliderect(paddle.rect):
        ball.bounce_on_paddle()

    if not paused:
        paddle.set_width(500)
        # 移动球
        ball.move(screen_width, screen_height)
        # 球和砖块的碰撞
        for brick in current_level.bricks:
            if ball.rect.colliderect(brick.rect) and brick.alive:
                brick.alive = False
                player.score += 10
                # 反弹球的逻辑
                if abs(ball.rect.bottom - brick.rect.top) < 10 and ball.speed_y > 0:
                    ball.speed_y *= -1
                elif abs(ball.rect.top - brick.rect.bottom) < 10 and ball.speed_y < 0:
                    ball.speed_y *= -1
                elif abs(ball.rect.right - brick.rect.left) < 10 and ball.speed_x > 0:
                    ball.speed_x *= -1
                elif abs(ball.rect.left - brick.rect.right) < 10 and ball.speed_x < 0:
                    ball.speed_x *= -1
                break

        # 球和球拍的碰撞
        if ball.rect.colliderect(paddle.rect):
            # 球反弹
            ball.speed_y *= -1

        # 球和屏幕边界的碰撞
        if ball.rect.left <= 0 or ball.rect.right >= screen.get_width():
            ball.speed_x *= -1
        if ball.rect.top <= 0:
            ball.speed_y *= -1
        if ball.rect.bottom >= screen.get_height():
            player.lives -= 1
            if player.lives == 0:
                running = False
            #else:
                # 重置球和球拍位置
                #ball.reset_position(screen.get_width(), screen.get_height(), initial_speed_x, initial_speed_y)
               
        # 球和屏幕边界的碰撞
        if ball.rect.left <= 0:
            ball.rect.left = 0  # 防止球飞出左边缘
            ball.speed_x *= -1
        elif ball.rect.right >= screen.get_width():
            ball.rect.right = screen.get_width()  # 防止球飞出右边缘
            ball.speed_x *= -1

        if ball.rect.top <= 0:
            ball.rect.top = 0  # 防止球飞出上边缘
            ball.speed_y *= -1
        elif ball.rect.bottom >= screen.get_height():
            # 球飞出屏幕底部的处理
            player.lives -= 1
            if player.lives == 0:
                running = False  # 如果没有生命值，则游戏结束
            #else:
                # 重置球和球拍位置
                #ball.reset_position(screen.get_width(), screen.get_height(), initial_speed_x, initial_speed_y)  # 假设这是一个将球置于初始位置的方法


        # 渲染所有对象
        screen.fill(WHITE)
        current_level.draw(screen)  # 绘制关卡砖块
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        for power_up in power_ups:
            power_up.draw(screen)

            # 清屏
        #screen.fill((0, 0, 0))
        # 绘制生命值和排行榜
        player.draw_lives(screen, font, player.lives)  # 显示生命值，假设 player 对象有一个 lives 属性
        leaderboard.draw(screen, font)  # 不再需要传递 high_score，因为它是类的属性
        # 更新球的位置
        ball.update(screen_width, screen_height, player)


        pygame.display.flip()
    else:
        # 游戏暂停
        # 显示暂停菜单（如果有的话）
        pass

    # 控制游戏刷新率
    pygame.time.Clock().tick(60)

# 退出游戏
pygame.quit()