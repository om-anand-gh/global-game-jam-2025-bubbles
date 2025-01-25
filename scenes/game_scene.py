from scenes.base_scene import BaseScene
from components.button import Button

class GameScene(BaseScene):
    def __init__(self, window):
        super().__init__(window, "assets/images/background/background_game.png")
        
        
        self.main_menu_button = Button(
            x=window.width  - 100,
            y=window.height - 50,
            size="medium",
            text="Main Menu",
            on_click=self.return_to_menu
        )

        self.elements.append(self.main_menu_button)

    def return_to_menu(self):
        # Import MenuScene here to avoid circular import
        from scenes.menu_scene import MenuScene
        self.window.switch_scene(MenuScene(self.window))