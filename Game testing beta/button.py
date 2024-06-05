import pygame

#button class
class Button():
    def __init__(self, x, y, image, hover_image, clicked_image, scale):
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.hover_image = pygame.transform.scale(hover_image, (int(hover_image.get_width() * scale), int(hover_image.get_height() * scale)))
        self.clicked_image = pygame.transform.scale(clicked_image, (int(clicked_image.get_width() * scale), int(clicked_image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.hover = False
        self.clicking = False
    def update(self, surface):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicking = True
        else:
            self.hover = False
            self.clicking = False
        if self.clicking:
            surface.blit(self.clicked_image, (self.rect.x, self.rect.y))
        elif self.hover:
            surface.blit(self.hover_image, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))
    def is_clicked(self):
        if self.clicking:
            self.clicking = False
            return True
        else:
            return False
