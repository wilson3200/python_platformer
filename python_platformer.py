import sys
import pygame
import math
from settings import Settings
from game_stats import GameStats
from player import Player
from level_one import LevelOne
from level_two import LevelTwo

class PythonPlatformer:
    """Class to manage game, the assets, and behaviors."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.stats = GameStats(self)  # Pass self to GameStats
        self.player = Player(self)
        self.camera_x = 0
        self._load_level()  # Load the initial level
        self.font = pygame.font.SysFont(None, 48)
        self.pause_menu_font = pygame.font.SysFont(None, 72)

        # Pause menu related
        self.pause_menu_active = False
        self.ui_spritesheet = pygame.image.load('UI.png').convert_alpha()
        self.resume_button_image = self._get_sprite(0, 2)
        self.resume_button_hover_image = self._get_sprite(0, 3)
        self.restart_button_image = self._get_sprite(1, 0)
        self.restart_button_hover_image = self._get_sprite(1, 1)
        self.exit_button_image = self._get_sprite(1, 2)
        self.exit_button_hover_image = self._get_sprite(1, 3)

        # Load the button select sound
        self.select_sound = pygame.mixer.Sound('select.wav')

    def _get_sprite(self, row, col):
        """Get a sprite from the sprite sheet based on row and column."""
        sprite_width, sprite_height = 32, 32
        x = col * sprite_width
        y = row * sprite_height
        return self.ui_spritesheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))

    def _load_level(self):
        """Load the current level based on the stats."""
        if self.stats.level == 1:
            self.level = LevelOne(self)
        elif self.stats.level == 2:
            self.level = LevelTwo(self)
        self.level.set_player_position()  # Set the player's initial position for the loaded level

        # Update the enemies attribute with the level's enemies
        self.enemies = self.level.enemies

    def run_game(self):
        """Start the main loop for the game."""
        level_complete_collided = False  # Track if collision with level complete object has occurred
        start_time = pygame.time.get_ticks()  # Add this line to get the start time

        while True:
            self._check_events()
            if self.stats.game_active and not self.pause_menu_active:
                self.player.update(enemies=self.enemies)
                self.level.update()
                self._update_camera()
                self._check_collisions()
                # Update the elapsed time
                self.stats.elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Calculate elapsed time in seconds

                # Check if player reached level complete object
                if pygame.sprite.collide_rect(self.player, self.level.level_complete):
                    if not level_complete_collided:  # Only open the chest if not already opened
                        self.level.level_complete.open()
                        level_complete_collided = True  # Mark as collided to avoid reopening
                        self.stats.level_complete_time = pygame.time.get_ticks()  # Record the time of collision

            self._update_screen()

            # Check if level completion delay has passed
            if self.stats.level_complete_time and (pygame.time.get_ticks() - self.stats.level_complete_time >= 2000):
                self._start_next_level()

    def _start_next_level(self):
        """Start the next level."""
        self.stats.level += 1
        self.stats.level_complete_time = None  # Reset the level complete time
        self.level = LevelTwo(self)
        self.level.set_player_position()  # Set the player's position for the new level

    def _check_collisions(self):
        """Check for collisions between the player and obstacles, and between enemies and obstacles."""
        player_colliding = False
        for obstacle in self.level.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                player_colliding = True
                if self.player.vertical_speed > 0 and self.player.rect.bottom > obstacle.rect.top and self.player.rect.top < obstacle.rect.top:
                    self.player.rect.bottom = obstacle.rect.top
                    self.player.y = self.player.rect.bottom - self.player.rect.height
                    self.player.vertical_speed = 0
                    self.player.is_jumping = False
                elif self.player.vertical_speed < 0 and self.player.rect.top < obstacle.rect.bottom and self.player.rect.bottom > obstacle.rect.bottom:
                    self.player.rect.top = obstacle.rect.bottom
                    self.player.y = self.player.rect.top
                    self.player.vertical_speed = 0
                elif self.player.moving_right and self.player.rect.right > obstacle.rect.left and self.player.rect.left < obstacle.rect.left:
                    self.player.rect.right = obstacle.rect.left
                    self.player.x = self.player.rect.right - self.player.rect.width
                elif self.player.moving_left and self.player.rect.left < obstacle.rect.right and self.player.rect.right > obstacle.rect.right:
                    self.player.rect.left = obstacle.rect.right
                    self.player.x = self.player.rect.left

        if not player_colliding and not self.player.is_jumping:
            self.player.is_jumping = False
            self.player.vertical_speed = 1.0

        # Check collisions between player and enemies using rect
        for enemy in self.level.enemies:
            if self.player.rect.colliderect(enemy.rect):
                # If player collides with any enemy, end the game
                self.stats.game_active = False
                break

        # Check collisions between enemies and obstacles
        for enemy in self.level.enemies:
            for obstacle in self.level.obstacles:
                if enemy.rect.colliderect(obstacle.rect):
                    if enemy.vertical_speed > 0 and enemy.rect.bottom > obstacle.rect.top and enemy.rect.top < obstacle.rect.top:
                        enemy.rect.bottom = obstacle.rect.top
                        enemy.y = enemy.rect.bottom
                        enemy.vertical_speed = 0

        # Check to see if player fell off the map
        if self.player.rect.y >= self.settings.screen_height + 200:
            self.stats.game_active = False

    def _check_events(self):
        """Watch for keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and self.pause_menu_active:
                self._check_pause_menu_events(event)

    def _check_keydown_events(self, event):
        """Responds to key presses."""
        if event.key == pygame.K_d:
            self.player.moving_right = True
        elif event.key == pygame.K_a:
            self.player.moving_left = True
        elif event.key == pygame.K_w:
            if not self.player.is_jumping:
                self.player.jumping = True
        elif event.key == pygame.K_SPACE:
            self.player.attack(self.level.enemies)  # Call the attack method and pass the enemies group
        elif event.key == pygame.K_ESCAPE:
            self._toggle_pause()

    def _check_keyup_events(self, event):
        """Responds to key releases."""
        if event.key == pygame.K_d:
            self.player.moving_right = False
        elif event.key == pygame.K_a:
            self.player.moving_left = False
        elif event.key == pygame.K_w:
            self.player.jumping = False

    def _update_camera(self):
        """Update the camera position to follow the player horizontally."""
        if self.player.rect.right > self.camera_x + self.settings.screen_width - self.settings.camera_margin:
            self.camera_x = self.player.rect.right - self.settings.screen_width + self.settings.camera_margin
        if self.player.rect.left < self.camera_x + self.settings.camera_margin:
            self.camera_x = self.player.rect.left - self.settings.camera_margin

    def _update_screen(self):
        """Redraw the screen during each pass through."""
        self.screen.fill(self.settings.bg_color)  # Fill the screen with the background color
        adjusted_player_rect = self.player.rect.copy()
        adjusted_player_rect.x -= self.camera_x
        self.screen.blit(self.player.image, adjusted_player_rect)
        self.level.draw()  # Draw level elements

        # Draw the level complete object
        adjusted_level_complete_rect = self.level.level_complete.rect.copy()
        adjusted_level_complete_rect.x -= self.camera_x
        self.level.level_complete.draw(self.screen, adjusted_level_complete_rect)

        self._draw_timer()

        if self.pause_menu_active:
            self._draw_pause_menu()

        pygame.display.flip()

    def _draw_timer(self):
        """Draw the timer on the screen."""
        timer_text = f"Time: {self.stats.elapsed_time:.2f}s"
        timer_image = self.font.render(timer_text, True, (30, 30, 30))
        self.screen.blit(timer_image, (20, 20))

    def _toggle_pause(self):
        """Toggle the pause state of the game."""
        self.pause_menu_active = not self.pause_menu_active
        self.stats.game_active = not self.pause_menu_active
        if not self.pause_menu_active:
            pygame.mixer.music.unpause()  # Resume music when game is unpaused
        else:
            pygame.mixer.music.pause()  # Pause music when game is paused

    def _draw_pause_menu(self):
        """Draw the pause menu."""
        # Draw the semi-transparent overlay
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        self.screen.blit(overlay, (0, 0))

        # Calculate button positions
        button_width, button_height = 32, 32  # Assuming buttons are 32x32
        button_spacing = 20
        total_height = 3 * button_height + 2 * button_spacing
        start_y = (self.settings.screen_height - total_height) // 2

        resume_button_rect = pygame.Rect(
            (self.settings.screen_width - button_width) // 2, start_y, button_width, button_height)
        restart_button_rect = pygame.Rect(
            (self.settings.screen_width - button_width) // 2, start_y + button_height + button_spacing, button_width, button_height)
        exit_button_rect = pygame.Rect(
            (self.settings.screen_width - button_width) // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height)

        # Draw buttons with hover effect
        mouse_pos = pygame.mouse.get_pos()
        self._draw_button(resume_button_rect, self.resume_button_image, self.resume_button_hover_image, mouse_pos)
        self._draw_button(restart_button_rect, self.restart_button_image, self.restart_button_hover_image, mouse_pos)
        self._draw_button(exit_button_rect, self.exit_button_image, self.exit_button_hover_image, mouse_pos)

        pygame.display.flip()

    def _draw_button(self, rect, default_image, hover_image, mouse_pos):
        """Draw a button with hover effect."""
        if rect.collidepoint(mouse_pos):
            self.screen.blit(hover_image, rect)
        else:
            self.screen.blit(default_image, rect)

    def _check_pause_menu_events(self, event):
        """Handle mouse click events on the pause menu."""
        mouse_pos = pygame.mouse.get_pos()
        button_width, button_height = 32, 32
        button_spacing = 20
        total_height = 3 * button_height + 2 * button_spacing
        start_y = (self.settings.screen_height - total_height) // 2

        resume_button_rect = pygame.Rect(
            (self.settings.screen_width - button_width) // 2, start_y, button_width, button_height)
        restart_button_rect = pygame.Rect(
            (self.settings.screen_width - button_width) // 2, start_y + button_height + button_spacing, button_width, button_height)
        exit_button_rect = pygame.Rect(
            (self.settings.screen_width - button_width) // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height)

        if event.button == 1:  # Left mouse button click
            if resume_button_rect.collidepoint(mouse_pos):
                self.select_sound.play()
                self._toggle_pause()
            elif restart_button_rect.collidepoint(mouse_pos):
                self.select_sound.play()
                self.stats.reset_stats()
                self._load_level()
                self._toggle_pause()
            elif exit_button_rect.collidepoint(mouse_pos):
                self.select_sound.play()
                sys.exit()

if __name__ == '__main__':
    pp_game = PythonPlatformer()
    pp_game.run_game()
