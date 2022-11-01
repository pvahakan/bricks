#!/usr/bin/env python3
import pygame
import random

pygame.init()

width = 640
height = 480
brick_width = width / 10
brick_height = height / 20

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

class MovingObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.loc = pygame.math.Vector2(320, 400)
        self.v = pygame.math.Vector2(5, 0)
        self.image = pygame.Surface([20, 10])
        self.rect = self.image.get_rect()
        self.rect.center = self.loc

    def draw(self):
        pygame.draw.rect(screen, 'red', self.rect)
        # pygame.draw.circle(screen, 'red', self.loc, self.r)

    def move_left(self):
        if 20 <= self.loc.x <= screen.get_size()[0]:
            self.loc -= self.v
            self.rect.center = self.loc

    def move_right(self):
        if 0 <= self.loc.x <= screen.get_size()[0] - 20:
            self.loc += self.v
            self.rect.center = self.loc


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([brick_width, brick_height])
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        self.loc = pygame.math.Vector2(x, y)
        self.rect.center = self.loc

    def draw(self):
        pygame.draw.rect(screen, 'blue', self.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self, player : MovingObject):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.loc = pygame.math.Vector2(random.randint(50, width-50), height/2)
        self.v = pygame.math.Vector2(-1, 1)
        self.rect.center = self.loc

    def move(self):
        if pygame.sprite.collide_rect(self.player, self):
            self.v.y = -self.v.y

        self.loc += self.v
        self.rect.center = self.loc

    def draw(self):
        pygame.draw.rect(screen, 'yellow', self.rect)

class Field(pygame.sprite.Sprite):
    def __init__(self, ball : Ball, player : MovingObject):
        super().__init__()
        self.ball = ball
        self.player = player
        self.bricks = pygame.sprite.Group()

    def create_bricks(self, n : int):
        x = brick_width
        y = brick_height
        for i in range(n):
            self.bricks.add(Brick(x, y))
            if x < width - brick_width:
                x += brick_width + 1
            else:
                x = brick_width
                y += brick_height + 1

    def draw(self):
        self.ball.draw()
        self.player.draw()
        self.bricks.draw(screen)

def main():
    player = MovingObject()
    bricks = pygame.sprite.Group()
    ball = Ball(player)
    x = brick_width
    y = brick_height
    left = False
    right = False
    for i in range(54):
        bricks.add(Brick(x, y))
        if x < width - brick_width:
            x += brick_width + 1
        else:
            x = brick_width
            y += brick_height + 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_RIGHT:
                    right = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_RIGHT:
                    right = False

        if left:
            player.move_left()
        
        if right:
            player.move_right()

        screen.fill((0,0,0))
        player.draw()
        bricks.draw(screen)
        ball.draw()
        ball.move()
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    player = MovingObject()
    ball = Ball(player)
    field = Field(ball, player)

    left = False
    right = False

    field.create_bricks(54)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_RIGHT:
                    right = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_RIGHT:
                    right = False

        if left:
            player.move_left()
        
        if right:
            player.move_right()

        screen.fill((0,0,0))
        field.draw()
        ball.move()
        pygame.display.flip()
        clock.tick(60)