import pygame
import sys
import time
import random


# 游戏对象定义
class Game:
    def __init__(self,screen,font):
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
        self.screen = screen
        self.font = pygame.font.SysFont('SimHei', 24)
        self.running = True
        self.paused = False
        self.start_time = time.time()
        self.elapsed_time = 0
        self.ui = UserInterface(screen)
        self.screen = screen
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
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == 'start':
                        # 在开始状态下，按下任意键开始游戏
                        self.start_game()
                    elif event.key == pygame.K_p:
                        # 当游戏正在运行时按下 P 键暂停游戏
                        if self.state == 'running':
                            self.pause_game()
                        # 当游戏已暂停时按下 P 键继续游戏
                        elif self.state == 'paused':
                            self.unpause_game()
                    elif event.key == pygame.K_r and self.state == 'game over':
                        # 游戏结束状态下按下 R 键重置游戏
                        self.reset_game()

            self.screen.fill((0, 0, 0))  # 清屏
            if self.state == 'start':
                # 显示开始提示
                self.show_text(self.start_text, self.screen.get_width() // 2, self.screen.get_height() // 2)
            elif self.state == 'running':
                # 更新游戏状态
                self.paddle.update(self.keys_pressed)  # 更新球拍位置
                self.ball.update()  # 更新球的位置
                # 检测球与挡板的碰撞
                if pygame.sprite.collide_rect(self.ball, self.paddle):
                    self.ball.bounce_off_paddle(self.paddle.rect)

                # 检测球与砖块的碰撞
                brick_collision_list = pygame.sprite.spritecollide(self.ball, self.bricks, False)
                for brick in brick_collision_list:
                    self.ball.bounce_off_brick(brick.rect)
                    brick.kill()  # 移除碰撞的砖块
                    self.generate_powerup(brick.rect.center)  # 生成道具

                # 检测玩家挡板与道具的碰撞
                powerup_hits = pygame.sprite.spritecollide(self.paddle, self.powerups, True)
                for powerup in powerup_hits:
                    self.activate_powerup(powerup)

                # 检查球是否掉出屏幕底部
                if self.ball.rect.top > self.screen.get_height():
                    self.lives -= 1
                    if self.lives == 0:
                        self.state = 'game over'
                    else:
                        self.reset_ball()

                # 绘制所有精灵
                self.all_sprites.draw(self.screen)
                self.all_sprites.draw(self.screen)  # 绘制所有精灵
            elif self.state == 'paused':
                # 显示暂停提示
                self.show_text(self.pause_text, self.screen.get_width() // 2, self.screen.get_height() // 2)
            elif self.state == 'game over':
                # 显示游戏结束提示
                self.show_text(self.game_over_text, self.screen.get_width() // 2, self.screen.get_height() // 2)

            pygame.display.flip()
            self.clock.tick(60)  # 设置帧率为60fps

    def start_game(self):
        self.state = 'running'
        self.reset_game()

    def pause_game(self):
        self.state = 'paused'
        self.show_text(self.pause_text, self.screen.get_width() // 2, self.screen.get_height() // 2)

    def unpause_game(self):
        self.state = 'running'

    def reset_game(self):
        # 重置游戏到初始状态
        self.state = 'running'
        # 初始化或重置游戏对象，如球拍、球、砖块，以及生命值等

    def show_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.show_text("游戏暂停，按 P 继续", self.screen.get_width() // 2, self.screen.get_height() // 2)
            self.elapsed_time += time.time() - self.start_time
        else:
            self.start_time = time.time()

    def restart_game(self):
        # 重置游戏状态，生命值和关卡等
        self.lives = 3
        self.start_time = time.time()
        self.paused = False
        # 显示重启游戏的信息
        self.show_text("游戏重新开始！", self.screen.get_width() // 2, self.screen.get_height() // 2)
        pygame.display.flip()
        time.sleep(2)  # 暂停2秒以显示提示信息

    def restart_level(self):
        self.levels[self.current_level_index].reset()
        self.lives = 3
        self.start_time = time.time()
        self.paused = False

    def update(self):
        # 更新游戏对象的状态
        pass

    def check_collisions(self):
        # 检测碰撞和游戏逻辑
        pass

    def render(self):
        # 渲染游戏对象到屏幕
        pass

    def show_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def next_level(self):
        if self.current_level_index < len(self.levels) - 1:
            self.current_level_index += 1
            self.levels[self.current_level_index].reset()
        else:
            self.show_victory_screen()

    def show_victory_screen(self):
        total_time = self.elapsed_time + (time.time() - self.start_time)
        self.leaderboard.add_score(self.ui.username, total_time)
        self.leaderboard.draw()
        pygame.display.flip()
        time.sleep(5)  # 暂停5秒以显示排行榜

    def activate_powerup(self, hit):
        pass

    def generate_powerup(self, x, y):
        pass

    def pause_game(self):
        pass

    def unpause_game(self):
        pass

    def reset_game(self):
        pass

    def start_game(self):
        pass

    def reset_ball(self):
        # 重置球的位置和速度
        self.ball.rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.ball.velocity = [3, -3]

    def generate_powerup(self, position):
        # 根据概率生成道具
        if random.random() < 0.1:  # 10% 的几率生成道具
            powerup = PowerUp(position[0], position[1], 'clear_bricks')
            self.powerups.add(powerup)
            self.all_sprites.add(powerup)

    def activate_powerup(self, powerup):
        # 根据道具类型激活效果
        if powerup.powerup_type == 'clear_bricks':
            self.clear_all_bricks()

    def clear_all_bricks(self):
        # 清除所有砖块
        for brick in self.bricks:
            brick.kill()


class Level:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        # 根据难度初始化砖块和其他元素

    def reset(self):
        # 重置关卡
        pass


# 其他游戏对象类（挡板、球、砖块、道具）的定义省略

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))  # 道具为红色方块，实际游戏中应使用图像
        self.rect = self.image.get_rect(topleft=(x, y))
        self.powerup_type = powerup_type  # 道具的类型，例如"clear_bricks"
        self.fall_speed = 2  # 道具下落的速度

    def update(self):
        self.rect.y += self.fall_speed
        if self.rect.top > 480:
            self.kill()  # 如果道具落出屏幕则移除
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 20))
        self.image.fill((255, 255, 255))  # 白色砖块，实际游戏中应使用图像
        self.rect = self.image.get_rect(topleft=(x, y))

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((80, 10))
        self.image.fill((255, 255, 255))  # 白色球拍
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.screen_width = pygame.display.get_surface().get_width()

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('ball.png')  # 加载球形图像
        self.image = pygame.transform.scale(self.image, (10, 10))  # 调整图像大小
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = [3, -3]  # 初始速度

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # 球碰到屏幕边缘反弹
        if self.rect.left <= 0 or self.rect.right >= 640:
            self.velocity[0] = -self.velocity[0]
        if self.rect.top <= 0:
            self.velocity[1] = -self.velocity[1]
# 用户界面类
class UserInterface:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('SimHei', 24)  # 使用支持中文的字体
        self.username = ""
        self.input_active = True
        self.cursor_blink = True
        self.cursor_time = pygame.time.get_ticks()

    def draw_text(self, text, position, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def draw_login_screen(self):
        self.screen.fill((0, 0, 0))  # 黑色背景

        # 计算文本和输入框的位置
        input_box_width = 200
        input_box_height = 32
        input_box_x = self.screen.get_width() // 2 - input_box_width // 2
        input_box_y = self.screen.get_height() // 2 - input_box_height // 2

        login_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
        pygame.draw.rect(self.screen, (255, 255, 255), login_box, 2)  # 绘制输入框

        # 绘制提示信息，水平和垂直居中
        prompt_text = "请在下方输入用户名，然后按回车键登录"
        self.draw_text(prompt_text, (self.screen.get_width() // 2 - 180, self.screen.get_height() // 2 - 50))

        if self.input_active:
            cursor = "|" if self.cursor_blink else ""
            self.draw_text(self.username + cursor, (input_box_x + 5, input_box_y + 5))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN:
                    self.input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode

    def update(self):
        # 闪烁光标效果
        if pygame.time.get_ticks() - self.cursor_time > 500:
            self.cursor_blink = not self.cursor_blink
            self.cursor_time = pygame.time.get_ticks()

    def display_login_screen(self):
        while self.input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.handle_event(event)

            self.update()
            self.draw_login_screen()
            pygame.display.flip()


# 排行榜类
class Leaderboard:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.scores = []  # 存储格式为 (username, time)

    def add_score(self, username, time):
        self.scores.append((username, time))
        self.scores.sort(key=lambda x: x[1])  # 按时间排序

    def draw(self):
        self.screen.fill((0, 0, 0))  # 黑色背景
        for i, score in enumerate(self.scores):
            # 只展示前5名
            if i < 5:
                text = f"{i+1}. {score[0]} - {score[1]:.2f} 秒"
                self.draw_text(text, (self.screen.get_width() // 2, 30 + i * 30))

    def draw_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)


    def update(self, username, time):
        self.scores.append((username, time))
        self.scores.sort(key=lambda x: x[1])  # 按时间排序
        self.display()

    def display(self):
        # 显示排行榜
        pass


# 游戏主程序
if __name__ == "__main__":
    # ui = UserInterface()
    # ui.display_login_screen()
    # username = ui.get_username()
    pygame.init()  # 初始化pygame
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)  # 创建屏幕对象
    pygame.display.set_caption("打砖块游戏")
    ui = UserInterface(screen)
    ui.display_login_screen()
    username = ui.username

    font = pygame.font.SysFont('SimHei', 24)
    leaderboard = Leaderboard(screen, font)
    game = Game(screen,font)
    game.leaderboard = leaderboard  # 将排行榜实例传递给游戏实例
    game.run()
