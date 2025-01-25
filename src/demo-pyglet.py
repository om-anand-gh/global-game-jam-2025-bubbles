import pyglet
import random
import math
import time  # Use Python's time module for consistent timing

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Initialize Pyglet window
window = pyglet.window.Window(WIDTH, HEIGHT, "Bubble Game - Click Anywhere, Act on Circle")
window.set_mouse_visible(True)

# Colors
BLUE = (0, 102, 204)
LIGHT_BLUE = (0, 102, 204, 100)  # Transparent shade for outer circle
HIGHLIGHT_BLUE = (0, 102, 255, 150)  # Intermediate shade for overlap

# Bubble properties
outer_radius = 100
inner_radius = 50
bubble_pos = [WIDTH // 2, HEIGHT // 2]
velocity = [random.choice([-3, 3]), random.choice([-3, 3])]  # Random initial velocity
growth_rate = 2  # Change in inner radius per frame when holding
outer_update_time = 5  # Time in seconds to update outer bubble size

# Variables to track mouse holding state
holding_left = False
holding_right = False

# Timer for updating outer circle size
last_update_time = time.time()

# Helper function to check if the mouse is on the inner circle
def is_mouse_on_circle(mouse_x, mouse_y, circle_x, circle_y, radius):
    distance = math.sqrt((mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2)
    return distance <= radius

# Draw function
@window.event
def on_draw():
    global outer_radius, inner_radius
    window.clear()
    
    # Draw outer circle with transparency
    outer_circle = pyglet.shapes.Circle(bubble_pos[0], bubble_pos[1], outer_radius, color=LIGHT_BLUE[:3])
    outer_circle.opacity = LIGHT_BLUE[3]
    outer_circle.draw()

    # Draw inner circle based on overlap
    if inner_radius > outer_radius:
        inner_circle = pyglet.shapes.Circle(bubble_pos[0], bubble_pos[1], inner_radius, color=HIGHLIGHT_BLUE[:3])
        inner_circle.opacity = HIGHLIGHT_BLUE[3]
    else:
        inner_circle = pyglet.shapes.Circle(bubble_pos[0], bubble_pos[1], inner_radius, color=BLUE)
    inner_circle.draw()

# Update function for game logic
def update(dt):
    global bubble_pos, velocity, outer_radius, last_update_time, inner_radius

    # Update bubble position based on velocity
    bubble_pos[0] += velocity[0]
    bubble_pos[1] += velocity[1]

    # Check for wall collisions and bounce
    if bubble_pos[0] - outer_radius <= 0 or bubble_pos[0] + outer_radius >= WIDTH:
        velocity[0] = -velocity[0]
    if bubble_pos[1] - outer_radius <= 0 or bubble_pos[1] + outer_radius >= HEIGHT:
        velocity[1] = -velocity[1]

    # Check if it's time to update the outer circle's size
    current_time = time.time()
    if current_time - last_update_time >= outer_update_time:
        outer_radius = random.randint(80, 150)
        last_update_time = current_time

# Mouse press event
@window.event
def on_mouse_press(x, y, button, modifiers):
    global holding_left, holding_right
    if button == pyglet.window.mouse.LEFT:
        holding_left = True
    elif button == pyglet.window.mouse.RIGHT:
        holding_right = True

# Mouse release event
@window.event
def on_mouse_release(x, y, button, modifiers):
    global holding_left, holding_right
    if button == pyglet.window.mouse.LEFT:
        holding_left = False
    elif button == pyglet.window.mouse.RIGHT:
        holding_right = False

# Mouse drag event (to handle holding logic properly)
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global inner_radius
    if holding_left and is_mouse_on_circle(x, y, bubble_pos[0], bubble_pos[1], inner_radius):
        inner_radius += growth_rate
    elif holding_right and is_mouse_on_circle(x, y, bubble_pos[0], bubble_pos[1], inner_radius):
        inner_radius -= growth_rate
        if inner_radius < 10:
            inner_radius = 10

# Schedule update
pyglet.clock.schedule_interval(update, 1 / 60)  # 60 FPS

# Run the game
pyglet.app.run()
