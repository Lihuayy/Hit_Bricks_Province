"""""
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
        keys = pygame.key.get_pressed()
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

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("打砖块")
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

        self.font = pygame.font.SysFont("宋体", 36)

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

        self.balls.update(self.paddle.sprite)

        # 球与砖块的碰撞检测
        for ball in self.balls:
            bricks_hit = pygame.sprite.spritecollide(ball, self.bricks, True)
            if len(bricks_hit) > 0:
                ball.dy = -ball.dy
                self.score += len(bricks_hit)

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

    def login(self):
        input_box = pygame.Rect(300, 250, 200, 50)
        active = False
        text = ""
        while not self.logged_in:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            self.username = text
                            self.logged_in = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)
            self.draw_text("请输入用户名：", WIDTH // 2, HEIGHT // 2 - 50)
            self.draw_text(text, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            self.clock.tick(60)

    def play(self):
        running = True
        self.create_paddle()
        self.start()
        while running:
            if not self.logged_in:
                self.login()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_over:
                            self.restart()
                        elif self.paused:
                            self.resume()
                        elif not self.level_completed:
                            self.start()

            self.screen.fill((0, 0, 0))
            self.bricks.draw(self.screen)
            self.balls.draw(self.screen)
            self.paddle.draw(self.screen)

            self.update()

            # 显示生命值和得分
            self.draw_text("Lives: " + str(self.lives), 70, 30)
            self.draw_text("Score: " + str(self.score), WIDTH - 70, 30)

            if self.paused:
                self.draw_text("暂停", WIDTH // 2, HEIGHT // 2)

            if self.game_over:
                self.draw_text("游戏结束", WIDTH // 2, HEIGHT // 2)
                self.draw_text("按空格键重新开始", WIDTH // 2, HEIGHT // 2 + 30)

            if self.level_completed:
                self.next_level()
                self.level_completed = False

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.play()
""""""
""""""
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
        keys = pygame.key.get_pressed()
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

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("打砖块")
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

        self.font = pygame.font.SysFont("simsunnsimsun", 36)

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

        self.balls.update(self.paddle.sprite)

        # 球与砖块的碰撞检测
        for ball in self.balls:
            bricks_hit = pygame.sprite.spritecollide(ball, self.bricks, True)
            if len(bricks_hit) > 0:
                ball.dy = -ball.dy
                self.score += len(bricks_hit)

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

    def login(self):
        input_box = pygame.Rect(300, 250, 200, 50)
        active = False
        text = ""
        while not self.logged_in:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            self.username = text
                            self.logged_in = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)
            self.draw_text("请输入用户名：", WIDTH // 2, HEIGHT // 2 - 50)
            self.draw_text(text, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            self.clock.tick(60)

    def play(self):
        running = True
        self.create_paddle()
        self.start()
        while running:
            if not self.logged_in:
                self.login()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_over:
                            self.restart()
                        elif self.paused:
                            self.resume()
                        elif not self.level_completed:
                            self.start()

            self.screen.fill((0, 0, 0))
            self.bricks.draw(self.screen)
            self.balls.draw(self.screen)
            self.paddle.draw(self.screen)

            self.update()

            # 显示生命值和得分
            self.draw_text("生命值: " + str(self.lives), 70, 30)
            self.draw_text("得分: " + str(self.score), WIDTH - 70, 30)

            if self.paused:
                self.draw_text("暂停", WIDTH // 2, HEIGHT // 2)

            if self.game_over:
                self.draw_text("游戏结束", WIDTH // 2, HEIGHT // 2)
                self.draw_text("按空格键重新开始", WIDTH // 2, HEIGHT // 2 + 30)

            if self.level_completed:
                self.next_level()
                self.level_completed = False

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.play()
"""""

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
        keys = pygame.key.get_pressed()
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

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("打砖块")
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

        self.font = pygame.font.SysFont("simsunnsimsun", 36)

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

        self.balls.update(self.paddle.sprite)

        # 球与砖块的碰撞检测
        for ball in self.balls:
            bricks_hit = pygame.sprite.spritecollide(ball, self.bricks, True)
            if len(bricks_hit) > 0:
                ball.dy = -ball.dy
                self.score += len(bricks_hit)

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

    def login(self):
        input_box = pygame.Rect(300, 250, 200, 50)
        active = False
        text = ""
        while not self.logged_in:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            self.username = text
                            self.logged_in = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)
            self.draw_text("请输入用户名：", WIDTH // 2, HEIGHT // 2 - 50)
            self.draw_text(text, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            self.clock.tick(60)

    def play(self):
        running = True
        self.create_paddle()
        self.start()
        while running:
            if not self.logged_in:
                self.login()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_over:
                            self.restart()
                        elif self.paused:
                            self.resume()
                        elif not self.level_completed:
                            self.start()

            self.screen.fill((0, 0, 0))
            self.bricks.draw(self.screen)
            self.balls.draw(self.screen)
            self.paddle.draw(self.screen)

            self.update()

            # 显示生命值和得分
            self.draw_text("生命值: " + str(self.lives), 70, 30)
            self.draw_text("得分: " + str(self.score), WIDTH - 70, 30)

            if self.paused:
                self.draw_text("暂停", WIDTH // 2, HEIGHT // 2)

            if self.game_over:
                self.draw_text("游戏结束", WIDTH // 2, HEIGHT // 2)
                self.draw_text("按空格键重新开始", WIDTH // 2, HEIGHT // 2 + 30)

            if self.level_completed:
                self.next_level()
                self.level_completed = False

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.play()
