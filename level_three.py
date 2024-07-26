import pygame
from obstacle import Obstacle
from enemy import Enemy
from enemy import Enemy2
from level_complete import LevelComplete

class LevelThree:
    def __init__(self, pp_game):
        self.pp_game = pp_game
        self.obstacles = []
        self.enemies = []
        self.level_complete = LevelComplete(self.pp_game, 10_550, self.pp_game.settings.screen_height - 48)
        self._create_obstacles()
        self._create_enemies()

        # Load background music
        pygame.mixer.music.load('candy.ogg')
        pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
        pygame.mixer.music.play(-1)  # loops indefinitely

    def _create_obstacles(self):
        """Create obstacles and ground for level three."""
        self.obstacles.append(Obstacle(self.pp_game, -400, self.pp_game.settings.screen_height - 16, 830, 16))
        self.obstacles.append(Obstacle(self.pp_game, 900, self.pp_game.settings.screen_height - 250, 400, 16))
        self.obstacles.append(Obstacle(self.pp_game, 1700, self.pp_game.settings.screen_height - 575, 600, 16))
        self.obstacles.append(Obstacle(self.pp_game, 2750, self.pp_game.settings.screen_height - 575, 100, 16))
        self.obstacles.append(Obstacle(self.pp_game, 3300, self.pp_game.settings.screen_height - 300, 100, 16))
        self.obstacles.append(Obstacle(self.pp_game, 3800, self.pp_game.settings.screen_height - 650, 250, 16))
        self.obstacles.append(Obstacle(self.pp_game, 4500, self.pp_game.settings.screen_height - 750, 700, 16))
        self.obstacles.append(Obstacle(self.pp_game, 5900, self.pp_game.settings.screen_height - 50, 800, 16))
        self.obstacles.append(Obstacle(self.pp_game, 5700, self.pp_game.settings.screen_height - 650, 1200, 16))
        self.obstacles.append(Obstacle(self.pp_game, 7100, self.pp_game.settings.screen_height - 220, 670, 16))
        self.obstacles.append(Obstacle(self.pp_game, 8200, self.pp_game.settings.screen_height - 500, 500, 16))
        self.obstacles.append(Obstacle(self.pp_game, 9_200, self.pp_game.settings.screen_height - 200, 600, 16))
        self.obstacles.append(Obstacle(self.pp_game, 10_500, self.pp_game.settings.screen_height - 16, 125, 16))

        # Walls
        self.obstacles.append(Obstacle(self.pp_game, 10600, 0, 16, self.pp_game.settings.screen_height, tile_index=1))

    def _create_enemies(self):
        """Create enemies for level three."""
        self.enemies.append(Enemy(self.pp_game, 400, self.pp_game.settings.screen_height - 16 - 25))
        self.enemies.append(Enemy2(self.pp_game, 1000, self.pp_game.settings.screen_height - 260 - 25))
        self.enemies.append(Enemy(self.pp_game, 2100, self.pp_game.settings.screen_height - 600 - 25))
        self.enemies.append(Enemy2(self.pp_game, 4700, self.pp_game.settings.screen_height - 800 - 25))
        self.enemies.append(Enemy(self.pp_game, 5600, self.pp_game.settings.screen_height - 100 - 25))
        self.enemies.append(Enemy2(self.pp_game, 6000, self.pp_game.settings.screen_height - 700 - 25))
        self.enemies.append(Enemy(self.pp_game, 6600, self.pp_game.settings.screen_height - 400 - 25))
        self.enemies.append(Enemy(self.pp_game, 7200, self.pp_game.settings.screen_height - 200 - 25))
        self.enemies.append(Enemy2(self.pp_game, 8300, self.pp_game.settings.screen_height - 200 - 25))
        self.enemies.append(Enemy2(self.pp_game, 9500, self.pp_game.settings.screen_height - 550 - 25))

    def set_player_position(self):
        """Set the player's initial position for level three."""
        self.pp_game.player.rect.topleft = (-300, self.pp_game.settings.screen_height - 100)  # Start near the left edge
        self.pp_game.player.x = float(self.pp_game.player.rect.x)
        self.pp_game.player.y = float(self.pp_game.player.rect.y)

    def update(self):
        """Update level three elements."""
        for enemy in self.enemies:
            enemy.check_edges(self.obstacles)
            enemy.update()

    def draw(self):
        """Draw level three elements."""
        for obstacle in self.obstacles:
            adjusted_obstacle_rect = obstacle.rect.copy()
            adjusted_obstacle_rect.x -= self.pp_game.camera_x
            obstacle.draw(adjusted_obstacle_rect)
        for enemy in self.enemies:
            adjusted_enemy_rect = enemy.rect.copy()
            adjusted_enemy_rect.x -= self.pp_game.camera_x
            enemy.draw(adjusted_enemy_rect)
        adjusted_level_complete_rect = self.level_complete.rect.copy()
        adjusted_level_complete_rect.x -= self.pp_game.camera_x
        self.level_complete.draw(self.pp_game.screen, adjusted_level_complete_rect)
