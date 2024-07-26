class Settings:
    """A class to store all settings for Python Platformer."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1400
        self.screen_height = 800
        self.bg_color = (255, 255, 255)  # White background

        # Player settings
        self.player_speed = 1.5
        self.jump_strength = 7.0
        self.idle_animation_time = 50
        self.running_animation_time = 20
        self.jumping_animation_time = 50
        self.attack_animation_time = 10
        self.attack_range = 100.0

        # Gravity settings
        self.gravity = 0.05
        self.gravity_fall = 1.5

        # Camera settings
        self.camera_speed = 1.5
        self.camera_margin = 600  # Margin before the camera starts moving

        # Background settings
        self.bg_color = (255, 255, 255)  # White background

        # Enemy settings
        self.enemy_speed = 0.35
        self.enemy2_speed = 0.7
        self.enemy_animation_speed = 100

        # Power-up settings
        self.power_up_animation_time = 50

        # FPS Settings
        self.fps = 400
