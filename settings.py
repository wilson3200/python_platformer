class Settings:
    """A class to store all settings for Python Platformer."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1400
        self.screen_height = 800
        self.bg_color = (255, 255, 255)  # White background

        # Player settings
        self.player_speed = 1.7
        self.jump_strength = 8.0  # Increased jump strength for better vertical movement
        self.idle_animation_time = 50
        self.running_animation_time = 20
        self.jumping_animation_time = 50

        # Gravity settings
        self.gravity = .07  # Increased gravity for better vertical movement

        # Camera settings
        self.camera_speed = 1.5
        self.camera_margin = 400  # Margin before the camera starts moving

        # Background settings
        self.bg_color = (255, 255, 255)  # White background

        # Enemy settings
        self.enemy_speed = 0.5  # Speed of enemy NPCs
