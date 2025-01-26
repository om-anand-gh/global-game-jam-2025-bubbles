import pyglet

import config
from utils.resource_loader import load_image

class BubblerPost:
    PROFILE_PICTURE = {
        "beanie_glasses": "bubbler/bubbler_user_beanie_glasses.png",
        "beanie_headphone": "bubbler/bubbler_user_beanie_headphone.png",
        "glasses": "bubbler/bubbler_user_glasses.png",
        "headphone": "bubbler/bubbler_user_headphone.png",
        "beanie": "bubbler/bubbler_user_beanie.png",
        "plain_blue": "bubbler/bubbler_user_plain_blue.png",
        "plain_green": "bubbler/bubbler_user_plain_green.png",
        "plain_purple": "bubbler/bubbler_user_plain_purple.png",
    }
    TREND = {
        "down": "bubbler/bubbler_trend_down.png",
        "neutral": "bubbler/bubbler_trend_neutral.png",
        "up": "bubbler/bubbler_trend_up.png",
    }

    def __init__(self, profile_picture: str, coin: str, trend: str, tint=(255, 255, 255)):
        # Validate profile_picture
        if profile_picture not in self.PROFILE_PICTURE:
            raise ValueError(
                f"Invalid profile_picture '{profile_picture}'. Choose from: {', '.join(self.PROFILE_PICTURE.keys())}."
            )
        
        # Validate coin
        if coin not in config.COIN:
            raise ValueError(
                f"Invalid coin '{coin}'. Choose from: {', '.join(config.COIN.keys())}."
            )
        
        # Validate trend
        if trend not in self.TREND:
            raise ValueError(
                f"Invalid trend '{trend}'. Choose from: {', '.join(self.TREND.keys())}."
            )
        
        window = next(iter(pyglet.app.windows))

        # Set initial position
        self.x = 0.03 * window.width
        self.y = 0.71 * window.height
        self.speed = config.SCROLL_SPEED  # Pixels per frame

        # Load the post image
        self.image_post = load_image("bubbler/bubbler_post.png")
        self.sprite_post = pyglet.sprite.Sprite(self.image_post, x=self.x, y=self.y)
        
        # Scale the post
        scale_factor = (0.175 * window.width) / self.sprite_post.width
        self.sprite_post.scale = scale_factor

        # Load and scale profile picture
        self.sprite_profile_picture = self.load_and_scale_sprite(
            self.PROFILE_PICTURE[profile_picture], 
            x_offset=0.05, 
            y_offset=0.1, 
            height_scale=0.8
        )

        # Load and scale coin
        self.sprite_coin = self.load_and_scale_sprite(
            config.COIN[coin], 
            x_offset=0.4, 
            y_offset=0.15, 
            height_scale=0.7
        )

        self.sprite_coin.color = tint

        # Load and scale trend
        self.sprite_trend = self.load_and_scale_sprite(
            self.TREND[trend], 
            x_offset=0.7, 
            y_offset=0.15, 
            height_scale=0.7
        )

    def update_position(self):
        """Updates the position to simulate scrolling."""
        self.y -= self.speed
        self.sprite_post.y  -= self.speed
        self.sprite_profile_picture.y  -= self.speed
        self.sprite_coin.y -= self.speed
        self.sprite_trend.y -= self.speed

    def is_out_of_bounds(self):
        """Checks if the post has scrolled off the screen."""
        window = next(iter(pyglet.app.windows))  # Get the first window
        return self.y < window.height * 0.4

    def draw(self):
        """Draws the post and its profile picture."""
        self.sprite_post.draw()
        self.sprite_profile_picture.draw()
        self.sprite_coin.draw()
        self.sprite_trend.draw()

    def load_and_scale_sprite(self, image_path, x_offset, y_offset, height_scale):
        """
        Loads an image, creates a sprite, scales it, and positions it.

        Args:
            image_path (str): Path to the image to load.
            x_offset (float): X-offset as a proportion of the post width.
            y_offset (float): Y-offset as a proportion of the post height.
            height_scale (float): Proportion of the post height to scale the sprite to.

        Returns:
            pyglet.sprite.Sprite: The created and scaled sprite.
        """
        image = load_image(image_path)
        sprite = pyglet.sprite.Sprite(image)

        # Scale to specified height
        target_height = height_scale * self.sprite_post.height
        scale_factor = target_height / sprite.height

        # Calculate square dimensions
        square_size = min(sprite.width * scale_factor, target_height)
        sprite.scale = square_size / max(sprite.width, sprite.height)

        # Update position
        sprite.update(
            x=self.x + (x_offset * self.sprite_post.width),
            y=self.y + (y_offset * self.sprite_post.height),
        )

        return sprite
