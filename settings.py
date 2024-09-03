class Settings:
    """A class to store all settings for Python Platformer."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1400
        self.screen_height = 800
        self.bg_color = (255, 255, 255)  # White background

        # Player settings
        self.player_speed = 10.0
        self.jump_strength = 22.5
        self.idle_animation_time = 5
        self.running_animation_time = 2
        self.jumping_animation_time = 5
        self.attack_animation_time = 1
        self.attack_range = 100.0

        # Gravity settings
        self.gravity = 0.75
        self.gravity_fall = 7.5

        # Camera settings
        self.camera_speed = 1.5
        self.camera_margin = 600  # Margin before the camera starts moving

        # Background settings
        self.bg_color = (135, 206, 235)  # Light Blue Background

        # Enemy settings
        self.enemy_speed = 3.5
        self.enemy2_speed = 7.0
        self.enemy_animation_speed = 10

        # Power-up settings
        self.power_up_animation_time = 5

        # FPS Settings
        self.fps = 60
