import pygame
import random

# 初始化pygame
pygame.init()

# 定义常数
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 720
BRICK_WIDTH = 80
BRICK_HEIGHT = 40
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
WHITE = (255, 255, 255)
BRICK_COLOR = (200, 200, 0)
BALL_COLOR = (255, 0, 0)
PADDLE_COLOR = (0, 255, 0)
FPS = 60
# 设置窗口模式和启用双缓冲
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)



# 设置屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("打砖块游戏")

# 加载并缩放背景图像
background_image = pygame.image.load('images_02/background.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
# 加载并缩放球拍图像
paddle_image = pygame.image.load('images_02/paddle.jpg')
paddle_image = pygame.transform.scale(paddle_image, (PADDLE_WIDTH, PADDLE_HEIGHT))
# 加载并缩放球图像
ball_image = pygame.image.load('images_02/ball.jpg')
ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))  # 乘以2因为直径是半径的两倍
brick_image = pygame.image.load('images_02/brick_image.jpg')
brick_image = pygame.transform.scale(brick_image, (BRICK_WIDTH, BRICK_HEIGHT))


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
ball_speed_x = 6 * random.choice((1, -1))
ball_speed_y = -6


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
        paddle.left -= 20  # 球拍移动速度
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.right += 20  # 球拍移动速度


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



        # 画面更新 - 开始
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill((0, 0, 0))  # 只有在没有背景图像时才需要填充背景颜色

        # 绘制所有游戏元素
        for brick in bricks:
            screen.blit(brick_image, brick)  # 绘制砖块图像
        screen.blit(paddle_image, paddle)  # 绘制球拍图像
        screen.blit(ball_image, ball)  # 绘制球图像

        # 更新屏幕
    pygame.display.flip()
    # 绘制砖块
    for brick in bricks:
        screen.blit(brick_image, brick.topleft)

        # 检查游戏是否结束
        if ball.bottom >= SCREEN_HEIGHT:
            print("游戏结束！")
            running = False
    # 控制游戏刷新速率
    clock.tick(FPS)

pygame.quit()
