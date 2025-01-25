from pyglet.app import run
from game_window import GameWindow
from config import WINDOW_HEIGHT, WINDOW_WIDTH, GAME_TITLE
if __name__ == "__main__":
    window = GameWindow(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, caption=GAME_TITLE)
    run()  # Starts the Pyglet event loop
