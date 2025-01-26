import pyglet

import config
from utils.resource_loader import load_audio, load_image


class Market:
    TREND_EFFECT = {
        "up": 1.1,  # Increase market size by 10%
        "neutral": 1.0,  # No change
        "down": 0.9,  # Decrease market size by 10%
    }

    def __init__(
        self,
        coin_id: str,
        coin: str,
        x: float,
        y: float,
        initial_size: float = 100,
        tint=(255, 255, 255),
    ):
        """
        Initializes the Market component for a specific coin.

        Args:
            coin (str): The name of the coin this market represents.
            x (float): The x-coordinate for the market's bubble.
            y (float): The y-coordinate for the market's bubble.
            initial_size (float): The initial size of the market bubble.
        """
        self.coin_id = coin_id
        self.coin = coin
        self.x = x
        self.y = y
        self.size = initial_size
        self.target_size = initial_size
        self.animation_speed = 5.0  # Size units per second
        self.color = tint

        # Load the bubble asset for the market
        self.image_bubble = load_image("bubble/bubble_empty.png")
        self.sprite_bubble = pyglet.sprite.Sprite(self.image_bubble)

        # Set the tint color
        self.sprite_bubble.color = tint

        # Load the bubble eye asset
        self.image_bubble_eye = load_image("bubble/bubble_face_happy.png")
        self.sprite_bubble_eye = pyglet.sprite.Sprite(self.image_bubble_eye)

        # Load the additional asset based on the coin
        self.image_coin = load_image(config.COIN[coin])
        self.sprite_coin = pyglet.sprite.Sprite(self.image_coin)

        # Scale the additional asset to half the initial size
        self.sprite_coin.scale = initial_size / 200  # Divide by 200 for half the size (100 is full)
        self.sprite_coin.x = self.x - (self.sprite_coin.width * self.sprite_coin.scale) / 2
        self.sprite_coin.y = self.y - (self.sprite_coin.height * self.sprite_coin.scale) / 2
        self.sprite_coin.color = tint


        # Load the pop asset
        self.image_pop = load_image("bubble/pop_neutral.png")  # Replace with the actual pop asset
        self.sprite_pop = pyglet.sprite.Sprite(self.image_pop)
        self.sprite_pop.color = tint
        self.is_popping = False  # Flag to indicate if the bubble is in the popping state
        

        # Set the initial scale and position
        self.update_bubble_scale()

    def update_bubble_scale(self):
        """Updates the size and position of the bubble based on the current market size."""
        scale_factor = self.size / 100  # Assuming the default size corresponds to 100
        self.sprite_bubble.scale = scale_factor
        self.sprite_bubble.x = self.x - (self.sprite_bubble.width * scale_factor) / 2
        self.sprite_bubble.y = self.y - (self.sprite_bubble.height * scale_factor) / 2

        self.sprite_bubble_eye.scale = scale_factor
        self.sprite_bubble_eye.x = self.x - (self.sprite_bubble_eye.width * scale_factor) / 2
        self.sprite_bubble_eye.y = self.y - (self.sprite_bubble_eye.height * scale_factor) / 2

        # Keep sprite_coin centered (independent of scale)
        self.sprite_coin.x = self.x - (self.sprite_coin.width * self.sprite_coin.scale) / 2
        self.sprite_coin.y = self.y - (self.sprite_coin.height * self.sprite_coin.scale) / 2



    def animate_size(self, dt):
        """Animates the market size towards the target size."""
        if abs(self.size - self.target_size) < 0.1:  # Stop if close enough
            self.size = self.target_size
        else:
            # Smoothly interpolate towards the target size
            direction = 1 if self.size < self.target_size else -1
            self.size += direction * self.animation_speed * dt

        # Update the bubble's scale
        self.update_bubble_scale()

    def apply_trend(self, trend: str):
        """
        Adjusts the market size based on the trend.

        Args:
            trend (str): The trend direction ("up", "neutral", "down").
        """
        if trend not in self.TREND_EFFECT:
            raise ValueError(
                f"Invalid trend '{trend}'. Must be 'up', 'neutral', or 'down'."
            )

        # Update the target market size
        self.target_size *= self.TREND_EFFECT[trend]

    def draw(self):
        """Draws the market bubble."""
        if self.is_popping:
            self.sprite_pop.draw()
        else:
            self.sprite_coin.draw()
            self.sprite_bubble.draw()
            self.sprite_bubble_eye.draw()
    
    def get_center(self):
        """
        Returns the center (x, y) of the market bubble, considering scaling.
        """
        center_x = self.sprite_bubble.x + (self.sprite_bubble.width * self.sprite_bubble.scale) / 2
        center_y = self.sprite_bubble.y + (self.sprite_bubble.height * self.sprite_bubble.scale) / 2
        return center_x, center_y

    def get_bounding_box(self):
        """
        Returns the bounding box of the bubble sprite as (left, right, top, bottom).
        Considers the sprite's scale and position.

        Returns:
            tuple: (left, right, top, bottom) coordinates of the sprite's bounding box.
        """
        left = self.sprite_bubble.x
        right = self.sprite_bubble.x + (self.sprite_bubble.width * self.sprite_bubble.scale)
        bottom = self.sprite_bubble.y
        top = self.sprite_bubble.y + (self.sprite_bubble.height * self.sprite_bubble.scale)
        return left, right, top, bottom
    
    def should_pop(self):
        """
        Determines if the market bubble should pop.
        The bubble pops if 80% of its size is smaller than or equal to the coin size.

        Returns:
            bool: True if the bubble should pop, False otherwise.
        """
        bubble_radius = (self.sprite_bubble.width * self.sprite_bubble.scale) / 2
        coin_radius = (self.sprite_coin.width * self.sprite_coin.scale) / 2
        if 0.8 * bubble_radius <= coin_radius:
            self.is_popping = True
            # Play audio when the object is to be popped
            sound = load_audio("bubble_pop_audio.mp3")
            sound.play()
            return True
        return False

    def show_pop_asset(self):
        """Replaces the bubble and coin with the pop asset."""
        self.sprite_pop.x = self.sprite_bubble.x
        self.sprite_pop.y = self.sprite_bubble.y
        self.sprite_pop.height = self.sprite_bubble.height
        self.sprite_pop.width = self.sprite_bubble.width
