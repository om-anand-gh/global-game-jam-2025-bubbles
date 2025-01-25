import pyglet

def load_image(name):
    return pyglet.resource.image(f"assets/images/{name}")

def load_sound(name):
    return pyglet.resource.media(f"assets/sounds/{name}", streaming=False)

def load_font():
    pyglet.resource.add_font(f"assets/fonts/SuperFrog-Yqy1q.ttf")
