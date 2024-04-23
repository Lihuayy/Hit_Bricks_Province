import pygame
import sys
import random

# 游戏界面的宽度和高度
WIDTH = 800
HEIGHT = 600

# 砖块的宽度和高度
BRICK_WIDTH = 60
BRICK_HEIGHT = 20

# 球拍的宽度和高度
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10

# 游戏关卡的数量
LEVELS = 3

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (200, 200, 200)
GREEN = (0, 255, 0)


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.image.load("ball.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = dx
        self.dy = dy
        self.initial_x = x
        self.initial_y = y

    def update(self, paddle):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # 碰撞检测逻辑
        if self.rect.x >= WIDTH or self.rect.x <= 0:
            self.dx = -self.dx
        if self.rect.y <= 0:
            self.dy = -self.dy
        if self.rect.colliderect(paddle.rect):
            self.dy = -self.dy
            self.rect.y = paddle.rect.y - self.rect.height

        if self.rect.y >= HEIGHT:
            return True

        return False

    def reset(self, x, y, dx, dy):
        self.rect.x = x
        self.rect.y = y
        self.dx = dx
        self.dy = dy

# ... (保持不变)

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - PADDLE_WIDTH // 2
        self.rect.y = HEIGHT - 50
        self.dx = 0

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.dx = -5
        elif keys[pygame.K_RIGHT]:
            self.dx = 5
        else:
            self.dx = 0

        self.rect.x += self.dx

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - PADDLE_WIDTH:
            self.rect.x = WIDTH - PADDLE_WIDTH


class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback

    def draw(self, screen, font):
        pygame.draw.rect(screen, LIGHT_GREY, self.rect)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.active = False
        self.color = LIGHT_GREY

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = GREEN if self.active else LIGHT_GREY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        pass

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surf = font.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("弹出新高度")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("微软雅黑", 36)
        self.clock = pygame.time.Clock()
        # 初始化logged_in属性
        self.logged_in = False
        # 加载背景音乐和音效
        pygame.mixer.music.load("BGM.flac")
        self.brick_sound = pygame.mixer.Sound("Brick striking.mp3")

        # 开始播放背景音乐
        pygame.mixer.music.play(-1)  # -1 表示无限循环播放

        # 加载背景图像
        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.bricks = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.paddle = pygame.sprite.GroupSingle()

        self.score = 0
        self.lives = 3
        self.current_level = 1
        self.paused = False
        self.game_over = False
        self.level_completed = False
        # 预定义的用户名和密码
        self.correct_username = "1234"
        self.correct_password = "1234"

        self.username_input = InputBox(300, 250, 200, 50)
        self.password_input = InputBox(300, 320, 200, 50)
        self.login_button = Button(300, 390, 200, 50, "登录", self.login)
        self.exit_button = Button(300, 460, 200, 50, "退出", self.quit_game)

    def login(self):
        username = self.username_input.text
        password = self.password_input.text
        if username == self.correct_username and password == self.correct_password:
            print("登录成功！")
            self.logged_in = True
        else:
            print("登录失败，用户名或密码错误。")
        # print(f"Logging in with username: {username} and password: {password}")
        # self.logged_in = True

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            self.username_input.handle_event(event)
            self.password_input.handle_event(event)
            self.login_button.handle_event(event)
            self.exit_button.handle_event(event)

    def draw_login_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text("启程砖块乐园", WIDTH // 2, HEIGHT // 2 - 100)
        self.username_input.draw(self.screen, self.font)
        self.password_input.draw(self.screen, self.font)
        self.login_button.draw(self.screen, self.font)
        self.exit_button.draw(self.screen, self.font)
        pygame.display.flip()


    def play(self):
        running = True
        while running:
            if not self.logged_in:
                self.handle_events()
                self.draw_login_screen()
                continue

            def create_bricks(self):
                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
                for row in range(self.current_level + 2):
                    for column in range(self.current_level + 5):
                        color = random.choice(colors)
                        brick = Brick(column * (BRICK_WIDTH + 5) + 50, row * (BRICK_HEIGHT + 5) + 50, color)
                        self.bricks.add(brick)

            def create_ball(self, paddle):
                x = paddle.rect.x + paddle.rect.width // 2
                y = paddle.rect.y - 20
                dx = random.choice([-2, 2])
                dy = -2
                ball = Ball(x, y, dx, dy)
                self.balls.add(ball)

            def create_paddle(self):
                paddle = Paddle()
                self.paddle.add(paddle)

            def update(self):
                if self.paused or self.game_over:
                    return

                keys = pygame.key.get_pressed()
                self.paddle.update(keys)
                self.balls.update(self.paddle.sprite)

                # 球与砖块的碰撞检测
                for ball in self.balls:
                    bricks_hit = pygame.sprite.spritecollide(ball, self.bricks, True)
                    if len(bricks_hit) > 0:
                        ball.dy = -ball.dy
                        self.score += len(bricks_hit)
                        self.brick_sound.play()  # 播放砖块碰撞音效

                # 判断关卡是否完成
                if len(self.bricks) == 0:
                    self.level_completed = True

                # 判断球是否掉出屏幕
                for ball in self.balls:
                    if ball.update(self.paddle.sprite):
                        self.lives -= 1
                        if self.lives <= 0:
                            self.game_over = True
                        else:
                            self.create_ball(self.paddle.sprite)

            def reset_ball(self):
                self.balls.empty()

            def next_level(self):
                self.current_level += 1
                self.lives = 3
                self.bricks.empty()
                self.create_bricks()
                self.reset_ball()
                self.create_ball(self.paddle.sprite)

            def start(self):
                self.paused = False
                self.game_over = False
                self.create_bricks()
                self.create_ball(self.paddle.sprite)

            def pause(self):
                self.paused = True

            def resume(self):
                self.paused = False

            def restart(self):
                self.current_level = 1
                self.score = 0
                self.lives = 3
                self.bricks.empty()
                self.create_bricks()
                self.reset_ball()
                self.create_ball(self.paddle.sprite)

                self.start()

            def draw_text(self, text, x, y):
                text_surface = self.font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect.center = (x, y)
                self.screen.blit(text_surface, text_rect)

    def draw_text(self, param, param1, param2):
        pass


if __name__ == "__main__":
    game = Game()
    game.play()
