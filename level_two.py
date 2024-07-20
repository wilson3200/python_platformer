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
        pygame.mixer.music.load('box_jump.ogg')
        pygame.mixer.music.play(-1)  # loops indefinitely

    def _create_obstacles(self):
        """Create obstacles and ground for level two."""
        # Example: Add obstacles specific to level two
        self.obstacles.append(Obstacle(self.pp_game, 0, self.pp_game.settings.screen_height - 16, 2000, 16))
        # Add more obstacles

    def _create_enemies(self):
        """Create enemies for level two."""
        # Example: Add enemies specific to level two
        self.enemies.append(Enemy(self.pp_game, 2000, self.pp_game.settings.screen_height - 16 - 25))
        # Add more enemies

    def set_player_position(self):
        """Set the player's initial position for level two."""
        self.pp_game.player.rect.topleft = (500, self.pp_game.settings.screen_height - 100)  # Example position, adjust as needed
        self.pp_game.player.x = float(self.pp_game.player.rect.x)
        self.pp_game.player.y = float(self.pp_game.player.rect.y)

    def update(self):
        """Update level two elements."""
        # Update enemies and obstacles
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
        self.level_complete.draw(self.pp_game.screen, self.level_complete.rect)
