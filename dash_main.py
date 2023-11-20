# import the pygame module, so you can use it
import pygame
import os
import sys
from random import randint, choice
from math import sqrt, ceil

# initialize the pygame module
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(
    os.path.join(
        "assets",
        "sounds",
        "playful-140946.mp3"
        )
    )
pygame.mixer.music.play(-1)

# Setting up FPS
FPS = 30
FramePerSec = pygame.time.Clock()

# set colors
BLUE = (70, 170, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# load and set the logo
logo = pygame.image.load(os.path.join("assets", "pinky_logo.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Rainbow's Dash!")

# initialize assets
rainbow = [
    pygame.image.load(os.path.join("assets", "rainbow1_40.png")),
    pygame.image.load(os.path.join("assets", "rainbow2_40.png")),
    pygame.image.load(os.path.join("assets", "rainbow3_40.png")),
]
rainbow[1].set_colorkey(WHITE)
whoosh = [
    pygame.mixer.Sound(os.path.join("assets", "sounds", "whoosh_1.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "whoosh_2.mp3"))
]
dash_talk = [
    pygame.mixer.Sound(os.path.join("assets", "sounds", "10-seconds.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "dangers-my.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "here-we-go.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "iron-pony.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "snack-time.mp3")),
]
SPEED = 1
SCORE = 0
font = pygame.font.SysFont("Broadway", 60)
welcome = font.render("Welcome", True, BLUE)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(BLUE)


# define Cloud Sprite
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
        self.direction = [choice((-1, 1)), choice((-1, 1))]
        self.pop = -1

    def burst(self):
        self.pop = 3
        self.image = pygame.image.load(os.path.join("assets", "cloud_pop.png"))
        self.image.set_colorkey(WHITE)
        choice(whoosh).play()

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


# define Dash sprite
class Dash(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.im = 0
        self.image = rainbow[self.im]
        self.image.set_colorkey((WHITE))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.lure = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

    def step(self):
        self.im += 1
        if self.im == len(rainbow):
            self.im = 0
        self.image = rainbow[self.im]

    def move(self):
        # Function to calculate distance between two points
        x = (self.rect.centerx - self.lure[0]) ** 2
        y = (self.rect.centery - self.lure[1]) ** 2
        dist = sqrt(x + y)
        dist /= 10

        # Calculate the direction vector
        direction_x = self.lure[0] - self.rect.center[0]
        direction_y = self.lure[1] - self.rect.center[1]

        # Normalize the direction vector (convert it to a unit vector)
        if dist > 3:
            direction_x /= dist
            direction_y /= dist
            # Calculate the travel distance for this turn
            travel_x = ceil(direction_x) * 2
            travel_y = ceil(direction_y) * 2
        else:
            travel_x = 0
            travel_y = 0
        self.rect.move_ip((travel_x, travel_y))

    def talk(self):
        choice(dash_talk).play()


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
        global SCORE
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
        for sprite in pygame.sprite.spritecollide(P1, all_sprites, False):
            if sprite != P1 and sprite.pop == -1:
                sprite.burst()
                if randint(1, 10) == 10:
                    P1.talk()
                SCORE += 1

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
