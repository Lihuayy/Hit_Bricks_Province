import pygame
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
        self.image = pygame.image.load("images_03/ball.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = dx
        self.dy = dy
        self.initial_x = x
        self.initial_y = y

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # 碰撞检测逻辑
        if self.rect.x >= WIDTH or self.rect.x <= 0:
            self.dx = -self.dx
        if self.rect.y <= 0:
            self.dy = -self.dy
        if self.rect.y >= HEIGHT:
            self.reset_ball()

    def reset_ball(self):
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.dx = random.choice([-2, 2])
        self.dy = random.choice([-2, -3, -4])

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - PADDLE_WIDTH // 2
        self.rect.y = HEIGHT - 50
        self.dx = 0

    def update(self):
        self.rect.x += self.dx

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - PADDLE_WIDTH:
            self.rect.x = WIDTH - PADDLE_WIDTH

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()

        self.bricks = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.paddle = pygame.sprite.GroupSingle()

        self.score = 0
        self.lives = 3
        self.current_level = 1
        self.paused = False
        self.game_over = False
        self.level_completed = False
        self.logged_in = False
        self.username = ""

        self.create_bricks()
        self.create_ball()
        self.create_paddle()

        self.font = pygame.font.Font(None, 36)

    def create_bricks(self):
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for row in range(self.current_level + 2):
            for column in range(self.current_level + 5):
                color = random.choice(colors)
                brick = Brick(column * (BRICK_WIDTH + 5) + 50, row * (BRICK_HEIGHT + 5) + 50, color)
                self.bricks.add(brick)

    def create_ball(self):
        ball = Ball(WIDTH // 2, HEIGHT // 2, random.choice([-2, 2]), random.choice([-2, -3, -4]))
        self.balls.add(ball)

    def create_paddle(self):
        paddle = Paddle()
        self.paddle.add(paddle)

    def update(self):
        if self.paused or self.game_over:
            return

        self.balls.update()
        self.paddle.update()

        # 球与砖块的碰撞检测
        for ball in self.balls:
            bricks_hit = pygame.sprite.spritecollide(ball, self.bricks, True)
            if len(bricks_hit) > 0:
                ball.dy = -ball.dy
                self.score += len(bricks_hit)

        # 球与边界的碰撞检测
        for ball in self.balls:
            if ball.rect.y >= HEIGHT:
                self.lives -= 1
                self.reset_ball()

        # 球与球拍的碰撞检测
        for ball in self.balls:
            if pygame.sprite.spritecollide(ball, self.paddle, False):
                ball.dy = -ball.dy

        # 判断关卡是否完成
        if len(self.bricks) == 0:
            self.level_completed = True

    def reset_ball(self):
        self.balls.empty()
        self.create_ball()

    def next_level(self):
        self.current_level += 1
        self.lives = 3
        self.bricks.empty()
        self.create_bricks()
        self.create_ball()

    def start(self):
        self.paused = False
        self.game_over = False

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
        self.create_ball()

        self.start()

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def login(self):
        self.username = input("请输入用户名：")
        self.logged_in = True

    def play(self):
        running = True
        while running:
            if not self.logged_in:
                self.login()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.paddle.sprite.dx = -5
                    elif event.key == pygame.K_RIGHT:
                        self.paddle.sprite.dx = 5
                    elif event.key == pygame.K_SPACE:
                        if self.game_over:
                            self.restart()
                        elif self.paused:
                            self.resume()
                        elif not self.level_completed:
                            self.start()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.paddle.sprite.dx = 0

            self.screen.fill((0, 0, 0))
            self.bricks.draw(self.screen)
            self.balls.draw(self.screen)
            self.paddle.draw(self.screen)

            self.update()

            # 显示生命值和得分
            self.draw_text("Lives: " + str(self.lives), 70, 30)
            self.draw_text("Score: " + str(self.score), WIDTH - 70, 30)

            if self.paused:
                self.draw_text("Paused", WIDTH // 2, HEIGHT // 2)

            if self.game_over:
                self.draw_text("Game Over", WIDTH // 2, HEIGHT // 2)
                self.draw_text("Press SPACE to restart", WIDTH // 2, HEIGHT // 2 + 30)

            if self.level_completed:
                self.next_level()
                self.level_completed = False

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.play()
