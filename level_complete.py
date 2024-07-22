import pygame

class LevelComplete(pygame.sprite.Sprite):
    """A class to represent the end point of each level."""
    def __init__(self, pp_game, x, y):
        super().__init__()
        self.pp_game = pp_game
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)  # Use SRCALPHA for transparency
        self.sprite_sheet = pygame.image.load('chests.png').convert_alpha()
        self.closed_chest = self._get_image(0, 0)
        self.open_chest = self._get_image(2, 0)
        self.image.blit(self.closed_chest, (1, 1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.opened = False

        # Load the sound
        self.open_sound = pygame.mixer.Sound('CoinPickUp3.wav')

    def _get_image(self, col, row):
        """Extracts a sprite from the sprite sheet."""
        width, height = 16, 16
        image = pygame.Surface((width, height), pygame.SRCALPHA)  # Use SRCALPHA for transparency
        image.blit(self.sprite_sheet, (0, 0), (col * width, row * height, width, height))
        return pygame.transform.scale(image, (32, 32))

    def draw(self, screen, rect):
        """Draw the level complete object on the screen."""
        screen.blit(self.image, rect)

    def open(self):
        """Open the chest."""
        if not self.opened:
            self.opened = True
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA)  # Reset the surface
            self.image.blit(self.open_chest, (0, 0))  # Blit the opened chest image
            self.open_sound.play()  # Play the sound
            print("Chest opened!")  # Debug statement
        else:
            print("Chest already opened.")  # Additional debug statement