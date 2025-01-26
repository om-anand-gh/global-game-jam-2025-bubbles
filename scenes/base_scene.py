import pyglet
import time

from utils.resource_loader import load_audio

class BaseScene:
    def __init__(self, window, background_image_path: str, background_audio_path: str = "menu_bg_audio.mp3"):
        self.window = window

        # Load and set the background image
        self.background_image = pyglet.resource.image(background_image_path)
        self.background_sprite = pyglet.sprite.Sprite(self.background_image)

        # Center and scale the background image
        self.background_sprite.scale = max(
            window.width / self.background_image.width,
            window.height / self.background_image.height,
        )
        self.background_sprite.x = (window.width - self.background_sprite.width) / 2
        self.background_sprite.y = (window.height - self.background_sprite.height) / 2
        
        # Store elements in a hierarchical list for event handling
        self.elements = []

        # Load the background music
        self.music = load_audio(background_audio_path)
        self.music_player = pyglet.media.Player()
        self.music_player.queue(self.music)
        self.music_player.loop = True  # Enable looping
        self.music_player.volume = 0.3
        self.music_player.play()  # Start playback

        
        # Add a cooldown for mouse input
        self.last_scene_switch = time.time()


        # Bind event handlers
        window.push_handlers(self)

    def draw(self):
        # Draw the background
        self.background_sprite.draw()

        # Draw the elements
        for element in self.elements:
            element.draw()

    def cleanup(self):
        # Clean up event handlers when switching scenes
        self.window.remove_handlers(self)

    def update(self, dt):
        # Default update (can be overridden in derived classes)
        pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        # Ignore mouse presses if still in cooldown
        if time.time() - self.last_scene_switch < 1:
            return
        
        # Forward mouse press to all interactive elements
        for element in self.elements:
            element.on_mouse_press(x, y, button, modifiers)

    def stop_music(self):
        """Stop the background music."""
        self.music_player.pause()

    def resume_music(self):
        """Resume the background music."""
        self.music_player.play()