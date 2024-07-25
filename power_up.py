import pygame
from pygame.sprite import Sprite

class PowerUp(Sprite):
    """A class to represent a power-up."""

    def __init__(self, pp_game, x, y):
        """Initialize the power-up and its starting position."""
        super().__init__()
        self.screen = pp_game.screen
        self.settings = pp_game.settings
        self.spritesheet = pygame.image.load('items.png').convert_alpha()  # Load your spritesheet image
        self.frame_width = 32
        self.frame_height = 32

        # Initialize animation variables
        self.current_frame = 0
        self.frames = []  # List to store animation frames
        self.frame_delay = self.settings.power_up_animation_time  # Number of game loops before updating frame
        self.loop_count = 0  # Counter for animation loops

        # Extract frames from the spritesheet
        self._extract_frames()

        # Set initial power-up image and rect
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Position the power-up at the given coordinates
        self.rect.x = x
        self.rect.y = y

    def _extract_frames(self):
        """Extract frames from the spritesheet."""
        row = 5  # Sixth row (0-indexed)
        num_frames = 5  # Five columns of animations

        for col in range(num_frames):
            frame_rect = pygame.Rect(col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height)
            frame_image = self.spritesheet.subsurface(frame_rect)
            self.frames.append(frame_image)

    def update(self):
        """Update the power-up's animation."""
        self.loop_count += 1
        if self.loop_count >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.loop_count = 0

    def draw(self, camera_x):
        """Draw the power-up on the screen."""
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= camera_x
        self.screen.blit(self.image, adjusted_rect)
