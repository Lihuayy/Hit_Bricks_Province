import pygame
import random

# 初始化pygame
pygame.init()

# 定义常数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
WHITE = (255, 255, 255)
BRICK_COLOR = (200, 200, 0)
BALL_COLOR = (255, 0, 0)
PADDLE_COLOR = (0, 255, 0)
FPS = 60

# 设置屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("打砖块游戏")

# 创建砖块
bricks = []
for y in range(5):
    for x in range(SCREEN_WIDTH // BRICK_WIDTH):
        brick_rect = pygame.Rect(x * BRICK_WIDTH, y * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick_rect)

# 创建球拍
paddle = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# 创建球
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
ball_speed_x = 4 * random.choice((1, -1))
ball_speed_y = -4

# 游戏循环
clock = pygame.time.Clock()
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 移动球拍
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= 6
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.right += 6

    # 移动球
    ball.left += ball_speed_x
    ball.top += ball_speed_y
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.colliderect(paddle) and ball_speed_y > 0:
        ball_speed_y *= -1

    # 检查球是否击中砖块
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y *= -1
            break

    # 检查游戏是否结束
    if ball.bottom >= SCREEN_HEIGHT:
        print("游戏结束！")
        running = False

    # 画面更新
    screen.fill((0, 0, 0))
    for brick in bricks:
        pygame.draw.rect(screen, BRICK_COLOR, brick)
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)
    pygame.draw.circle(screen, BALL_COLOR, ball.center, BALL_RADIUS)
    pygame.display.flip()

    # 控制游戏刷新速率
    clock.tick(FPS)

pygame.quit()


