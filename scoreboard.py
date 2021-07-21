import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """A class to report scoring information."""

    def __init__(self, ai_settings, screen, stats):
        """initialize score keeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #Font settings for storing information
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont('arial', 35)

        #Prepare initial scoring image
        self.prep_score()
        self.prep_highscore()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "Score: " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        #Display score at the top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 30
        self.score_rect.top = self.screen_rect.top + 10

    def prep_highscore(self):
        """Turn the highscore into a rendered image."""
        highscore = int(round(self.stats.highscore, -1))
        highscore_str = "HighScore: " + "{:,}".format(highscore)
        self.highscore_image = self.font.render(highscore_str, True, self.text_color, self.ai_settings.bg_color)

        #Display score at the top center of screen
        self.highscore_rect = self.highscore_image.get_rect()
        self.highscore_rect.centerx = self.screen_rect.centerx
        self.highscore_rect.top = self.screen_rect.top + 20

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.ai_settings.bg_color)

        #Position and Display level under the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Display the ships left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw score, ships and levels to the screen."""
        self.screen.blit(self.score_image,  self.score_rect)
        self.screen.blit(self.highscore_image,  self.highscore_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
