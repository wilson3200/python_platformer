import sys
import pygame
from settings import Settings
from game_stats import GameStats
from player import Player
from obstacle import Obstacle
from enemy import Enemy
from level_complete import LevelComplete

class PythonPlatformer:
    """Class to manage game, the assets, and behaviors."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.stats = GameStats(self)
        self.player = Player(self)
        self.camera_x = 0
        self.obstacles = []
        self.enemies = []
        self._create_obstacles()
        self._create_enemies()
        self.font = pygame.font.SysFont(None, 48)
        self.level_complete = LevelComplete(self, 9_950, self.settings.screen_height-48)

        # Load background music
        pygame.mixer.music.load('box_jump.ogg')

    def _create_obstacles(self):
        """Create obstacles and ground for the level."""
        # Create the ground
        self.obstacles.append(Obstacle(self, 0, self.settings.screen_height - 16, 2000, 16))
        self.obstacles.append(Obstacle(self, 3200, self.settings.screen_height - 16, 800, 16))
        self.obstacles.append(Obstacle(self, 5000, self.settings.screen_height - 16, 600, 16))
        self.obstacles.append(Obstacle(self, 8000, self.settings.screen_height - 16, 2000, 16))

        # Create Platforms
        self.obstacles.append(Obstacle(self, 2300, self.settings.screen_height - 216, 460, 16))
        self.obstacles.append(Obstacle(self, 4300, self.settings.screen_height - 216, 400, 16))
        self.obstacles.append(Obstacle(self, 5800, self.settings.screen_height - 240, 300, 16))
        self.obstacles.append(Obstacle(self, 6400, self.settings.screen_height - 426, 400, 16))
        self.obstacles.append(Obstacle(self, 7100, self.settings.screen_height - 628, 400, 16))

        # Create Wall (test)
        # self.obstacles.append(Obstacle(self, 1800, self.settings.screen_height-200, 30, 500))

        # Create left wall (using index 1 from forest_tileset.png for the entire height)
        self.obstacles.append(Obstacle(self, 0, 0, 16, self.settings.screen_height, tile_index=1))

        # Create right wall (using index 1 from forest_tileset.png for the entire height)
        self.obstacles.append(Obstacle(self, 10000, 0, 16, self.settings.screen_height, tile_index=1))

    def _create_enemies(self):
        """Create enemies for the level."""
        # Enemies on the ground sections
        self.enemies.append(Enemy(self, 1000, self.settings.screen_height - 16 - 25))  # Ground section 1
        self.enemies.append(Enemy(self, 3200 + 400, self.settings.screen_height - 16 - 25))  # Ground section 2
        self.enemies.append(Enemy(self, 5000 + 300, self.settings.screen_height - 16 - 25))  # Ground section 3
        self.enemies.append(Enemy(self, 8000 + 1000, self.settings.screen_height - 16 - 25))  # Ground section 4

        # Enemies on the platform sections
        self.enemies.append(Enemy(self, 2300 + 200, self.settings.screen_height - 216 - 25))  # Platform 1
        self.enemies.append(Enemy(self, 4300 + 200, self.settings.screen_height - 216 - 25))  # Platform 2
        self.enemies.append(Enemy(self, 5800 + 150, self.settings.screen_height - 240 - 25))  # Platform 3
        self.enemies.append(Enemy(self, 6400 + 200, self.settings.screen_height - 426 - 25))  # Platform 4
        self.enemies.append(Enemy(self, 7100 + 200, self.settings.screen_height - 628 - 25))  # Platform 5

    def run_game(self):
        """Start the main loop for the game."""

        # Play background music
        pygame.mixer.music.play(-1)  # loops indefinitely

        level_complete_collided = False  # Track if collision with level complete object has occurred

        while True:
            self._check_events()
            if self.stats.game_active:
                self.player.update()
                self.player.draw()
                self._update_camera()
                self._check_collisions()
                self._update_enemies()
                self.stats.update_time()

                # Check if player reached level complete object
                if pygame.sprite.collide_rect(self.player, self.level_complete):
                    if not level_complete_collided:  # Only open the chest if not already opened
                        self.level_complete.open()
                        level_complete_collided = True  # Mark as collided to avoid reopening

            self._update_screen()

            # Check if game is not active
            if not self.stats.game_active:
                self._stop_music()  # Stop background music when game is not active
                # Check if player reached level complete object
                if pygame.sprite.collide_rect(self.player, self.level_complete):
                    # Set level to 2
                    self.stats.level = 2

    def _check_collisions(self):
        """Check for collisions between the player and obstacles, and between enemies and obstacles."""
        player_colliding = False
        for obstacle in self.obstacles:
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
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                # If player collides with any enemy, end the game
                self.stats.game_active = False
                break

        # Check collisions between enemies and obstacles
        for enemy in self.enemies:
            for obstacle in self.obstacles:
                if enemy.rect.colliderect(obstacle.rect):
                    if enemy.vertical_speed > 0 and enemy.rect.bottom > obstacle.rect.top and enemy.rect.top < obstacle.rect.top:
                        enemy.rect.bottom = obstacle.rect.top
                        enemy.y = enemy.rect.bottom
                        enemy.vertical_speed = 0

        # Check to see if player fell off the map
        if self.player.rect.y >= self.settings.screen_height + 200:
            self.stats.game_active = False

        # Check collision with level complete object
        adjusted_level_complete_rect = self.level_complete.rect.copy()
        adjusted_level_complete_rect.x -= self.camera_x
        if self.player.rect.colliderect(adjusted_level_complete_rect):
            self.level_complete.open()
            self.stats.level = 2

    def _check_events(self):
        """Watch for keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Responds to key presses."""
        if event.key == pygame.K_d:
            self.player.moving_right = True
        elif event.key == pygame.K_a:
            self.player.moving_left = True
        elif event.key == pygame.K_w:
            if not self.player.is_jumping:
                self.player.jumping = True

    def _check_keyup_events(self, event):
        """Responds to key releases."""
        if event.key == pygame.K_d:
            self.player.moving_right = False
        elif event.key == pygame.K_a:
            self.player.moving_left = False
        elif event.key == pygame.K_w:
            self.player.jumping = False
        elif event.key == pygame.K_q:
            sys.exit()

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
        for obstacle in self.obstacles:
            adjusted_obstacle_rect = obstacle.rect.copy()
            adjusted_obstacle_rect.x -= self.camera_x
            obstacle.draw(adjusted_obstacle_rect)
        for enemy in self.enemies:
            adjusted_enemy_rect = enemy.rect.copy()
            adjusted_enemy_rect.x -= self.camera_x
            enemy.draw(adjusted_enemy_rect)

        # Adjust the position of the level complete object
        adjusted_level_complete_rect = self.level_complete.rect.copy()
        adjusted_level_complete_rect.x -= self.camera_x
        self.level_complete.draw(self.screen, adjusted_level_complete_rect)  # Draw the level complete object

        self._draw_timer()
        pygame.display.flip()

    def _update_enemies(self):
        """Update the positions of all enemies in the game."""
        for enemy in self.enemies:
            enemy.check_edges(self.obstacles)
            enemy.update()

    def _draw_timer(self):
        """Draw the timer on the screen."""
        timer_text = f"Time: {self.stats.elapsed_time:.2f}s"
        timer_image = self.font.render(timer_text, True, (30, 30, 30))
        self.screen.blit(timer_image, (20, 20))

    def _stop_music(self):
        """Stop playing background music."""
        pygame.mixer.music.stop()

if __name__ == '__main__':
    pp = PythonPlatformer()
    pp.run_game()
