import time

class GameStats:
    """Track statistics for Python Platformer."""

    def __init__(self, pp_game):
        self.pp_game = pp_game
        self.reset_stats()
        self.game_active = True
        self.level = 1
        self.level_complete_time = None  # Track when the level was completed

    def reset_stats(self):
        self.elapsed_time = 0.0
        self.start_time = time.time()  # Initialize the start time
        self.level = 1

    def update_time(self):
        """Update the elapsed time."""
        self.elapsed_time = time.time() - self.start_time
