import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_functions as gf
from button import Button
from scoreboard import Scoreboard

def main():
    #Initializing game and creating screen object
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #Make the play Button
    play_button = Button(ai_settings, screen, "Play")

    #Create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    score = Scoreboard(ai_settings, screen, stats)

    #Make a ship
    ship = Ship(ai_settings, screen)

    #Making a group to store bullets in
    bullets = Group()

    #Making a group to store aliens in
    aliens = Group()
    #Making the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #Starting main loop for the game
    while True:

        gf.check_events(ai_settings, screen, stats, score, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, score, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, score, ship, aliens, bullets)
            
        gf.update_screen(ai_settings, screen, stats, score, ship, aliens, bullets, play_button)

if __name__ == "__main__":
    main()

        
