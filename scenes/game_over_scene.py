import pyglet

import config
from scenes.base_scene import BaseScene

from components.button import Button

class GameOverScene(BaseScene):
    def __init__(self, window):
        super().__init__(window, "assets/images/background/background_game_over.png")


        # Create a button
        self.main_menu_button = Button(
            x=window.width // 2,
            y=window.height // 3,
            size="medium",
            text="Main Menu",
            on_click=self.return_to_main_menu
        )

        
        # Create a text label
        self.credit_label = pyglet.text.Label(
            "Made by Ben, Gowri, Om & Tolson",
            font_size=32,
            font_name=config.FONT,
            x=window.width // 2,
            y=20,
            anchor_x="center",
            anchor_y="bottom",
            color=(255, 255, 255, 255)  # White color
        )

        self.elements = [self.main_menu_button, self.credit_label]
    
    def return_to_main_menu(self):
        self.stop_music()
        from scenes.menu_scene import MenuScene
        # Logic to switch scenes
        self.window.switch_scene(MenuScene(self.window))
