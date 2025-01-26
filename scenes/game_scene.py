import random

import pyglet

import config
from scenes.base_scene import BaseScene
from components.button import Button
from components.bubbler_post import BubblerPost
from components.market import Market

class GameScene(BaseScene):
    def __init__(self, window):
        super().__init__(window, "assets/images/background/background_game.png")

        self.main_menu_button = Button(
            x=window.width - 100,
            y=window.height - 50,
            size="medium",
            text="Main Menu",
            on_click=self.return_to_menu,
        )

        self.elements = [self.main_menu_button]
        self.posts = []
        self.markets = {
            "banana": Market(coin="banana", x=400, y=400, tint=(255, 255, 0)),
            "beanie": Market(coin="beanie", x=800, y=400, tint=(255, 0, 0)),
            "headphone": Market(coin="headphone", x=400, y=200),
            "glasses": Market(coin="glasses", x=800, y=200),
            "tophat": Market(coin="tophat", x=600, y=300),
        }

        # Schedule random post creation every 2 seconds
        pyglet.clock.schedule_interval(self.add_random_post, config.NEW_POST_FREQUENCY)

    def add_random_post(self, dt):
        """Adds a new post with random attributes."""
        profile_picture = random.choice(list(BubblerPost.PROFILE_PICTURE.keys()))
        coin = random.choice(list(self.markets.keys()))
        trend = random.choices(
            population=list(BubblerPost.TREND.keys()),
            weights=[45, 10, 45],  # Probabilities: 40% down, 20% neutral, 40% up
            k=1  # Number of items to pick
        )[0]

        new_post = BubblerPost(
            profile_picture=profile_picture,
            coin=coin,
            trend=trend,
        )
        self.posts.append(new_post)

        # Update the market size based on the trend
        self.markets[coin].apply_trend(trend)

    def draw(self):
        super().draw()
        
        # Draw the markets
        for market in self.markets.values():
            market.draw()

        # Draw the posts
        for post in self.posts:
            post.draw()

    def update(self, dt):
        # Update markets' animation
        for market in self.markets.values():
            market.animate_size(dt)

        for post in self.posts[:]:
            post.update_position()
            if post.is_out_of_bounds():
                self.posts.remove(post)

    def return_to_menu(self):
        # Import MenuScene here to avoid circular import
        from scenes.menu_scene import MenuScene

        self.window.switch_scene(MenuScene(self.window))
