import pygame
import button

#create display window
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Button Demo')

#load button images
start_img = pygame.image.load('start_btn.png').convert_alpha()
start_hover_img = pygame.image.load('start_hover_btn.png').convert_alpha()
start_clicked_img = pygame.image.load('start_clicked_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()
exit_hover_img = pygame.image.load('exit_hover_btn.png').convert_alpha()
exit_clicked_img = pygame.image.load('exit_clicked_btn.png').convert_alpha()

start_button = button.Button(350, 250, start_img, start_hover_img, start_clicked_img, 0.8)
exit_button = button.Button(700, 250, exit_img, exit_hover_img, exit_clicked_img, 0.8)

#game loop
run = True
while run:

    screen.fill((202, 228, 241))
    start_button.update(screen)
    if start_button.is_clicked():
        print('START')
    exit_button.update(screen)
    if exit_button.is_clicked():
        print('EXIT')

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
