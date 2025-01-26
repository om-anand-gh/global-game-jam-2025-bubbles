import random

import pyglet

import config
from scenes.base_scene import BaseScene
from components.button import Button
from components.bubbler_post import BubblerPost


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

        # Schedule random post creation every 2 seconds
        pyglet.clock.schedule_interval(self.add_random_post, config.NEW_POST_FREQUENCY)

    def return_to_menu(self):
        # Import MenuScene here to avoid circular import
        from scenes.menu_scene import MenuScene

        self.window.switch_scene(MenuScene(self.window))

    def draw(self):
        super().draw()  # Draw the background and other UI elements like buttons
        
        # Draw only the posts that are in the self.posts list
        for post in self.posts:
            post.draw()


    def update(self, dt):
        for post in self.posts:
            post.update_position()
            if post.is_out_of_bounds():
                self.posts.remove(post)  

    def add_random_post(self, dt):
        """Adds a new post with random attributes."""
        profile_picture = random.choice(list(BubblerPost.PROFILE_PICTURE.keys()))
        coin = random.choice(list(BubblerPost.COIN.keys()))
        trend = random.choice(list(BubblerPost.TREND.keys()))
        
        new_post = BubblerPost(
            profile_picture=profile_picture,
            coin=coin,
            trend=trend
        )
        self.posts.append(new_post)
