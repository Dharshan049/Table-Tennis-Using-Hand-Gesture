import pygame
from pygame.locals import *
import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pygame
pygame.mixer.init()

pygame.init()

# Load button images
play_again_img = pygame.image.load("start_btn.png")
play_again_img_hover = pygame.image.load("start_hover_btn.png")
play_again_img_clicked = pygame.image.load("start_clicked_btn.png")

quit_img = pygame.image.load("exit_btn.png")
quit_img_hover = pygame.image.load("exit_hover_btn.png")
quit_img_clicked = pygame.image.load("exit_clicked_btn.png")

# Load background image and resize it to screen size
bg_img = pygame.image.load("background.jpg")
bg_img = pygame.transform.scale(bg_img, (1280, 720))

# Load background music
pygame.mixer.music.load("bg_music.wav")
startSound = pygame.mixer.Sound("sfx.wav")
exit_sound = pygame.mixer.Sound("click.wav")

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('TableTennis')

#define global variable
clicked = False
counter = 0

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

play_again = button(350, 250, play_again_img, play_again_img_hover, play_again_img_clicked)
quit = button(700, 250, quit_img, quit_img_hover, quit_img_clicked)

pygame.mixer.music.play(-1)

def table_tennis_game():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Importing all images
    imgBackground = cv2.imread('2DIMAGES/Background.png')
    imgGameOver = cv2.imread('2DIMAGES/gameOver.png')
    imgGameStart = cv2.imread('2DIMAGES/gameStart.png')
    imgBall = cv2.imread('2DIMAGES/ball.png', cv2.IMREAD_UNCHANGED)
    imgBat1 = cv2.imread('2DIMAGES/racket1.png', cv2.IMREAD_UNCHANGED)
    imgBat2 = cv2.imread('2DIMAGES/racket2.png', cv2.IMREAD_UNCHANGED)
    bounce_sound = pygame.mixer.Sound("2DIMAGES/bounce_sound.wav")
    end_sound = pygame.mixer.Sound("click.wav")
    restart_sound = pygame.mixer.Sound("restart.wav")

    # Hand Detector
    detector = HandDetector(detectionCon=0.8, maxHands=2)

    # Variables
    ballPos = [100, 100]
    speedX = 15
    speedY = 15
    gameOver = False
    score = [0, 0]

    gameStart = True
    solo = True

    while True:
        _, img = cap.read()

        img = cv2.flip(img, 1)

        # Find the hand and its landmarks
        hands, img = detector.findHands(img, flipType=False)  # with draw

        # Overlaying the background image
        img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

        # Check for hands
        if hands:
            for hand in hands:
                x, y, w, h = hand["bbox"]
                h1, w1, _ = imgBat1.shape
                y1 = y - h1 / 2
                y1 = np.clip(y1, 20, 395)

                if solo:
                    # Bot controlling the left bat
                    bot_y = ballPos[1] - imgBat1.shape[0] // 2
                    bot_y = np.clip(bot_y, 20, 415)
                    img = cvzone.overlayPNG(img, imgBat1, (59, int(bot_y)))
                    if 59 < ballPos[0] < 59 + imgBat1.shape[1] and bot_y < ballPos[1] < bot_y + imgBat1.shape[0]:
                        speedX = -speedX
                        ballPos[0] += 30
                        score[0] += 1
                        bounce_sound.play()

                    if hand['type'] == "Right":
                        img = cvzone.overlayPNG(img, imgBat2, (1195, int(y1)))
                        if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                            speedX = -speedX
                            ballPos[0] -= 30
                            score[1] += 1
                            bounce_sound.play()
                else:
                    if hand['type'] == "Right":
                        img = cvzone.overlayPNG(img, imgBat1, (59, int(y1)))
                        if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                            speedX = -speedX
                            ballPos[0] += 30
                            bounce_sound.play()

                    if hand['type'] == "Left":
                        img = cvzone.overlayPNG(img, imgBat2, (1195, int(y1)))
                        if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                            speedX = -speedX
                            ballPos[0] -= 30
                            bounce_sound.play()
        # Game Over
        if solo:
            if ballPos[0] < 40 or ballPos[0] > 1200:
                gameOver = True
        else:
            if ballPos[0] < 40:
                score[1] += 1
            elif ballPos[0] > 1200:
                score[0] += 1
            if ballPos[0] < 40 or ballPos[0] > 1200:
                ballPos = [100, 100]
                speedX = 15
                speedY = 15
            if max(score) == 11:
                gameOver = True

        if gameOver and solo:
            img = imgGameOver
            cv2.putText(img, str(score[0]) + ":" + str(score[1]), (560, 370), cv2.FONT_HERSHEY_COMPLEX,
                        2.5, (200, 0, 200), 5)
        elif gameOver:
            img = imgGameOver
            cv2.putText(img, str(score[0]) + ":" + str(score[1]), (560, 370), cv2.FONT_HERSHEY_COMPLEX,
                        2.5, (200, 0, 200), 5)

        elif gameStart:
            img = imgGameStart

        # if game not over move the ball
        else:

            # Move the Ball
            if ballPos[1] >= 500 or ballPos[1] <= 10:
                speedY = -speedY

            ballPos[0] += speedX
            ballPos[1] += speedY

            # Draw the ball
            img = cvzone.overlayPNG(img, imgBall, ballPos)

            cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
            cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

        cv2.imshow("TableTennis", img)

        key = cv2.waitKey(1)
        if key == ord('r') or key == ord('R'):
            restart_sound.play()
            ballPos = [100, 100]
            speedX = 15
            speedY = 15
            gameOver = False
            score = [0, 0]
            imgGameOver = cv2.imread('2DIMAGES/gameOver.png')
            gameStart = True
        elif key == ord('1') and gameStart:
            solo = True
            gameStart = False
        elif key == ord('2') and gameStart:
            solo = False
            gameStart = False
        elif key == 27:
            cv2.destroyAllWindows()
            end_sound.play()
            break

run = True
while run:
    screen.blit(bg_img, (0, 0)) # adding background image
    if play_again.draw_button():
        startSound.play()
        table_tennis_game()
        counter = 0
    if quit.draw_button():
        run = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()