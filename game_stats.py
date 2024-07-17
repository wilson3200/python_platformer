import time

class GameStats:
    """Track statistics for Python Platformer."""

    def __init__(self, pp_game):
        """Initialize statistics."""
        self.settings = pp_game.settings
        self.reset_stats()
        self.game_active = True
        self.start_time = time.time()
        self.elapsed_time = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.score = 0
        self.level = 1

    def update_time(self):
        """Update the elapsed time."""
        self.elapsed_time = time.time() - self.start_time
