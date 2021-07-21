class Settings():
    """A class to store all the settings of the Alien Invasion Game"""

    def __init__(self):
        """Initializing game's static settings"""
        #Screen Settings
        self.screen_width = 1200
        self.screen_height = 670
        self.bg_color = (230, 230, 230)

        #Ship settings
        self.ship_limit = 3

        #Bullet Settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #Alien settings
        self.fleet_drop_speed = 5
        
        #How quickly the game speeds up
        self.speedup_scale = 1.1

        #How quicky score value increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        #Ship settings
        self.ship_speed_factor = 1.5

        #Bullet Settings
        self.bullet_speed_factor = 1
        
        #Alien settings
        self.alien_speed_factor = 0.5
        # Fleet direction of 1 represents right, -1 represents left
        self.fleet_direction = 1

        #Points on shooting an alien/Scoring
        self.alien_points = 10

    def increase_speed(self):
        """Increase speed settings and alient point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

