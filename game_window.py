import pyglet
from scenes.menu_scene import MenuScene
from config import FPS
class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_scene = MenuScene(self)
        
        # Schedule updates (i.e FPS)
        pyglet.clock.schedule_interval(self.update, 1/FPS)

        

    def on_draw(self):
        self.clear()
        if self.current_scene:
            self.current_scene.draw()

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def switch_scene(self, new_scene):
        self.current_scene = new_scene

