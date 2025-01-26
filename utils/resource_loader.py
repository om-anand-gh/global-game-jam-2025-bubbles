import pyglet

def load_image(name):
    return pyglet.resource.image(f"assets/images/{name}")

def load_audio(name):
    return pyglet.resource.media(f"assets/audio/{name}", streaming=False)

def load_font():
    pyglet.resource.add_font(f"assets/fonts/SuperFrog-Yqy1q.ttf")
