# import the pygame module, so you can use it
import pygame
import os
import sys
from random import randint
from math import sqrt

# initialize the pygame module
pygame.init()

# Setting up FPS
FPS = 24
FramePerSec = pygame.time.Clock()

# load and set the logo
logo = pygame.image.load(os.path.join("assets", "pinky_logo.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Rainbow's Dash!")
rainbow = [
    pygame.image.load(os.path.join("assets", "rainbow1_40.png")),
    pygame.image.load(os.path.join("assets", "rainbow2_40.png")),
    pygame.image.load(os.path.join("assets", "rainbow3_40.png")),
]

# set colors
BLUE = (70, 170, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BLUE)

SPEED = 1
font = pygame.font.SysFont("Broadway", 60)
welcome = font.render("Welcome", True, BLUE)


# create sprites
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "cloud.png"))
        self.image.set_colorkey((WHITE))
        self.rect = self.image.get_rect()
        self.rect.center = (
            randint(100, SCREEN_WIDTH-100),
            randint(100, SCREEN_HEIGHT-100)
        )
        self.age = 0

    def move(self):
        global SCORE
        self.age += 1
        if self.age == 3:
            vector = (randint(0, SPEED * 2) - SPEED,
                      randint(0, SPEED * 2) - SPEED,
                      )
            self.rect.move_ip(vector)
            if (self.rect.bottom > SCREEN_HEIGHT or
               self.rect.right > SCREEN_WIDTH or
               self.rect.left < 0 or
               self.rect.top < 0):
                self.kill()
            self.age = 0


# create sprites
class Dash(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.im = 0
        self.image = rainbow[self.im]
        self.image.set_colorkey((WHITE))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.lure = (200, 200)

    def move(self):
        # Function to calculate distance between two points
        x = (self.rect.centerx - self.lure[0]) ** 2
        y = (self.rect.centery - self.lure[1]) ** 2
        dist = sqrt(x + y)
        # Calculate the direction vector
        direction_x = self.lure[0] - self.rect.center[0]
        direction_y = self.lure[1] - self.rect.center[1]

        # Normalize the direction vector (convert it to a unit vector)
        if dist > 2:
            direction_x /= dist
            direction_y /= dist

        # Calculate the travel distance for this turn
        travel_x = int(direction_x * SPEED)
        travel_y = int(direction_y * SPEED)
        self.rect.move_ip((travel_x, travel_y))


# Setting up Sprites
P1 = Dash()
E1 = Cloud()

# Creating Sprites Groups
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

NEW_CLOUD = pygame.USEREVENT + 1
pygame.time.set_timer(NEW_CLOUD, 1000)


# define a main function
def main():
    pygame.display.flip()

    # main loop
    while True:
        screen.fill(BLUE)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                P1.lure = pygame.mouse.get_pos()
            # only do something if the event is of type QUIT
            if event.type == NEW_CLOUD and len(all_sprites) < 10:
                all_sprites.add(Cloud())
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for sprite in all_sprites:
            sprite.move()
            screen.blit(sprite.image, sprite.rect.center)
        lure = font.render(str(P1.lure), True, BLACK)
        P1pos = font.render(str(P1.rect.center), True, BLACK)
        screen.blit(lure, (25, 25))
        screen.blit(P1pos, (25, 100))

        pygame.display.update()
        FramePerSec.tick(FPS)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
