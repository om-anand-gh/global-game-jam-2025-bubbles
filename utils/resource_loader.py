import pyglet

def load_image(name):
    return pyglet.resource.image(f"assets/images/{name}")

def load_sound(name):
    return pyglet.resource.media(f"assets/sounds/{name}", streaming=False)

def load_font():
    return pyglet.resource.media(f"assets/sounds/SuperFrog-Yqy1q.ttf", streaming=False)
