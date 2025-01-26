import pyglet

from scenes.base_scene import BaseScene

from components.button import Button

class GameOverScene(BaseScene):
    def __init__(self, window):
        super().__init__(window, "assets/images/background/background_game_over.png")


        # Create a button
        self.main_menu_button = Button(
            x=window.width // 2,
            y=window.height // 2,
            size="medium",
            text="Main Menu",
            on_click=self.return_to_main_menu
        )

        self.elements = [self.main_menu_button]
    
    def return_to_main_menu(self):
        self.stop_music()
        from scenes.menu_scene import MenuScene
        # Logic to switch scenes
        self.window.switch_scene(MenuScene(self.window))
