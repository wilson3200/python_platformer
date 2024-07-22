import pygame
from obstacle import Obstacle
from enemy import Enemy
from level_complete import LevelComplete

class LevelTwo:
    def __init__(self, pp_game):
        self.pp_game = pp_game
        self.obstacles = []
        self.enemies = []
        self.level_complete = LevelComplete(self.pp_game, 10_000, self.pp_game.settings.screen_height - 48)
        self._create_obstacles()
        self._create_enemies()

        # Load background music
        pygame.mixer.music.load('connected.ogg')
        pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
        pygame.mixer.music.play(-1)  # loops indefinitely

    def _create_obstacles(self):
        """Create obstacles and ground for level two."""
        self.obstacles.append(Obstacle(self.pp_game, 0, self.pp_game.settings.screen_height - 16, 2000, 16))
        self.obstacles.append(Obstacle(self.pp_game, 2200, self.pp_game.settings.screen_height - 16, 1000, 16))
        self.obstacles.append(Obstacle(self.pp_game, 3500, self.pp_game.settings.screen_height - 200, 500, 16))
        self.obstacles.append(Obstacle(self.pp_game, 4500, self.pp_game.settings.screen_height - 300, 800, 16))
        self.obstacles.append(Obstacle(self.pp_game, 5500, self.pp_game.settings.screen_height - 100, 600, 16))
        self.obstacles.append(Obstacle(self.pp_game, 6500, self.pp_game.settings.screen_height - 400, 700, 16))
        self.obstacles.append(Obstacle(self.pp_game, 7500, self.pp_game.settings.screen_height - 200, 900, 16))
        self.obstacles.append(Obstacle(self.pp_game, 8500, self.pp_game.settings.screen_height - 500, 1000, 16))
        self.obstacles.append(Obstacle(self.pp_game, 9500, self.pp_game.settings.screen_height - 200, 250, 16))
        self.obstacles.append(Obstacle(self.pp_game, 10000, 0, 16, self.pp_game.settings.screen_height, tile_index=1))

    def _create_enemies(self):
        """Create enemies for level two."""
        self.enemies.append(Enemy(self.pp_game, 500, self.pp_game.settings.screen_height - 16 - 25))
        self.enemies.append(Enemy(self.pp_game, 2500, self.pp_game.settings.screen_height - 16 - 25))
        self.enemies.append(Enemy(self.pp_game, 3700, self.pp_game.settings.screen_height - 200 - 25))
        self.enemies.append(Enemy(self.pp_game, 4700, self.pp_game.settings.screen_height - 300 - 25))
        self.enemies.append(Enemy(self.pp_game, 5600, self.pp_game.settings.screen_height - 100 - 25))
        self.enemies.append(Enemy(self.pp_game, 6600, self.pp_game.settings.screen_height - 400 - 25))
        self.enemies.append(Enemy(self.pp_game, 7700, self.pp_game.settings.screen_height - 200 - 25))
        self.enemies.append(Enemy(self.pp_game, 8600, self.pp_game.settings.screen_height - 500 - 25))
        self.enemies.append(Enemy(self.pp_game, 9700, self.pp_game.settings.screen_height - 16))

    def set_player_position(self):
        """Set the player's initial position for level two."""
        self.pp_game.player.rect.topleft = (100, self.pp_game.settings.screen_height - 100)  # Start near the left edge
        self.pp_game.player.x = float(self.pp_game.player.rect.x)
        self.pp_game.player.y = float(self.pp_game.player.rect.y)

    def update(self):
        """Update level two elements."""
        for enemy in self.enemies:
            enemy.check_edges(self.obstacles)
            enemy.update()

    def draw(self):
        """Draw level two elements."""
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
