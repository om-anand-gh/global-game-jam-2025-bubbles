import pyglet
from utils.resource_loader import load_image


class Market:
    TREND_EFFECT = {
        "up": 1.1,      # Increase market size by 10%
        "neutral": 1.0, # No change
        "down": 0.9,    # Decrease market size by 10%
    }

    def __init__(self, coin: str, x: float, y: float, initial_size: float = 10, tint=(255, 255, 255)):
        """
        Initializes the Market component for a specific coin.

        Args:
            coin (str): The name of the coin this market represents.
            x (float): The x-coordinate for the market's bubble.
            y (float): The y-coordinate for the market's bubble.
            initial_size (float): The initial size of the market bubble.
        """
        self.coin = coin
        self.x = x
        self.y = y
        self.size = initial_size
        self.target_size = initial_size
        self.animation_speed = 5.0  # Size units per second

        # Load the bubble asset for the market
        self.image_bubble = load_image("bubble/happy_neutral.png")  # Replace with your bubble asset
        self.sprite_bubble = pyglet.sprite.Sprite(
            self.image_bubble, x=self.x, y=self.y
        )

        # Set the tint color
        self.sprite_bubble.color = tint

        # Set the initial scale
        self.update_bubble_scale()

    def update_bubble_scale(self):
        """Updates the size of the bubble based on the current market size."""
        scale_factor = self.size / 100  # Assuming the default size corresponds to 100
        self.sprite_bubble.scale = scale_factor
        self.sprite_bubble.x = self.x - self.sprite_bubble.width / 2
        self.sprite_bubble.y = self.y - self.sprite_bubble.height / 2

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
            raise ValueError(f"Invalid trend '{trend}'. Must be 'up', 'neutral', or 'down'.")

        # Update the target market size
        self.target_size *= self.TREND_EFFECT[trend]

    def draw(self):
        """Draws the market bubble."""
        self.sprite_bubble.draw()
