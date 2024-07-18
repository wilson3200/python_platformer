import pygame
class LevelComplete(pygame.sprite.Sprite):
    """A class to represent the end point of each level."""
    def __init__(self, pp_game, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 255, 0))  # Green color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen, rect):
        """Draw the level complete object on the screen."""
        screen.blit(self.image, rect)
