#!/usr/bin/env python3
import pygame
import random

pygame.init()

leveys = 640
korkeus = 480
tiilen_leveys = leveys / 10
tiilen_korkeus = korkeus / 10

naytto = pygame.display.set_mode((leveys, korkeus))
kello = pygame.time.Clock()

class Pelaaja(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.loc = pygame.math.Vector2(320, 400)
        self.v = pygame.math.Vector2(5, 0)
        self.image = pygame.Surface([leveys, 10])
        self.rect = self.image.get_rect()
        self.rect.center = self.loc
        self.points = 0

    def piirra(self):
        pygame.draw.rect(naytto, 'red', self.rect)
        # pygame.draw.circle(naytto, 'red', self.loc, self.r)

    def liiku_vasemmalle(self):
        if 20 <= self.loc.x <= naytto.get_size()[0]:
            self.loc -= self.v
            self.rect.center = self.loc

    def liiku_oikealle(self):
        if 0 <= self.loc.x <= naytto.get_size()[0] - 20:
            self.loc += self.v
            self.rect.center = self.loc

    def lisaa_piste(self):
        self.points += 1

    def nayta_pisteet(self):
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(self.points), True, 'green')
        naytto.blit(img, (10, 10))


class Tiili(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([tiilen_leveys, tiilen_korkeus])
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        self.loc = pygame.math.Vector2(x, y)
        self.rect.x = self.loc.x
        self.rect.y = self.loc.y
        self.rect.center = self.loc

    def piirra(self):
        pygame.draw.rect(naytto, 'blue', self.rect)

    def sijainti(self):
        """
        Returns bricks center point as a Vector2.
        """
        return self.loc

class Pallo(pygame.sprite.Sprite):
    def __init__(self, pelaaja : Pelaaja):
        pygame.sprite.Sprite.__init__(self)
        self.pelaaja = pelaaja
        self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.loc = pygame.math.Vector2(random.randint(50, leveys-50), korkeus/2)
        # self.loc = pygame.math.Vector2(10, tiilen_korkeus + 91)
        # self.loc = pygame.math.Vector2(20, 20)
        self.v = pygame.math.Vector2(3, 3)
        print(pygame.math.Vector2.magnitude(self.v))
        self.rect.center = self.loc

    def liiku(self):
        if self.loc.x <= 10 or self.loc.x >= leveys - 10:
            self.v.x = -self.v.x

        if self.loc.y <= 10:
            self.v.y = -self.v.y

        if pygame.sprite.collide_rect(self.pelaaja, self):
            self.v.y = -self.v.y

        self.loc += self.v
        self.rect.center = self.loc

    def is_inside(self, brick):
        print(f'ball.top: {self.rect.top} ball.bottom: {self.rect.bottom} ball.left: {self.rect.left} ball.right: {self.rect.right}')
        print(f'brick.top: {brick.rect.top} brick.bottom: {brick.rect.bottom} brick.left: {brick.rect.left} brick.right: {brick.rect.right}')

    def osuu_pohjaan(self, brick):
        if abs(brick.rect.bottom - self.rect.top) <= pygame.math.Vector2.magnitude(self.v):
            print('osui pohjasta')
            return True
        return False

    def osuu_ylareunaan(self, brick):
        if abs(brick.rect.top - self.rect.bottom) <= pygame.math.Vector2.magnitude(self.v):
            print('osui ylhäältä')
            return True
        return False

    def osuu_vasempaan_reunaan(self, brick):
        if abs(brick.rect.left - self.rect.right) <= pygame.math.Vector2.magnitude(self.v):
            print('osui vasemmalta')
            return True
        return False

    def osuu_oikeaan_reunaan(self, brick):
        if abs(brick.rect.right - self.rect.left) <= pygame.math.Vector2.magnitude(self.v):
            print('osui oikealta')
            return True
        return False

    def osuu_vasempaan_ylanurkkaan(self, brick):
        if abs(self.rect.bottom - brick.rect.top) <= 2 and abs(self.rect.right - brick.rect.left) <= 2: # pygame.math.Vector2.magnitude(self.v):
            print('osui oikeaan ylänurkkaan')
            return True
        return False

    def osuu_oikeaan_ylanurkkaan(self, brick):
        if abs(self.rect.bottom - brick.rect.top) <= 2 and abs(self.rect.left - brick.rect.right) <= 2: # pygame.math.Vector2.magnitude(self.v):
            print('osui oikeaan ylänurkkaan')
            return True
        return False

    def osuu_vasempaan_alanurkkaan(self, brick):
        if abs(self.rect.top - brick.rect.bottom) <= 2 and abs(self.rect.right - brick.rect.left) <= 2: # pygame.math.Vector2.magnitude(self.v):
            print('osui vasempaan alanurkkaan')
            return True
        return False

    def osuu_oikeaan_alanurkkaan(self, brick):
        if abs(self.rect.top - brick.rect.bottom) <= 2 and abs(self.rect.left - brick.rect.right) <= 2: # pygame.math.Vector2.magnitude(self.v):
            print('osui oikeaan alanurkkaan')
            return True
        return False

    def muuta_y_suunta(self):
        self.v.y = -self.v.y

    def muuta_x_suunta(self):
        self.v.x = -self.v.x

    def piirra(self):
        pygame.draw.rect(naytto, 'yellow', self.rect)

    def pois_pelista(self):
        if self.loc.y >= korkeus:
            return True
        return False

class Kentta(pygame.sprite.Sprite):
    def __init__(self, ball : Pallo, pelaaja : Pelaaja):
        super().__init__()
        self.ball = ball
        self.pelaaja = pelaaja
        self.bricks = pygame.sprite.Group()

    def lisaa_tiili(self, x, y):
        self.bricks.add(Tiili(x, y))

    def luo_tiilet(self, n : int):
        x = tiilen_leveys
        y = tiilen_korkeus
        for i in range(n):
            self.bricks.add(Tiili(x, y))
            if x < leveys - tiilen_leveys:
                x += tiilen_leveys + 1
            else:
                x = tiilen_leveys
                y += tiilen_korkeus + 1

    def osuma_tiileen(self):
        """
        Tarkistaa, osuuko pallo tiileen. Jos osuu, palauttaa kyseisen tiilen, jos ei palauttaa None.
        """
        return pygame.sprite.spritecollideany(self.ball, self.bricks)

    def poista_tiili(self, brick):
        self.bricks.remove(brick)

    def piirra(self):
        self.ball.piirra()
        self.pelaaja.piirra()
        self.bricks.draw(naytto)

class TapahtumanKasittelija():
    def __init__(self):
        self.events = pygame.event.get()

    def hae_tapahtumat(self):
        self.events = pygame.event.get()
        return self.events

    def vasen_nuoli_painettu(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return True

        return False

    def oikea_nuoli_painettu(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                return True

        return False

    def vasen_nuoli_ei_painettu(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                return True
        
        return False

    def oikea_nuoli_ei_painettu(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                return True
        
        return False

    def rasti_klikattu(self, event):
        if event.type == pygame.QUIT:
            return True
        return False

    def close_window(self):
        """
        Ehkä turha funktio
        """
        exit()
    

if __name__ == '__main__':
    pelaaja = Pelaaja()
    ball = Pallo(pelaaja)
    field = Kentta(ball, pelaaja)
    event_handler = TapahtumanKasittelija()

    left = False
    right = False

    running = True

    field.luo_tiilet(9)
    # field.lisaa_tiili(50, 50)

    while running:

        events = event_handler.hae_tapahtumat()
        for event in events:
            if event_handler.rasti_klikattu(event):
                # event_handler.close_window()
                running = False

            if event_handler.vasen_nuoli_painettu(event):
                left = True
            elif event_handler.oikea_nuoli_painettu(event):
                right = True

            if event_handler.vasen_nuoli_ei_painettu(event):
                left = False
            elif event_handler.oikea_nuoli_ei_painettu(event):
                right = False

        if left:
            pelaaja.liiku_vasemmalle()
        
        if right:
            pelaaja.liiku_oikealle()

        hitted_brick = field.osuma_tiileen()
        if hitted_brick != None:
            ball.is_inside(hitted_brick)
            if ball.osuu_vasempaan_reunaan(hitted_brick):
                ball.muuta_x_suunta()
                field.poista_tiili(hitted_brick)
                pelaaja.lisaa_piste()
            elif ball.osuu_oikeaan_reunaan(hitted_brick):
                ball.muuta_x_suunta()
                field.poista_tiili(hitted_brick)
                pelaaja.lisaa_piste()
            elif ball.osuu_pohjaan(hitted_brick):
                ball.muuta_y_suunta()
                field.poista_tiili(hitted_brick)
                pelaaja.lisaa_piste()
            elif ball.osuu_ylareunaan(hitted_brick):
                ball.muuta_y_suunta()
                field.poista_tiili(hitted_brick)
                pelaaja.lisaa_piste()
            elif ball.osuu_vasempaan_ylanurkkaan(hitted_brick):
                ball.muuta_x_suunta()
                ball.muuta_y_suunta()
                field.poista_tiili(hitted_brick)
                pelaaja.lisaa_piste()
            elif ball.osuu_oikeaan_ylanurkkaan(hitted_brick):
                ball.muuta_x_suunta()
                ball.muuta_y_suunta()
                field.poista_tiili(hitted_brick)
                pelaaja.lisaa_piste()
            elif ball.osuu_oikeaan_alanurkkaan(hitted_brick):
                ball.muuta_x_suunta()
                ball.muuta_y_suunta()
                field.poista_tiili(hitted_brick)
                pelaaja.lisaa_piste()
            elif ball.osuu_vasempaan_alanurkkaan(hitted_brick):
                ball.muuta_x_suunta()
                ball.muuta_y_suunta()
                field.poista_tiili(hitted_brick)
                pelaaja.lisaa_piste()



        naytto.fill((0,0,0))
        field.piirra()
        pelaaja.nayta_pisteet()
        ball.liiku()

        if ball.pois_pelista():
            running = False

        pygame.display.flip()
        kello.tick(60)