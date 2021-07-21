import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, stats, score, ship, aliens, bullets):
    """Responds to keypresses"""
    if event.key == pygame.K_RIGHT:
        #Move ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        #Move ship to the left.
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p:
        key_pressed = True
        check_play_key(ai_settings, screen, stats, score, ship, aliens, bullets, key_pressed)

def check_keyup_events(event, ship):
    """Responds to keyreleases"""
    if event.key == pygame.K_RIGHT:
        #Stop moving ship to right
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        #Stop moving ship to left
        ship.moving_left = False

def check_events(ai_settings, screen, stats, score, play_button, ship, aliens, bullets):
    """Responds to key presses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, score, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, score, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_key(ai_settings, screen, stats, score, ship, aliens, bullets, key_pressed):
    """Check is play key p is clicked or not. Start a new game if clicked."""
    if key_pressed and not stats.game_active:
        #Reset game settings
        ai_settings.initialize_dynamic_settings()

        #Hide mouse cursor
        pygame.mouse.set_visible(False)

        #Reset game statistics
        stats.reset_stats()
        stats.game_active = True

        #Reset scoreboard images
        score.prep_score()
        score.prep_highscore()
        score.prep_level()
        score.prep_ships()

        #Empty list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_play_button(ai_settings, screen, stats, score, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Starts a new game when player clicks play."""
    button_clicked = play_button.rect.collidepoint(mouse_x ,mouse_y)
    if button_clicked and not stats.game_active:
        #Reset game settings
        ai_settings.initialize_dynamic_settings()

        #Hide mouse cursor
        pygame.mouse.set_visible(False)

        #Reset game statistics
        stats.reset_stats()
        stats.game_active = True

        #Reset scoreboard images
        score.prep_score()
        score.prep_highscore()
        score.prep_level()
        score.prep_ships()

        #Empty list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, score, ship, aliens, bullets, play_button):
    """Updates images on the screen and flips to new screen."""
    #Redraw screen during each pass through loop
    screen.fill(ai_settings.bg_color)
    
    #Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    #Display ship
    ship.blitme()
    
    #Display fleet of aliens
    aliens.draw(screen)
    
    #Display the score information
    score.show_score()

    #Draw play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()
    
    #Making most recently drawn screen available
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, score, ship, aliens, bullets):
    """Update position of the bullets and get rid of old bullets."""
    #Update bullets position
    bullets.update()

    #Get rid of bullets that have dissappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= screen.get_rect().top:
            bullets.remove(bullet)
    #print(len(bullets))        shows the decreasing number of bullets as they disappear

    check_bullet_alien_collisions(ai_settings, screen, stats, score, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, score, ship, aliens, bullets):
    """Respond to bullet-alien collision."""
    #remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            score.prep_score()
        check_highcore(stats, score)

    if len(aliens) == 0:
        #Destroy existing bullets, speed up game and create new fleet
        bullets.empty()
        ai_settings.increase_speed()

        #Increase Level
        stats.level += 1
        score.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit is not reached yet."""
    #Check for limit
    if len(bullets) < ai_settings.bullets_allowed:
        #Create a new bullet and add it to the bullets group.
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_of_aliens(ai_settings, alien_width):
    """Determine the number of aliens that can fit in a row."""
    # Margin space is equal to one alien width
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    # Spacing between each alien is equal to one alien width
    number_of_aliens = int(available_space_x / (2 * alien_width))
    return number_of_aliens

def get_number_of_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_of_rows = int(available_space_y / (2 * alien_height))
    return number_of_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    #Create an alien and find number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_of_aliens = get_number_of_aliens(ai_settings, alien.rect.width)
    number_of_rows = get_number_of_rows(ai_settings, ship.rect.height, alien.rect.height)

    #Create the fleet of aliens
    for row_number in range(number_of_rows):
        #Create the first row of aliens and so on
        for alien_number in range(number_of_aliens):
            # Create an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any alien has reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, score, ship, aliens, bullets):
    """Respond to ship being hit by an alien."""
    if stats.ships_left > 0:
        #Decrement number of ships left
        stats.ships_left -= 1

        #Update scoreboard
        score.prep_ships()

        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #Pause
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, score, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #treat in the same way as if hit by a ship
            ship_hit(ai_settings, screen, stats, score, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, score, ship, aliens, bullets):
    """Check if fleet is at an edge and Update the position of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    #Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, score, ship, aliens, bullets)
    #Look for aliens hitting the bottom of screen
    check_aliens_bottom(ai_settings, screen, stats, score, ship, aliens, bullets)

def check_highcore(stats, score):
    """Check to see if there is a new highscore"""
    if stats.score > stats.highscore:
        stats.highscore = stats.score
        score.prep_highscore()