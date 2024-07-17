import tkinter as tk
from python_platformer import PythonPlatformer

class HomeScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Home Screen")

        # Create a label for title
        self.title_label = tk.Label(master, text="Welcome to Python Platformer Game", font=("Helvetica", 18))
        self.title_label.pack(pady=20)

        # Create a play button
        self.play_button = tk.Button(master, text="Play", width=20, height=2, command=self.start_game)
        self.play_button.pack()

    def start_game(self):
        """Function to start the PythonPlatformer game."""
        # Close the Tkinter window
        self.master.destroy()

        # Start the PythonPlatformer game
        game = PythonPlatformer()
        game.run_game()

def main():
    root = tk.Tk()
    app = HomeScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()

