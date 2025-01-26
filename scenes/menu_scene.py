import pyglet

from scenes.base_scene import BaseScene

from components.button import Button

class MenuScene(BaseScene):
    def __init__(self, window):
        super().__init__(window, "assets/images/background/background_main_menu.png")


        # Create a button
        self.start_button = Button(
            x=window.width // 2,
            y=window.height // 2,
            size="medium",
            text="start",
            on_click=self.start_game
        )

        self.exit_button = Button(
            x=window.width // 2,
            y=(window.height // 2) - 100,
            size="medium",
            text="Exit",
            on_click=self.exit_game
        )

        # Store elements in a list for event handling
        self.elements = [self.start_button, self.exit_button]
    
    def start_game(self):
        self.stop_music()
        from scenes.game_scene import GameScene
        # Logic to switch scenes
        self.window.switch_scene(GameScene(self.window))

    def exit_game(self):
        # Logic to exit the game
        print("Calling exit")
        pyglet.app.exit()
