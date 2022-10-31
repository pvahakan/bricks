#!/usr/bin/env python3
import pygame

pygame.init()

width = 640
height = 480

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

class MovingObject():
    def __init__(self):
        self.loc = pygame.math.Vector2(320, 240)
        self.v = pygame.math.Vector2(3, 0)
        self.r = 20

    def draw(self):
        pygame.draw.circle(screen, 'red', self.loc, self.r)

    def move(self):
        if  not (0 <= self.loc.x <= screen.get_size()[0]):
            self.v = -self.v

        self.loc = self.loc + self.v

if __name__ == '__main__':
    ball = MovingObject()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill((0,0,0))
        ball.draw()
        ball.move()
        pygame.display.flip()
        clock.tick(60)