# import the pygame module, so you can use it
import pygame
import os
import sys
from random import randint
from constants import *  # noqa
from entities import Dash, Cloud, Pinkie, Changeling


# Setting up FPS
FPS = 30
FramePerSec = pygame.time.Clock()

# load and set the logo and headline
logo = pygame.image.load(os.path.join("assets", "pinky_logo.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Rainbow's Dash!")

# initialize assets
font = pygame.font.SysFont("Arial", 60)
welcome = font.render("Welcome", True, BLACK)

# create a surface on screen that has the set size
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    # pygame.FULLSCREEN
)
screen.fill(BLUE)

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
pygame.time.set_timer(NEW_CLOUD, 500)
pygame.time.set_timer(PINKIE_FLOAT, 30000)


"""
"""


# define a main function
def main():
    global GAME_STATE
    while True:
        pygame.display.flip()
        match GAME_STATE:
            case "menu":
                # menu loop
                menu()
            case "play":
                # main loop
                game()
            case "dead":
                # dead loop
                dead()
            case "win":
                # win loop
                win()


def menu():
    global GAME_STATE
    go_button = pygame.Surface((200, 100))
    go_button.fill(PINK)
    go_button.blit(font.render("Play!", True, BLACK), (40, 15))
    go_button_rect = go_button.get_rect()
    go_button_rect.topleft = (
        SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50
    )

    while GAME_STATE == "menu":
        screen.fill(BLUE)
        screen.blit(welcome, (SCREEN_WIDTH // 2 - 100, 100))
        screen.blit(
            go_button,
            (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.mouse.get_pressed()[0]:
            if go_button_rect.collidepoint(pygame.mouse.get_pos()):
                GAME_STATE = "play"
                pygame.time.wait(50)
        pygame.display.update()
        FramePerSec.tick(FPS)
        pygame.time.wait(1)


def game():
    global GAME_STATE
    global SCORE
    SCORE = 0
    # Setting up Sprites
    P1 = Dash()
    # Creating Sprites Groups
    ponies = pygame.sprite.Group()
    ponies.add(P1)
    clouds = pygame.sprite.Group()
    for i in range(8):
        clouds.add(Cloud())
    enemies = pygame.sprite.Group()
    for i in range(3):
        enemies.add(Changeling())

    # initialize User Events
    NEW_CLOUD = pygame.USEREVENT + 1
    PINKIE_FLOAT = pygame.USEREVENT + 2
    pygame.time.set_timer(NEW_CLOUD, 3000)
    pygame.time.set_timer(PINKIE_FLOAT, 25000)

    while GAME_STATE == "play":
        screen.fill(BLUE)

        # updates Dash's target as long as mousebutton1 is pressed
        if pygame.mouse.get_pressed()[0]:
            P1.target(
                pygame.mouse.get_pos()[0],
                pygame.mouse.get_pos()[1],
            )

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == NEW_CLOUD and len(clouds) < 20:
                for i in range(5):
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

        # check for Dash colliding with enemies
        for sprite in pygame.sprite.spritecollide(P1, enemies, False):
            sprite.hit(P1)
            # change the enemy to the clouds group to stop causing hits.
            enemies.remove(sprite)
            clouds.add(sprite)

        # move and blit all sprites
        for sprite in enemies:
            sprite.move()
            screen.blit(sprite.image, sprite.rect.center)
        for sprite in clouds:
            sprite.move()
            screen.blit(sprite.image, sprite.rect.center)
        for sprite in ponies:
            sprite.move()
            screen.blit(sprite.image, sprite.rect.center)

        # blit score and update display
        score = font.render(str(SCORE), True, BLACK)
        screen.blit(score, (25, 25))
        P1.hud(screen)

        if P1.health < 1:
            GAME_STATE = "dead"
        elif SCORE > 19:
            GAME_STATE = 'win'
        else:
            GAME_STATE = "play"

        pygame.time.wait(1)
        pygame.display.update()
        FramePerSec.tick(FPS)


def dead():
    global GAME_STATE
    yDrop = -100
    go_button = pygame.Surface((300, 100))
    go_button.fill(RED)
    go_button.blit(font.render("OH NO!", True, GOLD), (40, 15))
    go_button_rect = go_button.get_rect()
    go_button_rect.topleft = (
        SCREEN_WIDTH // 2 - 150, yDrop
    )

    while GAME_STATE == "dead":
        if yDrop < SCREEN_HEIGHT // 2 - 50:
            yDrop += 20
        screen.fill(BLUE)
        screen.blit(
            go_button,
            (SCREEN_WIDTH // 2 - 150, yDrop)
        )
        go_button_rect.topleft = (SCREEN_WIDTH // 2 - 150, yDrop)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.mouse.get_pressed()[0]:
            if go_button_rect.collidepoint(pygame.mouse.get_pos()):
                GAME_STATE = "menu"
                screen.fill(BLUE)
                pygame.display.update()
                pygame.time.wait(500)
        pygame.display.update()
        FramePerSec.tick(FPS)
        pygame.time.wait(1)


def win():
    global GAME_STATE
    go_button = pygame.Surface((300, 100))
    go_button.fill(GOLD)
    go_button.blit(font.render("You Win!", True, BLACK), (40, 15))
    go_button_rect = go_button.get_rect()
    go_button_rect.topleft = (
        SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50
    )

    while GAME_STATE == "win":
        screen.fill(BLUE)
        screen.blit(
            go_button,
            (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.mouse.get_pressed()[0]:
            if go_button_rect.collidepoint(pygame.mouse.get_pos()):
                GAME_STATE = "play"
                screen.fill(BLUE)
                pygame.display.update()
                pygame.time.wait(500)
        pygame.display.update()
        FramePerSec.tick(FPS)
        pygame.time.wait(1)


if __name__ == "__main__":
    # call the main function
    main()
