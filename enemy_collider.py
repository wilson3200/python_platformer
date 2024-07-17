import pygame

class EnemyCollider:
    """Class to manage enemy colliders."""

    def __init__(self, pp_game, x, y, width, height):
        """Initialize the collider and set its position."""
        self.screen = pp_game.screen
        self.settings = pp_game.settings
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)  # Red color for debugging

    def draw(self):
        """Draw the collider to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect, 2)
