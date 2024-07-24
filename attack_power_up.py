import pygame

class AttackPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('attack_powerup.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        # Update logic for the power-up if needed
        pass