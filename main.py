#!/usr/bin/env python3
import pygame

pygame.init()

width = 640
height = 480
brick_width = width / 10
brick_height = height / 20

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

class MovingObject():
    def __init__(self):
        self.loc = pygame.math.Vector2(320, 400)
        self.v = pygame.math.Vector2(5, 0)
        self.r = 20
        self.rect = pygame.Rect(0,0,20,10)
        self.rect.center = self.loc

    def draw(self):
        pygame.draw.rect(screen, 'red', self.rect)
        # pygame.draw.circle(screen, 'red', self.loc, self.r)

    def move(self):
        if  not (0 <= self.loc.x <= screen.get_size()[0]):
            self.v = -self.v

        self.loc = self.loc + self.v
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


if __name__ == '__main__':
    ball = MovingObject()
    bricks = pygame.sprite.Group()
    x = brick_width
    y = brick_height
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

        screen.fill((0,0,0))
        ball.draw()
        bricks.draw(screen)
        ball.move()
        pygame.display.flip()
        clock.tick(60)