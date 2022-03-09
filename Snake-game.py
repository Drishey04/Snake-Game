import pygame
import random
import os
import sys

pygame.mixer.init()

pygame.init()

# Colors
white = (255, 255, 255)
red = (207, 39, 39)
black = (40, 41, 52)
yellow = (246, 165, 24)
green = (15, 252, 9)
game_page_color = (40, 133, 172)
game_over_color = ()

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))


# Game Title
pygame_icon = pygame.image.load("logo.png")
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Snakes game")
pygame.display.update()

clock = pygame.time.Clock()


def text_screen(text, given_font, color, x, y, size):
    font = pygame.font.SysFont(f"{given_font}", size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.circle(gameWindow, black, (x, y), snake_size, snake_size)


# Welcome page
def welcome():
    pygame.mixer.music.load('welcome-page.mp3')
    pygame.mixer.music.play()
    exit_game = False

    while not exit_game:
        gameWindow.fill((233, 220, 222))
        welcome_img = pygame.image.load("welcome-page.png")
        welcome_img = pygame.transform.scale(welcome_img, (screen_width, screen_height)).convert_alpha()
        gameWindow.blit(welcome_img, (0, 0))
        text_screen("Press Space Bar To Play", "INICIAR", black, 230, 290, 55)
        text_screen("Created by: Drishey Singh", "Comic Sans MS", black, 270, 550, 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0

    food_x = random.randint(200, screen_width / 2)
    food_y = random.randint(100, screen_height / 2)
    score = 0
    init_velocity = 5
    food_size = 15
    snake_size = 15
    fps = 60
    snake_list = []
    snake_length = 1

    pygame.mixer.music.load('game-page.mp3')
    pygame.mixer.music.play()
    game_page_img = pygame.image.load("welcome-page.png")
    game_page_img = pygame.transform.scale(game_page_img, (screen_width, screen_height)).convert_alpha()
    gameWindow.blit(game_page_img, (0, 0))

    # check if high_score file exists
    if not os.path.exists("high_score.txt"):
        with open("high_score.txt", "w") as f:
            f.write("0")

    with open("high_score.txt", 'r') as f:
        high_score = f.read()

    while not exit_game:

        if game_over:
            gameWindow.fill(red)
            text_screen("Game Over!", "dengxian", black, 265, 100, 100)
            text_screen(f"Your Score: {score}", "dengxian", black, 370, 250, 50)
            text_screen(f"Highest Score: {high_score}", "dengxian", black, 340, 300, 50)
            text_screen("Press Enter to Continue", "dengxian", black, 320, 450, 40)

            with open("high_score.txt", 'w') as f:
                f.write(str(high_score))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 20

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snake_length += 5
                if score > int(high_score):
                    high_score = score

            gameWindow.fill(game_page_color)

            text_screen("Score: " + str(score) + "  Highest Score: " + str(high_score), "Arial", yellow, 5, 5, 35)
            pygame.draw.circle(gameWindow, green, (food_x, food_y), food_size, food_size)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                gameWindow.fill(red)
                pygame.mixer.music.load('game-over.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                gameWindow.fill(red)
                pygame.mixer.music.load('game-over.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


welcome()
