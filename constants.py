import pygame
import os

SPEED = 1
SCORE = 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
GAME_STATE = "menu"

# set colors
RED = (255, 0, 0)
BLUE = (70, 170, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 0, 150)
GOLD = (200, 200, 50)

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
pygame.mixer.music.set_volume(.5)
pygame.mixer.music.play(-1)
whoosh = [
    pygame.mixer.Sound(os.path.join("assets", "sounds", "whoosh_1.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "whoosh_2.mp3"))
]
rainbow = [
    pygame.image.load(os.path.join("assets", "rainbow1_40.png")),
    pygame.image.load(os.path.join("assets", "rainbow2_40.png")),
    pygame.image.load(os.path.join("assets", "rainbow3_40.png")),
]
rainbow[1].set_colorkey(WHITE)
heart = pygame.image.load(os.path.join("assets", "heart.png"))
heart.set_colorkey(WHITE)
dash_talk = [
    pygame.mixer.Sound(os.path.join("assets", "sounds", "10-seconds.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "dangers-my.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "here-we-go.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "iron-pony.mp3")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "snack-time.mp3")),
]
for sound in dash_talk:
    sound.set_volume(.8)
pinkie_talk = pygame.mixer.Sound(
    os.path.join("assets", "sounds", "eye-in-sky.mp3")
)
ouch = pygame.mixer.Sound(os.path.join("assets", "sounds", "ouch.mp3"))
all_sounds = [
    whoosh,
    dash_talk,
    pinkie_talk,
    ouch,
]
