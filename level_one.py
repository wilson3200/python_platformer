# level_one.py
import pygame
from obstacle import Obstacle
from enemy import Enemy
from level_complete import LevelComplete

class LevelOne:
    def __init__(self, pp_game):
        self.pp_game = pp_game
        self.obstacles = []
        self.enemies = []
        self.level_complete = LevelComplete(self.pp_game, 9_950, self.pp_game.settings.screen_height - 48)
        self._create_obstacles()
        self._create_enemies()

    def _create_obstacles(self):
        """Create obstacles and ground for level one."""
        # Example: Add obstacles specific to level one
        self.obstacles.append(Obstacle(self.pp_game, 0, self.pp_game.settings.screen_height - 16, 2000, 16))
        # Add more obstacles

    def _create_enemies(self):
        """Create enemies for level one."""
        # Example: Add enemies specific to level one
        self.enemies.append(Enemy(self.pp_game, 1000, self.pp_game.settings.screen_height - 16 - 25))
        # Add more enemies

    def update(self):
        """Update level one elements."""
        for enemy in self.enemies:
            enemy.check_edges(self.obstacles)
            enemy.update()

    def draw(self):
        """Draw level one elements."""
        for obstacle in self.obstacles:
            adjusted_obstacle_rect = obstacle.rect.copy()
            adjusted_obstacle_rect.x -= self.pp_game.camera_x
            obstacle.draw(adjusted_obstacle_rect)
        for enemy in self.enemies:
            adjusted_enemy_rect = enemy.rect.copy()
            adjusted_enemy_rect.x -= self.pp_game.camera_x
            enemy.draw(adjusted_enemy_rect)
        self.level_complete.draw(self.pp_game.screen, self.level_complete.rect)
