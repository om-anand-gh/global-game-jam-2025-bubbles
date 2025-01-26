import random
from itertools import product

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
        self.markets = {}

        self.colors = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            # (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            # (255, 165, 0),  # Orange
            # (128, 0, 128),  # Purple
            # # (0, 255, 255),  # Cyan
            # (255, 192, 203),  # Pink
            # # (128, 128, 0),  # Olive
            # # (0, 128, 128),  # Teal
            # (128, 0, 0),  # Maroon
            # (0, 128, 0),  # Dark Green
            # # (0, 0, 128),  # Navy
            # (128, 128, 128),  # Gray
            # (255, 105, 180),  # Hot Pink
        ]

        self.available_combinations = list(product(config.COIN.keys(), self.colors))

        # Schedule random coin creation every few seconds
        pyglet.clock.schedule_interval(
            self.randomly_create_coin, config.NEW_COIN_FREQUENCY
        )

        # Schedule random post creation every 2 seconds
        pyglet.clock.schedule_interval(self.add_random_post, config.NEW_POST_FREQUENCY)

    def add_random_post(self, dt):
        """Adds a new post with random attributes."""

        if not self.markets:
            return

        profile_picture = random.choice(list(BubblerPost.PROFILE_PICTURE.keys()))
        coin_id = random.choice(list(self.markets.keys()))
        trend = random.choices(
            population=list(BubblerPost.TREND.keys()),
            weights=[45, 10, 45],  # Probabilities: 40% down, 20% neutral, 40% up
            k=1,  # Number of items to pick
        )[0]

        new_post = BubblerPost(
            profile_picture=profile_picture,
            coin=self.markets[coin_id].coin,
            trend=trend,
            tint=self.markets[coin_id].color
        )
        self.posts.append(new_post)

        # Update the market size based on the trend
        self.markets[coin_id].apply_trend(trend)

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

    def create_random_coin(self):
        if not self.available_combinations:
            # print("No available combinations left!")
            return

        coin_id = f"coin_{len(self.markets)}"  # Generate a unique ID for the coin
        coin_type, color = random.choice(self.available_combinations)
        self.available_combinations.remove((coin_type, color))  
        initial_size = 80
        # Try finding a valid position
        max_attempts = 10  # Maximum attempts to find a non-overlapping position
        for _ in range(max_attempts):
            x, y = random.randint(
                self.window.width * 0.3, self.window.width - initial_size
            ), random.randint(initial_size, int(0.7 * self.window.height) - initial_size)
            if self.is_position_valid(x, y, initial_size):
                self.markets[coin_id] = Market(
                    coin=coin_type,
                    coin_id=coin_id,
                    x=x,
                    y=y,
                    initial_size=initial_size,
                    tint=color,
                )
                return

    def randomly_create_coin(self, dt):
        if random.random() < 0.9999:  # 50% chance of creating a new coin
            self.create_random_coin()

    def is_position_valid(self, x, y, size):
        """
        Checks if a new bubble position is valid (doesn't overlap with existing bubbles).

        Args:
            x (float): X-coordinate of the new bubble's center.
            y (float): Y-coordinate of the new bubble's center.
            size (float): Diameter of the new bubble.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        # Calculate bounding box of the new bubble
        radius = size / 2
        new_left = x - radius
        new_right = x + radius
        new_bottom = y - radius
        new_top = y + radius

        for market in self.markets.values():
            market_left, market_right, market_top, market_bottom = (
                market.get_bounding_box()
            )

            # Check if the bounding boxes overlap
            if not (
                new_right < market_left  # New bubble is to the left
                or new_left > market_right  # New bubble is to the right
                or new_top < market_bottom  # New bubble is below
                or new_bottom > market_top  # New bubble is above
            ):
                return False  # Overlap detected

        return True
