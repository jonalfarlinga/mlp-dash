import pygame
from random import randint, choice
from math import sqrt, ceil
from constants import *  # noqa
import os


def randStart():
    x = randint(100, SCREEN_WIDTH - 300)
    y = randint(100, SCREEN_HEIGHT - 200)

    if SCREEN_HEIGHT // 2 - 100 < y < SCREEN_HEIGHT // 2 + 100:
        y += 200

    if SCREEN_WIDTH // 2 - 50 < x < SCREEN_WIDTH // 2 + 50:
        x += 200
    return x, y


# define Cloud Sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "cloud.png"))
        self.image.set_colorkey((WHITE))
        self.rect = self.image.get_rect()
        self.rect.center = (randStart())
        self.direction = [choice((-1, 1)), choice((-1, 1))]
        self.pop = -1

    # turns into a cloudburst, and starts the kill timer at 3
    def burst(self):
        self.pop = 3
        self.image = pygame.image.load(os.path.join("assets", "cloud_pop.png"))
        self.image.set_colorkey(WHITE)
        choice(whoosh).play()

    # kills a cloudburst after 3 loops, or moves a cloud randomly, turning away
    # from edges
    def move(self):
        if self.pop > 0:
            self.pop -= 1
        elif self.pop == 0:
            self.kill()
        else:
            turn = randint(0, 20)
            if turn > 19:
                self.direction = [choice((-1, 1)), choice((-1, 1))]
            if self.rect.bottom > SCREEN_HEIGHT:
                self.direction[1] = -1
            if self.rect.right > SCREEN_WIDTH:
                self.direction[0] = -1
            if self.rect.left < 0:
                self.direction[0] = 1
            if self.rect.top < 0:
                self.direction[1] = 1
            vector = (randint(0, SPEED * 2) * self.direction[0],
                      randint(0, SPEED * 2) * self.direction[1],
                      )

            self.rect.move_ip(vector)


class Changeling(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join("assets", "changeling.png")
        )
        self.image.set_colorkey((WHITE))
        self.rect = self.image.get_rect()
        self.rect.center = (randStart())
        self.direction = [choice((-1, 1)), choice((-1, 1))]
        self.pop = -1

    # kills a cloudburst after 3 loops, or moves a cloud randomly, turning away
    # from edges
    def move(self):
        if self.pop > 0:
            self.pop -= 1
        elif self.pop == 0:
            self.kill()
        else:
            turn = randint(0, 20)
            if turn > 39:
                self.direction = [choice((-1, 1)), choice((-1, 1))]
            if self.rect.bottom > SCREEN_HEIGHT:
                self.direction[1] = -1
            if self.rect.right > SCREEN_WIDTH:
                self.direction[0] = -1
            if self.rect.left < 0:
                self.direction[0] = 1
            if self.rect.top < 0:
                self.direction[1] = 1
            vector = (randint(0, SPEED * 2) * self.direction[0],
                      randint(0, SPEED * 2) * self.direction[1],
                      )

            self.rect.move_ip(vector)

    def hit(self, player):
        self.pop = 3
        self.image = pygame.image.load(os.path.join("assets", "cloud_pop.png"))
        self.image.set_colorkey(WHITE)
        player.hit()


# define Dash sprite
class Dash(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.im = 0
        self.image = rainbow[self.im]
        self.image.set_colorkey((WHITE))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.lurex = SCREEN_WIDTH // 2
        self.lurey = SCREEN_HEIGHT // 2
        self.health = 3

    def hud(self, screen):
        x = 25
        for i in range(self.health):
            screen.blit(heart, (x, SCREEN_HEIGHT - 100))
            x += 45

    # rotates the Dash image
    def step(self):
        self.im += 1
        if self.im == len(rainbow):
            self.im = 0
        self.image = rainbow[self.im]

    # moves Dash along x and y at 20px per tick.
    def move(self):
        # Function to calculate distance between two points
        x = (self.rect.centerx - self.lurex) ** 2
        y = (self.rect.centery - self.lurey) ** 2
        distance = sqrt(x + y) / 10

        # Calculate the direction vector
        direction_x = self.lurex - self.rect.centerx
        direction_y = self.lurey - self.rect.centery

        # Normalize the direction vector (convert it to a unit vector)
        if distance > 3:
            direction_x /= distance
            direction_y /= distance
            # Calculate the travel distance for this turn
            travel_x = ceil(direction_x) * 2
            travel_y = ceil(direction_y) * 2
        else:
            travel_x = 0
            travel_y = 0
        self.rect.move_ip((travel_x, travel_y))

    def talk(self):
        choice(dash_talk).play()

    def hit(self):
        self.health -= 1

    def target(self, x, y):
        self.lurex = x
        self.lurey = y


class Pinkie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(
                "assets",
                "pinkie_balloons_160.png"
            )
        )
        self.image.set_colorkey((WHITE))
        self.rect = self.image.get_rect()
        self.rect.center = (
            SCREEN_WIDTH - 200,
            SCREEN_HEIGHT
        )
        self.direction = [0, -1]

    # moves Pinkie up until she floats off screen.
    def move(self):
        self.rect.move_ip(0, SPEED * self.direction[1])
        if self.rect.bottom < -100:
            self.kill()
