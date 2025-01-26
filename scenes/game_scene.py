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
        super().__init__(
            window, "assets/images/background/background_game.png", "game_bg_audio.mp3"
        )

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

        # Cash and investments
        self.cash = 1000  # Starting cash
        self.investments = {}  # Track investments per market
        self.invest_amount = 50  # Fixed amount to invest per click

        self.cash_label = pyglet.text.Label(
            f"Cash: ${self.cash:.2f} | Investments: ${sum(self.investments.values()):.2f}",
            font_name=config.FONT,
            font_size=20,
            x=10,
            y=10,
            anchor_x="left",
            anchor_y="bottom",
            color=(255, 255, 255, 255),  # White color
        )

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
            weights=[50, 30, 20],  # Probabilities: 50% down, 20% neutral, 20% up
            k=1,  # Number of items to pick
        )[0]

        new_post = BubblerPost(
            profile_picture=profile_picture,
            coin=self.markets[coin_id].coin,
            trend=trend,
            tint=self.markets[coin_id].color,
        )
        self.posts.append(new_post)

        # Update the market size based on the trend
        self.markets[coin_id].apply_trend(trend)

        # Adjust investment values based on the trend
        if trend == "up":
            self.investments[coin_id] = self.investments.get(coin_id, 0) * 1.1
        elif trend == "down":
            self.investments[coin_id] = self.investments.get(coin_id, 0) * 0.9

    def draw(self):
        super().draw()

        # Draw the markets
        for market in self.markets.values():
            market.draw()

        # Draw the posts
        for post in self.posts:
            post.draw()

        self.cash_label.draw()

    def update(self, dt):
        # Update markets' animation
        for coin_id, market in list(self.markets.items()):
            market.animate_size(dt)
            if market.is_popping:
                market.show_pop_asset()
                self.investments[coin_id] = 0  # Reset investment
                self.available_combinations.append(
                    (self.markets[coin_id].coin, self.markets[coin_id].color)
                )
                self.markets.pop(coin_id)

            elif market.should_pop():
                market.show_pop_asset()

        # Game over if cash + investments < 0
        total_investment = sum(self.investments.values())
        if self.cash + total_investment <= 0:
            self.game_over()

        for post in self.posts[:]:
            post.update_position()
            if post.is_out_of_bounds():
                self.posts.remove(post)

        self.cash_label.text = f"Cash: ${self.cash:.2f} | Investments: ${sum(self.investments.values()):.2f}"

    def return_to_menu(self):
        self.stop_music()
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
            ), random.randint(
                initial_size, int(0.7 * self.window.height) - initial_size
            )
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
        if random.random() < 0.6:  # 60% chance of creating a new coin
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

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            print("handling left click")
            self.handle_investment(x, y)
        elif button == pyglet.window.mouse.RIGHT:
            print("handling right click")
            self.handle_withdrawal(x, y)

    def handle_investment(self, x, y):
        """
        Invest a fixed amount of cash in a market if a bubble is clicked.
        """
        for coin_id, market in self.markets.items():
            if self.is_bubble_clicked(x, y, market):
                if self.cash >= self.invest_amount:
                    self.cash -= self.invest_amount
                    self.investments[coin_id] = (
                        self.investments.get(coin_id, 0) + self.invest_amount
                    )
                else:
                    print("Not enough cash to invest!")
                return

    def handle_withdrawal(self, x, y):
        """
        Withdraw a fixed amount of cash from a market if a bubble is clicked.
        """
        for coin_id, market in self.markets.items():
            if self.is_bubble_clicked(x, y, market):
                if self.investments.get(coin_id, 0) >= self.invest_amount:
                    self.investments[coin_id] -= self.invest_amount
                    self.cash += self.invest_amount
                else:
                    print("Not enough investment in this market to withdraw!")
                return

    def is_bubble_clicked(self, x, y, market):
        """
        Check if a bubble was clicked.
        """
        left, right, top, bottom = market.get_bounding_box()
        return left <= x <= right and bottom <= y <= top

    def game_over(self):
        """
        Ends the game when cash + investments < 0.
        """
        print("Game Over! You ran out of cash.")
        self.stop_music()
        player = pyglet.media.Player()
        player.pause()
        # Switch to a game over scene
        from scenes.game_over_scene import GameOverScene
        self.window.switch_scene(GameOverScene(self.window))
