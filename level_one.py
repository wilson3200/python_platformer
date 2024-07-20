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

        # Load background music
        pygame.mixer.music.load('box_jump.ogg')
        pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
        pygame.mixer.music.play(-1)  # loops indefinitely

    def set_player_position(self):
        """Set the player's initial position for level one."""
        self.pp_game.player.rect.topleft = (500, self.pp_game.settings.screen_height - 100)  # Example position, adjust as needed
        self.pp_game.player.x = float(self.pp_game.player.rect.x)
        self.pp_game.player.y = float(self.pp_game.player.rect.y)

    def _create_obstacles(self):
        """Create obstacles and ground for level one."""
        # Example: Add obstacles specific to level one
        self.obstacles.append(Obstacle(self.pp_game, 0, self.pp_game.settings.screen_height - 16, 2000, 16))
        self.obstacles.append(Obstacle(self.pp_game, 3200, self.pp_game.settings.screen_height - 16, 800, 16))
        self.obstacles.append(Obstacle(self.pp_game, 5000, self.pp_game.settings.screen_height - 16, 600, 16))
        self.obstacles.append(Obstacle(self.pp_game, 8000, self.pp_game.settings.screen_height - 16, 2000, 16))
        self.obstacles.append(Obstacle(self.pp_game, 2300, self.pp_game.settings.screen_height - 216, 460, 16))
        self.obstacles.append(Obstacle(self.pp_game, 4300, self.pp_game.settings.screen_height - 216, 400, 16))
        self.obstacles.append(Obstacle(self.pp_game, 5800, self.pp_game.settings.screen_height - 240, 300, 16))
        self.obstacles.append(Obstacle(self.pp_game, 6400, self.pp_game.settings.screen_height - 426, 400, 16))
        self.obstacles.append(Obstacle(self.pp_game, 7100, self.pp_game.settings.screen_height - 628, 400, 16))
        self.obstacles.append(Obstacle(self.pp_game, 0, 0, 16, self.pp_game.settings.screen_height, tile_index=1))
        self.obstacles.append(Obstacle(self.pp_game, 10000, 0, 16, self.pp_game.settings.screen_height, tile_index=1))

    def _create_enemies(self):
        """Create enemies for level one."""
        self.enemies.append(Enemy(self.pp_game, 1000, self.pp_game.settings.screen_height - 16 - 25))
        self.enemies.append(Enemy(self.pp_game, 3200 + 400, self.pp_game.settings.screen_height - 16 - 25))
        self.enemies.append(Enemy(self.pp_game, 5000 + 300, self.pp_game.settings.screen_height - 16 - 25))
        self.enemies.append(Enemy(self.pp_game, 8000 + 1000, self.pp_game.settings.screen_height - 16 - 25))
        self.enemies.append(Enemy(self.pp_game, 2300 + 200, self.pp_game.settings.screen_height - 216 - 25))
        self.enemies.append(Enemy(self.pp_game, 4300 + 200, self.pp_game.settings.screen_height - 216 - 25))
        self.enemies.append(Enemy(self.pp_game, 5800 + 150, self.pp_game.settings.screen_height - 240 - 25))
        self.enemies.append(Enemy(self.pp_game, 6400 + 200, self.pp_game.settings.screen_height - 426 - 25))
        self.enemies.append(Enemy(self.pp_game, 7100 + 200, self.pp_game.settings.screen_height - 628 - 25))

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
        adjusted_level_complete_rect = self.level_complete.rect.copy()
        adjusted_level_complete_rect.x -= self.pp_game.camera_x
        self.level_complete.draw(self.pp_game.screen, adjusted_level_complete_rect)
