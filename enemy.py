import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    """A class to represent an enemy in the game."""

    def __init__(self, pp_game, x, y, width, height):
        """Initialize the enemy and its starting position."""
        super().__init__()
        self.screen = pp_game.screen
        self.settings = pp_game.settings

        # Load spritesheets for different animations
        self.moving_spritesheet = pygame.image.load('slime_moving.png').convert_alpha()
        self.idle_spritesheet = pygame.image.load('slime_idle.png').convert_alpha()

        # Define dimensions of frames in the spritesheets
        self.frame_width = 64  # Adjust according to your spritesheets
        self.frame_height = 64  # Adjust according to your spritesheets

        # Initialize animation variables for moving
        self.current_moving_frame = 0
        self.moving_frames = []  # List to store moving frames
        self.moving_frame_delay = 125  # Number of game loops before updating moving frame
        self.moving_loop_count = 0  # Counter for moving animation loops

        # Initialize animation variables for idle
        self.current_idle_frame = 0
        self.idle_frames = []  # List to store idle frames
        self.idle_frame_delay = 225  # Number of game loops before updating idle frame
        self.idle_loop_count = 0  # Counter for idle animation loops

        self._extract_frames()

        # Set initial enemy image and rect to idle animation
        self.image = self.idle_frames[self.current_idle_frame]
        self.rect = self.image.get_rect()

        # Set initial position with y offset
        self.rect.x = x
        self.rect.bottom = y

        # Store a decimal value for the enemy's position
        self.x = float(self.rect.x)
        self.y = float(self.rect.bottom)  # Use bottom to match the ground level

        # Movement flags
        self.moving_right = True
        self.speed = self.settings.enemy_speed

        # Gravity settings
        self.vertical_speed = 0
        self.gravity = self.settings.gravity

        # Track last movement direction for sprite flipping
        self.last_direction = "right"

    def _extract_frames(self):
        """Extract frames from the spritesheets."""
        self._extract_moving_frames()
        self._extract_idle_frames()

    def _extract_moving_frames(self):
        """Extract moving frames from the moving spritesheet."""
        num_frames = self.moving_spritesheet.get_width() // self.frame_width
        for i in range(num_frames):
            frame_rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame_image = self.moving_spritesheet.subsurface(frame_rect)
            self.moving_frames.append(frame_image)

    def _extract_idle_frames(self):
        """Extract idle frames from the idle spritesheet."""
        num_frames = self.idle_spritesheet.get_width() // self.frame_width
        for i in range(num_frames):
            frame_rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame_image = self.idle_spritesheet.subsurface(frame_rect)
            self.idle_frames.append(frame_image)

    def update(self):
        """Update the enemy's position and animation."""
        if self.moving_right or not self.moving_right:
            # Update moving animation
            self.moving_loop_count += 1
            if self.moving_loop_count >= self.moving_frame_delay:
                self.current_moving_frame = (self.current_moving_frame + 1) % len(self.moving_frames)
                self.image = self.moving_frames[self.current_moving_frame]
                self.moving_loop_count = 0

                # Flip sprite if moving left
                if not self.moving_right:
                    self.image = pygame.transform.flip(self.image, True, False)

        else:
            # Update idle animation
            self.idle_loop_count += 1
            if self.idle_loop_count >= self.idle_frame_delay:
                self.current_idle_frame = (self.current_idle_frame + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.current_idle_frame]
                self.idle_loop_count = 0

                # Flip sprite based on last movement direction
                if self.last_direction == "left":
                    self.image = pygame.transform.flip(self.image, True, False)

        # Update enemy's position based on movement flags
        if self.moving_right:
            self.x += self.speed
            self.last_direction = "right"
        else:
            self.x -= self.speed
            self.last_direction = "left"

        # Apply gravity
        self.vertical_speed += self.gravity
        self.y += self.vertical_speed

        # Check if enemy is on the ground
        if self.y >= self.settings.screen_height:
            self.y = self.settings.screen_height
            self.vertical_speed = 0

        # Update the rect object from self.x and self.y
        self.rect.x = self.x
        self.rect.bottom = self.y  # Ensure bottom aligns with y to avoid floating

    def switch_direction(self):
        """Switch the direction of the enemy."""
        self.moving_right = not self.moving_right

    def draw(self, adjusted_rect):
        """Draw the enemy to the screen."""
        self.screen.blit(self.image, adjusted_rect)
