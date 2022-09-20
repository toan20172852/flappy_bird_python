# link guideline code game: https://www.youtube.com/watch?v=mFbdfXWmLU8

from math import floor
from tkinter import CENTER
import pygame
import sys
import random

#function create two floor run in screen
def draw_floor():
    screen.blit(floor,(floor_x_pos,650)) #floor 1
    screen.blit(floor,(floor_x_pos+432,650)) #floor 2, floor 2 next to floor 1

#function create pipe
def create_pipe():
    random_pipe_pos = random.choice(pipe_height) #create random pipe position with size random
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos)) #create bottom pipe
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos-650)) #create top pipe, random_pipe_pos - X is create space for bird fly
    return bottom_pipe, top_pipe

#function move pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

#function draw pipe
def draw_pipe(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface, pipe)
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) #reverse pipe if it is top_pipe, and overturn OY
            screen.blit(flip_pipe, pipe)

#function prosess collision
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): #bird collision with pipe
            hit_sound.play() #when bird to pipe then play audio
            swooshing_sound.play()
            die_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650: #bird fly over window game or bird in floor
            return False
    return True

#function annimation rotate bird
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3, 1) #rotate bird for bird_movement
    return new_bird

#function animation bird flap
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

#function display score in screen 
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        #display score when game over
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)        

        #display high score
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 0, 0))
        high_score_rect = high_score_surface.get_rect(center = (216, 630))
        screen.blit(high_score_surface, high_score_rect)

#function update score
def update_score(score, high_score):
    if score >= high_score:
        high_score = score
    return high_score

#function init
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

#create black window
screen= pygame.display.set_mode((432,768))

#set FPS for game
clock = pygame.time.Clock()

#create gravity for game
gravity = 0.25

#set position start of bird
bird_movement = 0

#game_active to stop or play
game_active = True

#import font character to game
game_font = pygame.font.Font('FileGame/04B_19.ttf', 40) #name of font and size of character

#create score
score = 0
high_score = 0

#create background for game
bg = pygame.image.load('FileGame/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg) #full screen black window

#create floor for game
floor = pygame.image.load('FileGame/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor) #full screen black window
#create local start of birst when start
floor_x_pos = 0

#create bird
bird_down = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-downflap.png').convert_alpha()) #covert_alpha() don't have black around
bird_mid = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up] #list status of bird
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100, 384))

#create timer for bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200) #after 200ms bird flap

#insert audio flap
flap_sound = pygame.mixer.Sound('FileGame/sound/sfx_wing.wav') #audio bird fly
hit_sound = pygame.mixer.Sound('FileGame/sound/sfx_hit.wav') #audio bird to pipe
score_sound = pygame.mixer.Sound('FileGame/sound/sfx_point.wav') #audio increate score
die_sound = pygame.mixer.Sound('FileGame/sound/sfx_die.wav') #audio bird die
swooshing_sound = pygame.mixer.Sound('FileGame/sound/sfx_swooshing.wav') #audio bird swooshing when to pipe
score_sound_countdown = 100

#create screen finish
game_over_surface = pygame.transform.scale2x(pygame.image.load('FileGame/assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216, 384))

#create piple
pipe_surface = pygame.image.load('FileGame/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface) #full screen black window
pipe_list = [] #list contain all pipe was created

#create timer for game when play to spaw pipe
spawnpipe = pygame.USEREVENT #auto create new pipe when play
pygame.time.set_timer(spawnpipe, 1200) #after 1200ms then create new pipe in game

#create list save for pipe
pipe_height = [200, 300, 400] #create list size of pipe

#main loop of game
while True:
    for event in pygame.event.get():

        #create event then press keyboard to exit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #event help bird fly when press "Space"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -11 #bird fly up
                flap_sound.play() #run audio
            if event.key == pygame.K_SPACE and game_active == False:
                game_active=True
                pipe_list.clear() #reset game after loss and start again
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0 #reset score after restar game

        #event create pipe when play
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe()) #append() get one return, extend() get two return
        
        #event bird flap
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation() #animation bird flap
            
    screen.blit(bg,(0,0)) #insert backgroud to black window

    if game_active:
        #bird
        bird_movement += gravity #when bird move then bird down
        rotated_bird = rotate_bird(bird) #rotate bird
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect) #insert bird to black window
        game_active = check_collision(pipe_list) #event bird collision with pipe

        #pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01 #increate score
        score_display('main game')
        score_sound_countdown -= 1

        #when increate score
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100

    else: #finish
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game over')
    
    #floor
    floor_x_pos -= 1 #posion to left of screen
    draw_floor()
    #reset position of birst when run over with of screen
    if floor_x_pos <= -432:
        floor_x_pos = 0
    
    pygame.display.update() #after quit must update sate of game
    clock.tick(100) #alignment timer in game
