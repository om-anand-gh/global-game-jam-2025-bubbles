import pyglet
from scenes.menu_scene import MenuScene
from config import FPS
from utils import resource_loader

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_scene = MenuScene(self)
        
        # Schedule updates (i.e FPS)
        pyglet.clock.schedule_interval(self.update, 1/FPS)
        resource_loader.load_font()
        

    def on_draw(self):
        self.clear()
        if self.current_scene:
            self.current_scene.draw()

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def switch_scene(self, new_scene):
        self.current_scene = new_scene

    
    def on_mouse_press(self, x, y, button, modifiers):
        # Forward mouse press to the current scene
        if hasattr(self.current_scene, "on_mouse_press"):
            self.current_scene.on_mouse_press(x, y, button, modifiers)

