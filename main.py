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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.loc = pygame.math.Vector2(320, 400)
        self.v = pygame.math.Vector2(5, 0)
        self.image = pygame.Surface([50, 10])
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
        self.points = 0

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

    def add_point(self):
        self.points += 1

    def show_points(self):
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(self.points), True, 'green')
        screen.blit(img, (10, 10))


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
    def __init__(self, player : Player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.loc = pygame.math.Vector2(random.randint(50, width-50), height/2)
        self.v = pygame.math.Vector2(-5, 5)
        self.rect.center = self.loc

    def move(self):
        if self.loc.x <= 10 or self.loc.x >= width - 10:
            self.v.x = -self.v.x

        if self.loc.y <= 10:
            self.v.y = -self.v.y

        if pygame.sprite.collide_rect(self.player, self):
            self.v.y = -self.v.y

        self.loc += self.v
        self.rect.center = self.loc

    def change_y_direction(self):
        self.v.y = -self.v.y

    def draw(self):
        pygame.draw.rect(screen, 'yellow', self.rect)

class Field(pygame.sprite.Sprite):
    def __init__(self, ball : Ball, player : Player):
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

    def hit_brick(self):
        """
        Tarkistaa, osuuko pallo tiileen. Jos osuu, palauttaa kyseisen tiilen, jos ei palauttaa None.
        """
        return pygame.sprite.spritecollideany(self.ball, self.bricks)

    def remove_brick(self, brick):
        self.bricks.remove(brick)

    def draw(self):
        self.ball.draw()
        self.player.draw()
        self.bricks.draw(screen)

class EventHandler():
    def __init__(self):
        self.events = pygame.event.get()

    def get_events(self):
        self.events = pygame.event.get()
        return self.events

    def left_arrow_pressed(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return True

        return False

    def right_arrow_pressed(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                return True

        return False

    def left_arrow_not_pressed(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                return True
        
        return False

    def right_arrow_not_pressed(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                return True
        
        return False

    def close_pressed(self, event):
        if event.type == pygame.QUIT:
            return True
        return False

    def close_window(self):
        exit()
    

if __name__ == '__main__':
    player = Player()
    ball = Ball(player)
    field = Field(ball, player)
    event_handler = EventHandler()

    left = False
    right = False

    field.create_bricks(9)

    while True:
        events = event_handler.get_events()
        for event in events:
            if event_handler.close_pressed(event):
                event_handler.close_window()

            if event_handler.left_arrow_pressed(event):
                left = True
            elif event_handler.right_arrow_pressed(event):
                right = True

            if event_handler.left_arrow_not_pressed(event):
                left = False
            elif event_handler.right_arrow_not_pressed(event):
                right = False

        if left:
            player.move_left()
        
        if right:
            player.move_right()

        hitted_brick = field.hit_brick()
        if hitted_brick != None:
            field.remove_brick(hitted_brick)
            player.add_point()
            ball.change_y_direction()

        screen.fill((0,0,0))
        field.draw()
        player.show_points()
        ball.move()
        pygame.display.flip()
        clock.tick(60)