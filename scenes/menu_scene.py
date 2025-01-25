import pyglet

class MenuScene:
    def __init__(self, window):
        self.window = window

        # Load the background image
        self.background_image = pyglet.resource.image("assets/images/main_menu_bg.png")
        self.background_sprite = pyglet.sprite.Sprite(self.background_image)

        # Center the background image in the window
        self.background_sprite.scale = max(
            window.width / self.background_image.width,
            window.height / self.background_image.height
        )
        self.background_sprite.x = (window.width - self.background_sprite.width) / 2
        self.background_sprite.y = (window.height - self.background_sprite.height) / 2

        # Label for the menu
        self.label = pyglet.text.Label(
            "Main Menu",
            font_name="Arial",
            font_size=36,
            x=window.width // 2,
            y=window.height // 2,
            anchor_x="center",
            anchor_y="center",
            color=(255, 255, 255, 255)  # White color
        )

    def draw(self):
        # Draw the background first
        self.background_sprite.draw()

        # Draw the label on top
        self.label.draw()

    def update(self, dt):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            # Switch to the GameScene when Enter is pressed
            from scenes.game_scene import GameScene
            self.window.switch_scene(GameScene(self.window))
