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
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill((255, 255, 255))
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

        self.create_bricks()
        self.create_ball()
        self.create_paddle()

    def create_bricks(self):
        for row in range(5):
            for column in range(10):
                brick = Brick(column * (BRICK_WIDTH + 5) + 50, row * (BRICK_HEIGHT + 5) + 50)
                self.bricks.add(brick)

    def create_ball(self):
        ball = Ball(WIDTH // 2, HEIGHT // 2, random.choice([-2, 2]), random.choice([-2, -3, -4]))
        self.balls.add(ball)

    def create_paddle(self):
        paddle = Paddle()
        self.paddle.add(paddle)

    def update(self):
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
                self.reset_game()

        # 球与球拍的碰撞检测
        for ball in self.balls:
            if pygame.sprite.spritecollide(ball, self.paddle, False):
                ball.dy = -ball.dy

    def reset_game(self):
        if self.lives == 0:
            print("Game Over")
            pygame.quit()
            quit()
        else:
            self.balls.empty()
            self.create_ball()

    def next_level(self):
        self.current_level += 1
        self.lives = 3
        self.create_bricks()
        self.create_ball()

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.paddle.sprite.dx = -5
                    elif event.key == pygame.K_RIGHT:
                        self.paddle.sprite.dx = 5
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.paddle.sprite.dx = 0

            self.screen.fill((0, 0, 0))
            self.bricks.draw(self.screen)
            self.balls.draw(self.screen)
            self.paddle.draw(self.screen)

            self.update()

            # 显示生命值和得分
            font = pygame.font.Font(None, 36)
            lives_text = font.render("Lives: " + str(self.lives), True, (255, 255, 255))
            score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
            self.screen.blit(lives_text, (10, 10))
            self.screen.blit(score_text, (10, 50))

            if len(self.bricks) == 0:
                if self.current_level == LEVELS:
                    print("Congratulations! You cleared all levels.")
                    pygame.quit()
                    quit()
                else:
                    self.next_level()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.play()
