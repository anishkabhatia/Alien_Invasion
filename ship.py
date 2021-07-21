import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """ Initialize the ship and it's starting position. """
        #super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        Sprite.__init__(self)

        #Load the ship image and get its rect.
        #rect element lets you trat images as rectangles, so as to move and determine the position of the object
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Start each new ship at the botton center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #Store decimal value for the ship's center
        self.center = float(self.rect.centerx)

        #Movement Flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor

        #Update rect object from self.center
        self.rect.centerx = self.center

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx

    def blitme(self):
        """ Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

        