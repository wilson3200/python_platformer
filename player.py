import pygame
from pygame.sprite import Sprite

class Player(Sprite):
    """A class to manage the player."""

    def __init__(self, pp_game):
        """Initialize the player and its starting position."""
        super().__init__()
        self.screen = pp_game.screen
        self.settings = pp_game.settings
        self.screen_rect = pp_game.screen.get_rect()

        # Load spritesheets for different animations
        self.walk_spritesheet = pygame.image.load('player_walk.png').convert_alpha()
        self.idle_spritesheet = pygame.image.load('player_idle.png').convert_alpha()
        self.jump_spritesheet = pygame.image.load('player_jump.png').convert_alpha()

        # Define dimensions of frames in the spritesheets
        self.frame_width = 100  # Adjust according to your spritesheets
        self.frame_height = 64  # Adjust according to your spritesheets

        # Initialize animation variables for walking
        self.current_walk_frame = 0
        self.walk_frames = []  # List to store walking frames
        self.walk_frame_delay = self.settings.running_animation_time  # Number of game loops before updating walk frame
        self.walk_loop_count = 0  # Counter for walk animation loops

        # Initialize animation variables for idle
        self.current_idle_frame = 0
        self.idle_frames = []  # List to store idle frames
        self.idle_frame_delay = self.settings.idle_animation_time  # Number of game loops before updating idle frame
        self.idle_loop_count = 0  # Counter for idle animation loops

        # Initialize animation variables for jumping
        self.current_jump_frame = 0
        self.jump_frames = []  # List to store jump frames
        self.jump_frame_delay = self.settings.jumping_animation_time  # Number of game loops before updating jump frame
        self.jump_loop_count = 0  # Counter for jump animation loops

        self._extract_frames()

        # Set initial player image and rect to walking animation facing right
        self.image = self.walk_frames[self.current_walk_frame]
        self.rect = self.image.get_rect()

        # Start the new player 16 pixels above the bottom of the screen
        self.rect.midbottom = (self.screen_rect.midbottom[0], self.screen_rect.midbottom[1] - 16)

        # Store a decimal value for the player's x pos and y pos
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.jumping = False

        # Jumping Settings
        self.vertical_speed = 0
        self.gravity = self.settings.gravity
        self.jump_strength = self.settings.jump_strength
        self.is_jumping = False

        # Track last movement direction for idle animation
        self.last_direction = "right"  # Initial direction

        # Load the jump sound effect
        self.jump_sound = pygame.mixer.Sound('jump1.wav')

    def _extract_frames(self):
        """Extract frames from the spritesheets."""
        self._extract_walk_frames()
        self._extract_idle_frames()
        self._extract_jump_frames()

    def _extract_walk_frames(self):
        """Extract walking frames from the walk spritesheet."""
        num_frames = self.walk_spritesheet.get_width() // self.frame_width
        for i in range(num_frames):
            frame_rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame_image = self.walk_spritesheet.subsurface(frame_rect)
            self.walk_frames.append(frame_image)

    def _extract_idle_frames(self):
        """Extract idle frames from the idle spritesheet."""
        num_frames = self.idle_spritesheet.get_width() // self.frame_width
        for i in range(num_frames):
            frame_rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame_image = self.idle_spritesheet.subsurface(frame_rect)
            self.idle_frames.append(frame_image)

    def _extract_jump_frames(self):
        """Extract jump frames from the jump spritesheet."""
        num_frames = self.jump_spritesheet.get_width() // self.frame_width
        for i in range(num_frames):
            frame_rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame_image = self.jump_spritesheet.subsurface(frame_rect)
            self.jump_frames.append(frame_image)

    def update(self):
        """Update the player's position and animation."""
        if self.moving_right or self.moving_left:
            # Update walking animation
            self.walk_loop_count += 1
            if self.walk_loop_count >= self.walk_frame_delay:
                self.current_walk_frame = (self.current_walk_frame + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.current_walk_frame]
                self.walk_loop_count = 0

                # Flip sprite if moving left
                if self.moving_left:
                    self.image = pygame.transform.flip(self.image, True, False)

        elif self.jumping:
            # Update jump animation
            self.jump_loop_count += 1
            if self.jump_loop_count >= self.jump_frame_delay:
                self.current_jump_frame = (self.current_jump_frame + 1) % len(self.jump_frames)
                self.image = self.jump_frames[self.current_jump_frame]
                self.jump_loop_count = 0

                # Flip sprite if moving left
                if self.moving_left:
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

        # Update player's position based on movement flags
        if self.moving_right:
            self.x += self.settings.player_speed
            self.last_direction = "right"
        if self.moving_left:
            self.x -= self.settings.player_speed
            self.last_direction = "left"

        # Handle jumping mechanics
        if self.jumping and not self.is_jumping:
            self.vertical_speed = -self.jump_strength
            self.is_jumping = True
            # Play the jump sound effect
            self.jump_sound.play()

        # Apply gravity if the player is in the air
        if self.is_jumping or self.vertical_speed != 0:
            self.vertical_speed += self.gravity
            self.y += self.vertical_speed

        # Update the rect object from self.x and self.y
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        """Draw the player's sprite and the collision rect."""
        self.screen.blit(self.image, self.rect)
