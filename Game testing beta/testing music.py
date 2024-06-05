import pygame.mixer

# Initialize the mixer
pygame.mixer.init()

# Load the background music
bg_music = pygame.mixer.Sound('bg_music.wav')

# Play the background music in a loop
channel = bg_music.play()
channel.set_endevent(pygame.constants.USEREVENT)
while channel.get_busy():
    pygame.time.wait(1000)
    bg_music.play()
