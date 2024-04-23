import pygame
import sys
import time
import random
from pygame import image  # 添加导入语句

# 游戏对象定义
class Game:
    def __init__(self, screen, font):
        self.leaderboard = None
        pygame.init()
        self.size = self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("打砖块游戏")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.levels = [Level(difficulty=i) for i in range(1, 4)]
        self.current_level_index = 0
        self.lives = 3
        self.start_time = None
        self.elapsed_time = 0
        self.ui = UserInterface(screen)
        self.font = font
        self.running = True
        self.paused = False
        self.lives = 3  # 初始化生命值为3
        self.start_time = time.time()
        self.elapsed_time = 0
        self.leaderboard = Leaderboard(screen, font)
        self.ui = UserInterface(screen)
        self.bricks = pygame.sprite.Group()
        self.paddle = Paddle(320, 460)
        self.ball = Ball(320, 300)
        self.powerups = pygame.sprite.Group()  # 用于存储屏幕上的道具
        self.all_sprites = pygame.sprite.Group(self.paddle, self.ball)  # 所有精灵的组
        # 创建砖块
        for i in range(5):  # 5行砖块
            for j in range(9):  # 每行9个砖块
                brick = Brick(j * 64 + 32, i * 24 + 32)
                self.bricks.add(brick)
                self.all_sprites.add(brick)
        self.state = 'start'  # 游戏状态：'start', 'running', 'paused', 'game over'
        self.start_text = '按任意键开始游戏'
        self.pause_text = '游戏暂停，按P继续'
        self.game_over_text = '游戏结束，按R重新开始'
        self.keys_pressed = None  # 用于存储当前按下的键

        # 移动方法定义至此处
        def start_game(self):
            self.state = 'running'
            self.reset_game()

        def pause_game(self):
            if self.state == 'running':
                self.state = 'paused'
                self.show_text(self.pause_text, self.screen.get_width() // 2, self.screen.get_height() // 2)

        def unpause_game(self):
            if self.state == 'paused':
                self.state = 'running'

        def reset_game(self):
            # 重置游戏状态，生命值和关卡等
            self.lives = 3
            self.all_sprites.empty()
            self.bricks.empty()
            self.powerups.empty()
            self.create_objects()
            self.start_time = time.time()
            self.paused = False


        def generate_powerup(self, x, y):
            # 随机生成道具
            if random.randint(1, 100) <= 10:  # 有10%的几率生成道具
                powerup = PowerUp(x, y, "clear_bricks")
                self.powerups.add(powerup)

        def activate_powerup(self, powerup):
            # 激活道具
            if powerup.powerup_type == "clear_bricks":
                # 假设有一个self.bricks的Group存储所有砖块
                for brick in self.bricks:
                    brick.kill()  # 移除所有砖块
                self.show_text("清空所有砖块！", self.screen.get_width() // 2, self.screen.get_height() // 2)

    def lose_life(self):
        self.lives -= 1
        if self.lives > 0:
            self.show_text(f"你失去了一条生命，还剩 {self.lives} 条", self.screen.get_width() // 2,
                           self.screen.get_height() // 2)
            time.sleep(2)  # 暂停2秒以显示信息
            # ... 重置游戏到当前生命的状态 ...
        else:
            self.game_over()

    def game_over(self):
        self.show_text("游戏结束！", self.screen.get_width() // 2, self.screen.get_height() // 2)
        time.sleep(2)  # 暂停2秒以显示游戏结束信息
        # ... 提供重新开始或退出游戏的选项 ...

    # ... 其他方法定义 ...

    def run(self):
        # ... run 方法内容 ...

# 主程序
if __name__ == "__main__":
    pygame.init()  # 初始化pygame
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)  # 创建屏幕对象
    pygame.display.set_caption("打砖块游戏")
    font = pygame.font.SysFont('SimHei', 24)
    leaderboard = Leaderboard(screen, font)
    game = Game(screen, font)
    game.leaderboard = leaderboard  # 将排行榜实例传递给游戏实例
    game.run()
