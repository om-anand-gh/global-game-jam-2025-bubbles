import pyglet

class GameScene:
    def __init__(self, window):
        self.window = window

        # Load player sprite
        self.player_image = pyglet.resource.image("assets/images/player.png")
        self.player_sprite = pyglet.sprite.Sprite(
            self.player_image,
            x=window.width // 2,
            y=window.height // 2
        )

        # Velocity for movement
        self.player_velocity_x = 0
        self.player_velocity_y = 0

        # Bind event handlers
        window.push_handlers(self)

    def draw(self):
        self.player_sprite.draw()

    def update(self, dt):
        # Update player position
        self.player_sprite.x += self.player_velocity_x * dt
        self.player_sprite.y += self.player_velocity_y * dt

        # Keep the player within the window bounds
        self.player_sprite.x = max(0, min(self.window.width - self.player_sprite.width, self.player_sprite.x))
        self.player_sprite.y = max(0, min(self.window.height - self.player_sprite.height, self.player_sprite.y))

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.player_velocity_y = 200
        elif symbol == pyglet.window.key.DOWN:
            self.player_velocity_y = -200
        elif symbol == pyglet.window.key.LEFT:
            self.player_velocity_x = -200
        elif symbol == pyglet.window.key.RIGHT:
            self.player_velocity_x = 200

    def on_key_release(self, symbol, modifiers):
        if symbol in (pyglet.window.key.UP, pyglet.window.key.DOWN):
            self.player_velocity_y = 0
        elif symbol in (pyglet.window.key.LEFT, pyglet.window.key.RIGHT):
            self.player_velocity_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        # Example: Switch back to MenuScene on mouse click
        if button == pyglet.window.mouse.LEFT:
            from scenes.menu_scene import MenuScene
            self.window.switch_scene(MenuScene(self.window))

    def cleanup(self):
        # Clean up event handlers when switching scenes
        self.window.remove_handlers(self)
