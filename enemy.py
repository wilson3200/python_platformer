import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    """A class to represent an enemy in the game."""

    def __init__(self, pp_game, x, y):
        """Initialize the enemy and its starting position."""
        super().__init__()
        self.screen = pp_game.screen
        self.settings = pp_game.settings

        # Load spritesheet for animations
        self.spritesheet = pygame.image.load('enemies.png').convert_alpha()

        # Define dimensions of frames in the spritesheet
        self.frame_width = 20  # Width of each frame
        self.frame_height = 20  # Height of each frame

        # Initialize animation variables
        self.current_frame = 0
        self.frames = []  # List to store frames
        self.frame_delay = 125  # Number of game loops before updating frame
        self.loop_count = 0  # Counter for animation loops

        self._extract_frames()

        # Set initial enemy image and rect
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Set initial position
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
        """Extract frames from the spritesheet."""
        num_rows = 12  # Total number of rows in the spritesheet
        num_cols = 4  # Total number of columns in the spritesheet

        # Select the 9th row for this enemy's animation
        row = 8  # Zero-based index (9th row)

        for col in range(num_cols):
            frame_rect = pygame.Rect(col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height)
            frame_image = self.spritesheet.subsurface(frame_rect)
            self.frames.append(frame_image)

    def update(self):
        """Update the enemy's position and animation."""
        self.loop_count += 1
        if self.loop_count >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.loop_count = 0

            # Flip sprite if moving left
            if not self.moving_right:
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

        # Update the rect object from self.x and self.y
        self.rect.x = self.x
        self.rect.bottom = self.y  # Ensure bottom aligns with y to avoid floating

    def switch_direction(self):
        """Switch the direction of the enemy."""
        self.moving_right = not self.moving_right

    def draw(self, adjusted_rect):
        """Draw the enemy to the screen."""
        # Scale the image to four times its size
        scaled_image = pygame.transform.scale(self.image, (self.rect.width * 6, self.rect.height * 4))

        # Adjust the position to keep the center of the sprite at the same location and raise it by 30 pixels
        scaled_rect = scaled_image.get_rect(center=adjusted_rect.center)
        scaled_rect.y -= 30

        # Halve the size of the collision rect
        collision_rect = self.rect.copy()
        collision_rect.width //= 2
        collision_rect.height //= 1
        collision_rect.center = adjusted_rect.center

        self.screen.blit(scaled_image, scaled_rect)

    def check_edges(self, obstacles):
        """Check if the enemy is at the edge of an obstacle."""
        buffer = 5  # Buffer to avoid switching too early
        on_obstacle = False
        for obstacle in obstacles:
            if self.rect.bottom == obstacle.rect.top and obstacle.rect.left < self.rect.right and self.rect.left < obstacle.rect.right:
                on_obstacle = True
                if self.moving_right and self.rect.right >= obstacle.rect.right - buffer:
                    self.switch_direction()
                elif not self.moving_right and self.rect.left <= obstacle.rect.left + buffer:
                    self.switch_direction()
        if not on_obstacle:
            self.vertical_speed += self.gravity
