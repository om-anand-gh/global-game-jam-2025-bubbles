import pyglet

from utils.resource_loader import load_image


class BubblerPost:
    PROFILE_PICTURE = {
        "beanie_glasses": "bubbler/bubbler_user_beanie_glasses.png",
        "beanie_headphone": "bubbler/bubbler_user_beanie_headphone.png",
    }
    COIN = {
        "banana": "coin/coin_banana.png",
        "beanie": "coin/coin_beanie.png",
    }
    TREND = {
        "down": "bubbler/bubbler_trend_down.png",
        "neutral": "bubbler/bubbler_trend_neutral.png",
        "up": "bubbler/bubbler_trend_up.png",
    }

    POSTION = (0, 1 ,2)

    x = 100
    y = 100

    def __init__(self, position: int, profile_picture: str, coin: str, trend: str):
        # Validate profile_picture
        if profile_picture not in self.PROFILE_PICTURE:
            raise ValueError(
                f"Invalid profile_picture '{profile_picture}'. Choose from: {', '.join(self.PROFILE_PICTURE.keys())}."
            )
        
        # Validate coin
        if coin not in self.COIN:
            raise ValueError(
                f"Invalid coin '{coin}'. Choose from: {', '.join(self.COIN.keys())}."
            )
        
        # Validate trend
        if trend not in self.TREND:
            raise ValueError(
                f"Invalid trend '{trend}'. Choose from: {', '.join(self.TREND.keys())}."
            )
        
        # Validate trend
        if position not in self.POSTION:
            raise ValueError(
                f"Invalid position '{position}'. Choose from: {', '.join(self.POSTION)}."
            )

        # Load the post image
        self.image_post = load_image("bubbler/bubbler_post.png")
        self.sprite_post = pyglet.sprite.Sprite(
            self.image_post, x=self.x, y=self.y + position * 100
        )

        # Load the profile picture image
        self.image_profile_picture = load_image(self.PROFILE_PICTURE[profile_picture])
        self.sprite_profile_picture = pyglet.sprite.Sprite(
            self.image_profile_picture, x=self.x + 10, y=self.y + position * 100 + 10
        )



    def draw(self):
        # Draw the post
        self.sprite_post.draw()

        # Draw the profile picture
        self.sprite_profile_picture.draw()
