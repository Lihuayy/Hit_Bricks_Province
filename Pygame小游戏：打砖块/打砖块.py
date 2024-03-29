#coding:utf-8
import pygame
from pygame.locals import *
import time
import random
import sys
import os

pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,25)

canvas = pygame.display.set_mode((1000,600))
canvas.fill((255,255,255))
pygame.display.set_caption("打砖块")

#加载图片
bg1=pygame.image.load("images/bg2.png")
bg2=pygame.image.load("images/bg1.png")
board=pygame.image.load("images/board.png")
c1=pygame.image.load("images/c2.png")
c2=pygame.image.load("images/c1.png")
life=pygame.image.load("images/life.png")
lose=pygame.image.load("images/lose.png")
win=pygame.image.load("images/win.png")
b=pygame.image.load("images/ball.png")
e1=pygame.image.load("images/enemy1.png")
e2=pygame.image.load("images/enemy2.png")
e3=pygame.image.load("images/enemy3.png")

def handleEvent(QUIT=None):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #鼠标移动事件
        if event.type == pygame.MOUSEMOTION:
            if Game.states == 'RUNNING':
                Game.player.x = event.pos[0] - Game.player.width / 2

#玩家类
class Player():
    def __init__(self,x,y,img):
        self.width=217
        self.height=10
        self.x=x
        self.y=y
        self.img = img
    def paint(self):
        canvas.blit(self.img,(self.x,self.y))
    def outOfBounds(self):
        if self.x<=30:
            self.x=30
        if self.x>=1000-30-self.width:
            self.x=1000-30-self.width
    def hit(self,c):
        return c.x > self.x - c.width and c.x < self.x+self.width and c.y > self.y-c.height and c.y < self.y+self.height

#弹球类
class Ball():
    def __init__(self,x,y,img):        
        self.width=46
        self.height=46
        self.x=x
        self.y=y
        self.img = img
        self.life=3
    def paint(self):
        canvas.blit(self.img,(self.x,self.y))
    def step(self):
        self.x=self.x+Game.m
        self.y=self.y-Game.n
        if self.x < 30:
            Game.m = random.randint(10,20)
        if self.x > 970:
            Game.m = -random.randint(10,20)
        if self.y < 15:
            Game.n = -random.randint(10,20)

#敌人类
class Enemy():
    def __init__(self,x,y,img):
        self.width=132
        self.height=48
        self.x=x
        self.y=y
        self.img = img
        self.life=1
    def paint(self):
        canvas.blit(self.img,(self.x,self.y))
    def hit(self,c):
        return c.x > self.x - c.width and c.x < self.x+self.width and c.y > self.y-c.height and c.y < self.y+self.height

#云类
class Cloud():
    def __init__(self,x,y,img):
        self.width=132
        self.height=48
        self.x=x
        self.y=y
        self.img = img
    def paint(self):
        canvas.blit(self.img,(self.x,self.y))
    def hit(self,c):
        return c.x > self.x - c.width and c.x < self.x+self.width and c.y > self.y-c.height and c.y < self.y+self.height

class Game():
    m=random.randint(10,20)
    n=random.randint(10,20)
    enemies=[Enemy(156,15,e1),Enemy(293,15,e2),Enemy(430,15,e3),Enemy(567,15,e2),Enemy(704,15,e1),
             Enemy(156,63,e3),Enemy(293,63,e2),Enemy(430,63,e1),Enemy(567,63,e2),Enemy(704,63,e3),
             Enemy(156,111,e1),Enemy(293,111,e2),Enemy(430,111,e3),Enemy(567,111,e2),Enemy(704,111,e1)]
    clouds=[Cloud(30,15,c1),Cloud(844,15,c2)]
    ball=Ball(500,400,b)
    player=Player(450,500,board)
    states='RUNNING'

def conPaint():
    canvas.blit(bg1,(0,0))
    Game.player.paint()
    canvas.blit(bg2,(0,0))
    Game.ball.paint()
    for enemy in Game.enemies:
        enemy.paint()
    for cloud in Game.clouds:
        cloud.paint()
    #绘制生命值
    if Game.ball.life==3:
        canvas.blit(life,(975,70))
        canvas.blit(life,(975,90))
        canvas.blit(life,(975,110))
    if Game.ball.life==2:
        canvas.blit(life,(975,70))
        canvas.blit(life,(975,90))
    if Game.ball.life==1:
        canvas.blit(life,(975,70))

def conStep():
    Game.ball.step()

def checkHit():
    for enemy in Game.enemies:
        if enemy.hit(Game.ball):
            enemy.life=0
            Game.m=-1*Game.m
            Game.n=-random.randint(10,20)
        for cloud in Game.clouds:
            if cloud.hit(Game.ball):
                Game.m = -1*Game.m
                Game.n=-random.randint(10,20)
        if Game.player.hit(Game.ball):
            Game.n=random.randint(10,20)
        if Game.ball.y > 600:
            Game.ball.life=Game.ball.life-1
            Game.ball.x=500
            Game.ball.y=200

def conDelete():
    for enemy in Game.enemies:
        if enemy.life == 0:
            Game.enemies.remove(enemy)

def gameOver():
    if len(Game.enemies) == 0 or Game.ball.life <=0:
        Game.states='OVER'

def control():
    if Game.states == 'RUNNING':
        conPaint()
        conStep()
        Game.player.outOfBounds()
        checkHit()
        conDelete()
        gameOver()

    if Game.states == 'OVER':
        conPaint()
        if len(Game.enemies)==0:
            canvas.blit(win,(250,150))
        if Game.ball.life<=0:
            canvas.blit(lose,(250,150))

while True:
    control()
    handleEvent()
    pygame.display.update()
    pygame.time.delay(10)