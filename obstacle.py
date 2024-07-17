import pygame

class Obstacle:
    """A class to represent an obstacle in the game."""

    def __init__(self, game, x, y, width, height, tile_index=None):
        """Initialize the obstacle."""
        self.screen = game.screen
        self.tileset = pygame.image.load('forest_tileset.png').convert_alpha()  # Load tileset image
        self.tile_size = 16  # Assuming each tile in the tileset is 16x16 pixels
        self.rect = pygame.Rect(x, y, width, height)
        self.tile_index = tile_index  # Optional tile index for custom tiles

    def draw(self, adjusted_rect):
        """Draw the obstacle using tiles from the tileset."""
        if self.tile_index is None:
            num_tiles_x = adjusted_rect.width // self.tile_size
            num_tiles_y = adjusted_rect.height // self.tile_size

            for y in range(num_tiles_y):
                for x in range(num_tiles_x):
                    tile_x = adjusted_rect.x + x * self.tile_size
                    tile_y = adjusted_rect.y + y * self.tile_size
                    tile_rect = pygame.Rect(tile_x, tile_y, self.tile_size, self.tile_size)

                    # Alternate between grass (index 0) and dirt (index 2)
                    if (x + y) % 2 == 0:
                        tile_index = 0  # Grass tile index
                    else:
                        tile_index = 1  # Dirt tile index

                    tile = self.tileset.subsurface((tile_index * self.tile_size, 0, self.tile_size, self.tile_size))
                    self.screen.blit(tile, tile_rect)
        else:
            num_tiles_y = adjusted_rect.height // self.tile_size

            for y in range(num_tiles_y):
                tile_x = adjusted_rect.x
                tile_y = adjusted_rect.y + y * self.tile_size
                tile_rect = pygame.Rect(tile_x, tile_y, self.tile_size, self.tile_size)

                # Use the specified tile_index for the entire height of the obstacle
                tile = self.tileset.subsurface((self.tile_index * self.tile_size, 0, self.tile_size, self.tile_size))
                self.screen.blit(tile, tile_rect)
