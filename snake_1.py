"""
Wormy (a Nibbles clone)
By Al Sweigart al@inventwithpython.com
http://inventwithpython.com/pygame
Released under a "Simplified BSD" license
Modifications by Valdemar Svabensky valdemar@mail.muni.cz
"""

import pygame, sys, random
from pygame.locals import *
pygame.init()

#main content
FPS = 10
WINDOWWIDTH = 680
WINDOWHEIGHT = 420
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, 'Window width must be a multiple of cell size.'
assert WINDOWHEIGHT % CELLSIZE == 0, 'Window height must be a multiple of cell size.'
NUM_CELLS_X = None  # TODO
NUM_CELLS_Y = None  # TODO

#colors
BGCOLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)

# No other constants go here!
BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
CLOCK = pygame.time.Clock()
LOSE = 0
MUTE = 0


def main(): #main function
    global LOSE
    count = 0
    while True: #program loop
        get_new_snake()
        get_random_location()
        while LOSE == 0: # start screen loop
            if was_key_pressed() and LOSE == 0: #repaint window
                DISPLAYSURF.fill(BGCOLOR)
                LOSE = 1
            else: # start screen
                wait_for_key_pressed() 
                show_start_screen()
                mute()
        while LOSE == 1: #game loop
            if count == 0:  #play music on the start of round 
                song() 
            print(direction)
            was_key_pressed()
            run_game()
            wall_colosion()
            head_colision()
            apple_colision()
            draw_game_state(snake)
            DISPLAYSURF.fill(BGCOLOR)
            CLOCK.tick(FPS)

            count += 1
        while LOSE == 2:# screen on the end
            music_stop()
            show_game_over_screen() 
            restart()
            CLOCK.tick(FPS)   
                        

def terminate():
    """Exit the program."""
    sys.exit()

def restart(): #wait and restart program after lose
    global LOSE
    pygame.time.wait(1000)
    if was_key_pressed(): 
        LOSE = 1
        main()

def was_key_pressed():
    """Exit game on QUIT event, or return True if key was pressed."""
    global direction, MUTE
    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            terminate()
        # movement keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != "down":
                direction = "up"
                
            if event.key == pygame.K_a and direction != "right":
                direction = "left"
               
            if event.key == pygame.K_s and direction != "up":
                direction = "down"
                
            if event.key == pygame.K_d and direction != "left":
                direction = "right"
            # easter egg
            if event.key == pygame.K_o:
                addHead()
            #mute and play music
            if event.key == pygame.K_m:
                MUTE += 1
                if MUTE % 2 == 0: # counting if person want play or mute song
                    song()
                else: 
                    music_stop()
            #esc
            if event.key==pygame.K_ESCAPE:
                terminate()
        
            return True

        else:

            return False

def wait_for_key_pressed():
    """Wait for a player to press any key."""
    msg_surface = BASICFONT.render('Press a key to play', True, GRAY)
    msg_rect = msg_surface.get_rect()
    msg_rect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(msg_surface, msg_rect)
    pygame.display.update()


def show_start_screen():
    """Show a welcome screen at the first start of the game. (Do not modify.)"""
    title_font = pygame.font.Font('freesansbold.ttf', 80)
    title_surface = title_font.render('Snake!', True, WHITE)
    title_rect = title_surface.get_rect()
    title_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(title_surface, title_rect)

def mute():
    # text on start screen
    global MUTE 
    mute_surface = BASICFONT.render('Press M to mute', True, GRAY)
    mute_rect = mute_surface.get_rect()
    mute_rect.topleft =  (WINDOWWIDTH - 660, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(mute_surface, mute_rect)


def show_game_over_screen():
    """Show a game over screen when the player loses. (Do not modify.)"""
    game_over_font = pygame.font.Font('freesansbold.ttf', 120)
    game_surface = game_over_font.render('Game', True, WHITE)
    over_surface = game_over_font.render('Over', True, WHITE)
    game_rect = game_surface.get_rect()
    over_rect = over_surface.get_rect()
    game_rect.midtop = (WINDOWWIDTH / 2, 10)
    over_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 10 + 25)

    DISPLAYSURF.blit(game_surface, game_rect)
    DISPLAYSURF.blit(over_surface, over_rect)
    score()
    wait_for_key_pressed()

def score():
    score_surface = BASICFONT.render('Your score: ' + str(len(snake) - 3 ), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft =  (WINDOWWIDTH - 660, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(score_surface, score_rect)


def get_new_snake():
    """Set a random start point for a new snake and return its coordinates."""
    global direction, snake, X_start, Y_start
    X = [x for x in range(40, WINDOWWIDTH - 80, 20)] #multiplier list 20
    Y = [y for y in range(40,WINDOWHEIGHT  - 80, 20)]#multiplier list 20
    X_start = random.choice(X)#random multiplier of 20
    Y_start = random.choice(Y)#random multiplier of 20
    direction = "right"
    snake = [[X_start, Y_start], [X_start - 20, Y_start], [X_start - 40, Y_start]] #first 3 cells of snake

def get_random_location():
    #random lacation for apple
    global X_random, Y_random
    X = [x for x in range(20, WINDOWWIDTH - 20, 20)] 
    Y = [y for y in range(20, WINDOWHEIGHT  - 20, 20)] 
    X_random = random.choice(X)
    Y_random = random.choice(Y)
    
def addHead():
    #add cell 
    global snake, X_start, Y_start
    snake.insert(len(snake), [X_start, Y_start])

def move():
    #new coordinates for movement
    global direction, snake, X_start, Y_start

    snake.pop()

    if direction == "up":
        Y_start -= 20
    if direction == "left":
        X_start -= 20
    if direction == "down":
        Y_start += 20
    if direction == "right":
        X_start += 20

    snake.insert(0, [X_start, Y_start])

def grid():
    #draw grid
    DISPLAYSURF.fill(BGCOLOR)
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # Draw vertical lines
        pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # Draw horizontal lines
        pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))

def run_game():
    """Main game logic. Return on game over."""
    move()
    grid()

    for i in range(len(snake)):# draw every cell of snake 

        pygame.draw.rect(DISPLAYSURF, GREEN, (snake[i][0], snake[i][1], CELLSIZE, CELLSIZE))

    apple = pygame.draw.rect(DISPLAYSURF, RED, (X_random, Y_random,CELLSIZE, CELLSIZE))#draw apple

    print(snake)

def head_colision(): #detect if snake hit his body 
    global LOSE
    for i in range(1,len(snake)):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            LOSE = 2

def apple_colision():#detect if snake hit apple
    if snake[0][0] == X_random and snake[0][1] == Y_random:
        get_random_location()       
        addHead()


def wall_colosion():#detect if snake hit wall
    global LOSE
    if X_start == WINDOWWIDTH or X_start == -20:
        LOSE = 2
    if Y_start == WINDOWHEIGHT or Y_start == -20:
        LOSE = 2


def draw_game_state(snake):
    """Draw the contents on the screen. (Do not modify.)"""

    score_surface = BASICFONT.render('Score: ' + str(len(snake) - 3), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(score_surface, score_rect)
    pygame.display.update()

def song(): #play song
    track = "./song.mp3"
    pygame.mixer.music.load(track)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)

def music_stop(): #stop song
    pygame.mixer.music.stop()


if __name__ == '__main__':
    main()

