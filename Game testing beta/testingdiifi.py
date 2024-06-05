import pygame
from pygame.locals import *

pygame.init()

# Load button images
play_again_img = pygame.image.load("start_btn.png")
play_again_img_hover = pygame.image.load("start_hover_btn.png")
play_again_img_clicked = pygame.image.load("start_clicked_btn.png")

quit_img = pygame.image.load("exit_btn.png")
quit_img_hover = pygame.image.load("exit_hover_btn.png")
quit_img_clicked = pygame.image.load("exit_clicked_btn.png")

# Load difficulty button images
easy_img = pygame.image.load("easy_btn.png")
easy_img_hover = pygame.image.load("easy_btn_hover.png")
easy_img_clicked = pygame.image.load("easy_btn_clicked.png")

medium_img = pygame.image.load("medium_btn.png")
medium_img_hover = pygame.image.load("medium_btn_hover.png")
medium_img_clicked = pygame.image.load("medium_btn_clicked.png")

hard_img = pygame.image.load("hard_btn.png")
hard_img_hover = pygame.image.load("hard_btn_hover.png")
hard_img_clicked = pygame.image.load("hard_btn_clicked.png")

# Load background image and resize it to screen size
bg_img = pygame.image.load("background.jpg")
bg_img = pygame.transform.scale(bg_img, (1280, 720))

# Load background music
pygame.mixer.music.load("bg_music.wav")

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Button Demo')

font = pygame.font.SysFont('Constantia', 30)

#define colours
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

#define global variable
clicked = False
counter = 0
difficulty = None

class button():

    def __init__(self, x, y, normal_img, hover_img, clicked_img):
        self.x = x
        self.y = y
        self.normal_img = normal_img
        self.hover_img = hover_img
        self.clicked_img = clicked_img

    def draw_button(self):

        global clicked
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #create pygame Rect object for the button
        button_rect = self.normal_img.get_rect(topleft = (self.x, self.y))

        #check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                screen.blit(self.clicked_img, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                screen.blit(self.hover_img, button_rect)
        else:
            screen.blit(self.normal_img, button_rect)

        return action

easy_button = button(350, 250, easy_img, easy_img_hover, easy_img_clicked)
medium_button = button(500, 250, medium_img, medium_img_hover, medium_img_clicked)
hard_button = button(650, 250, hard_img, hard_img_hover, hard_img_clicked)

play_again = button(350, 250, play_again_img, play_again_img_hover, play_again_img_clicked)
quit = button(700, 250, quit_img, quit_img_hover, quit_img_clicked)

pygame.mixer.music.play(-1)

run = True
while run:
    screen.blit(bg_img, (0, 0)) # adding background image

    if difficulty == None:
        if play_again.draw_button():
            if easy_button.draw_button():
                difficulty = "easy"
            if medium_button.draw_button():
                difficulty = "medium"
            if hard_button.draw_button():
                difficulty = "hard"
    elif difficulty == "easy":
        # your game logic for easy difficulty
        pass
    elif difficulty == "medium":
        # your game logic for medium difficulty
        pass
    elif difficulty == "hard":
        # your game logic for hard difficulty
        pass

    if quit.draw_button():
        print('Quit')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()


