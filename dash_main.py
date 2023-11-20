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

# load and set the logo and headline
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
pinkie_talk = pygame.mixer.Sound(
    os.path.join("assets", "sounds", "eye-in-sky.mp3")
)
SPEED = 1
SCORE = 0
font = pygame.font.SysFont("Arial", 60)
welcome = font.render("Welcome", True, BLUE)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.FULLSCREEN
)
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


# define Dash sprite
class Dash(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.im = 0
        self.image = rainbow[self.im]
        self.image.set_colorkey((WHITE))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.lurex = SCREEN_WIDTH//2
        self.lurey = SCREEN_HEIGHT//2

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
            SCREEN_WIDTH-200,
            SCREEN_HEIGHT
        )
        self.direction = [0, -1]

    # moves Pinkie up until she floats off screen.
    def move(self):
        self.rect.move_ip(0, SPEED * self.direction[1])
        if self.rect.bottom < -100:
            self.kill()


# Setting up Sprites
P1 = Dash()
E1 = Cloud()

# Creating Sprites Groups
clouds = pygame.sprite.Group()
clouds.add(E1)
ponies = pygame.sprite.Group()
ponies.add(P1)

# initialize User Events
NEW_CLOUD = pygame.USEREVENT + 1
PINKIE_FLOAT = pygame.USEREVENT + 2
pygame.time.set_timer(NEW_CLOUD, 1000)
pygame.time.set_timer(PINKIE_FLOAT, 30000)


"""
"""


# define a main function
def main():
    pygame.display.flip()

    # main loop
    while True:
        global SCORE
        screen.fill(BLUE)

        # updates Dash's target as long as mousebutton is pressed
        if pygame.mouse.get_pressed()[0]:
            P1.lurex = pygame.mouse.get_pos()[0]
            P1.lurey = pygame.mouse.get_pos()[1]

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == NEW_CLOUD and len(clouds) < 10:
                clouds.add(Cloud())
            if event.type == PINKIE_FLOAT and len(ponies) < 2:
                ponies.add(Pinkie())
                pinkie_talk.play()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # check for Dash colliding with clouds
        for sprite in pygame.sprite.spritecollide(P1, clouds, False):
            if sprite.pop == -1:
                sprite.burst()
                if randint(1, 10) == 10:
                    P1.talk()
                SCORE += 1

        # move and blit all sprites
        for sprite in clouds:
            sprite.move()
            screen.blit(sprite.image, sprite.rect.center)
        for sprite in ponies:
            sprite.move()
            screen.blit(sprite.image, sprite.rect.center)

        # blit score and update display
        score = font.render(str(SCORE), True, BLACK)
        screen.blit(score, (25, 25))

        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    # call the main function
    main()
