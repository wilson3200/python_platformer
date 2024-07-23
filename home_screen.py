import tkinter as tk
import pygame
from python_platformer import PythonPlatformer

class HomeScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Home Screen")

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load the button select sound
        self.select_sound = pygame.mixer.Sound('select.wav')

        # Get the screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Set the window size to the screen dimensions
        self.master.geometry(f"{screen_width}x{screen_height}")

        # Maximize the window
        self.master.state('zoomed')

        # Create a frame for the content
        self.content_frame = tk.Frame(master)
        self.content_frame.pack(expand=True)

        # Create a label for title
        self.title_label = tk.Label(self.content_frame, text="Python Platformer", font=("Helvetica", 24))
        self.title_label.pack(pady=40)

        # Create a "Start AI" button
        self.start_ai_button = tk.Button(self.content_frame, text="Start AI", width=20, height=2, command=self.start_ai)
        self.start_ai_button.pack(pady=10)

        # Create a "Play" button
        self.play_button = tk.Button(self.content_frame, text="Play", width=20, height=2, command=self.start_game)
        self.play_button.pack(pady=10)

        # Create a "Quit" button
        self.quit_button = tk.Button(self.content_frame, text="Quit", width=20, height=2, command=self.quit_game)
        self.quit_button.pack(pady=10)

    def start_ai(self):
        """Function to handle the "Start AI" button click."""
        self.select_sound.play()  # Play the select sound
        # This function does nothing for now
        pass

    def start_game(self):
        """Function to start the PythonPlatformer game."""
        self.select_sound.play()  # Play the select sound
        # Close the Tkinter window
        self.master.destroy()

        # Start the PythonPlatformer game
        game = PythonPlatformer()
        game.run_game()

    def quit_game(self):
        """Function to quit the application."""
        self.select_sound.play()  # Play the select sound
        self.master.quit()

def main():
    root = tk.Tk()
    app = HomeScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
