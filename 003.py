import pygame
import sys
import random
import time

# 初始化 pygame
pygame.init()

# 设置游戏窗口尺寸
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('打砖块游戏')

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 定义挡板
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 20
        self.speed = 0

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

# 定义砖块
class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((80, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 定义球
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.speedx = 5
        self.speedy = 5

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.speedx = -self.speedx

        if self.rect.top < 0:
            self.speedy = -self.speedy

# 创建砖块
def create_bricks(level):
    bricks = pygame.sprite.Group()
    colors = [BLUE, RED, WHITE]
    for row in range(5):
        for column in range(10):
            brick = Brick(random.choice(colors), column * 80 + 60, row * 30 + 50)
            bricks.add(brick)
    return bricks

# 游戏开始动画
def game_start_animation():
    for i in range(3, 0, -1):
        WINDOW.fill(BLACK)
        font = pygame.font.SysFont(None, 100)
        text = font.render(str(i), True, WHITE)
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        WINDOW.blit(text, rect)
        pygame.display.flip()
        pygame.time.wait(1000)
    WINDOW.fill(BLACK)
    pygame.display.flip()
    pygame.time.wait(1000)

# 游戏结束动画
def game_over_animation():
    font = pygame.font.SysFont(None, 100)
    text = font.render("Game Over", True, RED)
    rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    WINDOW.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# 游戏胜利动画
def game_win_animation():
    font = pygame.font.SysFont(None, 100)
    text = font.render("You Win!", True, GREEN)
    rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    WINDOW.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# 游戏状态
class GameState:
    def __init__(self):
        self.game_over = False
        self.game_win = False
        self.game_paused = False
        self.game_started = False
        self.lives = 3
        self.level = 1
        self.start_time = 0
        self.end_time = 0
        self.bricks = pygame.sprite.Group()

    def start_game(self):
        self.game_started = True
        self.start_time = time.time()
        self.bricks = create_bricks(self.level)

    def reset_game(self):
        self.game_over = False
        self.game_win = False
        self.game_paused = False
        self.game_started = False
        self.lives = 3
        self.level = 1
        self.start_time = 0
        self.end_time = 0
        self.bricks = pygame.sprite.Group()

# 主函数
def main():
    clock = pygame.time.Clock()

    paddle = Paddle()
    ball = Ball()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle, ball)

    game_state = GameState()

    # 游戏循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle.speed = -5
                elif event.key == pygame.K_RIGHT:
                    paddle.speed = 5

                # 暂停游戏
                if event.key == pygame.K_p and game_state.game_started and not game_state.game_over and not game_state.game_win:
                    game_state.game_paused = not game_state.game_paused

                # 开始游戏
                if event.key == pygame.K_s and not game_state.game_started:
                    game_state.start_game()
                    game_start_animation()

                # 重新开始游戏
                if event.key == pygame.K_r and (game_state.game_over or game_state.game_win):
                    game_state.reset_game()
                    game_start_animation()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and paddle.speed < 0:
                    paddle.speed = 0
                elif event.key == pygame.K_RIGHT and paddle.speed > 0:
                    paddle.speed = 0

        # 如果游戏开始且没有结束，则更新游戏状态
        if game_state.game_started and not game_state.game_over and not game_state.game_win and not game_state.game_paused:
            all_sprites.update()

            # 检测球和砖块的碰撞
            hits = pygame.sprite.spritecollide(ball, game_state.bricks, True)
            if hits:
                ball.speedy = -ball.speedy

            # 检测球和挡板的碰撞
            if pygame.sprite.collide_rect(ball, paddle):
                ball.speedy = -ball.speedy

            # 如果球落到底部，减少生命值
            if ball.rect.top > WINDOW_HEIGHT:
                game_state.lives -= 1
                if game_state.lives <= 0:
                    game_state.game_over = True
                    game_over_animation()

                ball.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                ball.speedx = 5
                ball.speedy = 5

            # 如果砖块全部消失，游戏胜利
            if len(game_state.bricks) == 0:
                game_state.game_win = True
                game_state.end_time = time.time()
                game_win_animation()

                # 游戏胜利后，进入下一关
                game_state.level += 1
                game_state.bricks = create_bricks(game_state.level)

        # 游戏暂停时，显示提示信息
        elif game_state.game_paused:
            pause_font = pygame.font.SysFont(None, 50)
            pause_text = pause_font.render("游戏暂停", True, WHITE)
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            WINDOW.blit(pause_text, pause_rect)

        # 游戏开始前，显示提示信息
        elif not game_state.game_started:
            start_font = pygame.font.SysFont(None, 50)
            start_text1 = start_font.render("按 'S' 开始游戏", True, WHITE)
            start_text2 = start_font.render("按 'P' 暂停游戏", True, WHITE)
            start_rect1 = start_text1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            start_rect2 = start_text2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            WINDOW.blit(start_text1, start_rect1)
            WINDOW.blit(start_text2, start_rect2)

        # 绘制游戏界面
        WINDOW.fill(BLACK)
        all_sprites.draw(WINDOW)

        # 绘制生命值
        lives_font = pygame.font.SysFont(None, 30)
        lives_text = lives_font.render(f"生命值: {game_state.lives}", True, WHITE)
        WINDOW.blit(lives_text, (10, 10))

        # 绘制关卡
        level_text = lives_font.render(f"关卡: {game_state.level}", True, WHITE)
        WINDOW.blit(level_text, (WINDOW_WIDTH - 100, 10))

        # 游戏结束时，显示提示信息
        if game_state.game_over:
            end_font = pygame.font.SysFont(None, 100)
            end_text = end_font.render("游戏失败", True, RED)
            end_rect = end_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            WINDOW.blit(end_text, end_rect)

        # 游戏胜利时，显示提示信息
        elif game_state.game_win:
            end_font = pygame.font.SysFont(None, 100)
            end_text = end_font.render("游戏胜利", True, GREEN)
            end_rect = end_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            WINDOW.blit(end_text, end_rect)

            # 计算通关时间
            pass_time = int(game_state.end_time - game_state.start_time)
            pass_time_text = lives_font.render(f"通关时间: {pass_time} 秒", True, WHITE)
            pass_time_rect = pass_time_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
            WINDOW.blit(pass_time_text, pass_time_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()