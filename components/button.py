import pyglet

import config
from utils.resource_loader import load_image


class Button:
    SIZES = {
        "small": "button_small.png",
        "medium": "button_medium.png",
        "large": "button_large.png",
    }

    def __init__(self, x, y, size="medium", text="", font_size=32, color=(0, 0, 0, 255), on_click=None):
        # Validate size
        if size not in self.SIZES:
            raise ValueError(f"Invalid size '{size}'. Choose from: {', '.join(self.SIZES.keys())}.")

        # Load the button image
        self.image = load_image(self.SIZES[size])
        self.sprite = pyglet.sprite.Sprite(
            self.image,
            x=x - self.image.width // 2,
            y=y - self.image.height // 2
        )


        # Create the label for the button's text
        self.label = pyglet.text.Label(
            text,
            font_name=config.FONT,
            font_size=font_size,
            x=x,
            y=y,
            anchor_x="center",
            anchor_y="center",
            color=color,  
        )

        # Click callback
        self.on_click = on_click

    def draw(self):
        # Draw the button sprite
        self.sprite.draw()

        # Draw the button text
        self.label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Check if the click is within the button bounds
        if (
            self.sprite.x <= x <= self.sprite.x + self.sprite.width and
            self.sprite.y <= y <= self.sprite.y + self.sprite.height
        ):
            if self.on_click:
                self.on_click()
