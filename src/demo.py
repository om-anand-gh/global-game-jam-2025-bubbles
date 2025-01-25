import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Game - Click Anywhere, Act on Circle")

# Colors with transparency
BLUE = (0, 102, 204)
LIGHT_BLUE = (0, 102, 204, 100)  # Transparent shade for outer circle
HIGHLIGHT_BLUE = (0, 102, 255, 150)  # Intermediate shade for overlap

# Bubble properties
outer_radius = 100
inner_radius = 50
bubble_pos = [WIDTH // 2, HEIGHT // 2]  # Position of the bubble
velocity = [random.choice([-3, 3]), random.choice([-3, 3])]  # Random initial velocity
growth_rate = 2  # Change in inner radius per frame when holding
outer_update_time = 5000  # Time in milliseconds to update outer bubble size

# Variables to track mouse holding state
holding_left = False
holding_right = False

# Timer to update the outer circle size
last_update_time = pygame.time.get_ticks()

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Enable alpha channel for transparency
screen.set_alpha(None)

# Helper function to check if the mouse is on the inner circle
def is_mouse_on_circle(mouse_pos, circle_pos, radius):
    distance = ((mouse_pos[0] - circle_pos[0]) ** 2 + (mouse_pos[1] - circle_pos[1]) ** 2) ** 0.5
    return distance <= radius

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Clear the screen with white

    # Update bubble position based on velocity
    bubble_pos[0] += velocity[0]
    bubble_pos[1] += velocity[1]

    # Check for wall collisions and bounce
    if bubble_pos[0] - outer_radius <= 0 or bubble_pos[0] + outer_radius >= WIDTH:
        velocity[0] = -velocity[0]
    if bubble_pos[1] - outer_radius <= 0 or bubble_pos[1] + outer_radius >= HEIGHT:
        velocity[1] = -velocity[1]

    # Check if it's time to update the outer circle's size
    current_time = pygame.time.get_ticks()
    if current_time - last_update_time >= outer_update_time:
        outer_radius = random.randint(80, 150)  # Random size for outer circle
        last_update_time = current_time

    # Draw the outer circle
    outer_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(outer_surface, LIGHT_BLUE, bubble_pos, outer_radius)
    screen.blit(outer_surface, (0, 0))

    # Check for overlap and draw the inner circle accordingly
    if inner_radius > outer_radius:
        overlap_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(overlap_surface, HIGHLIGHT_BLUE, bubble_pos, inner_radius)
        screen.blit(overlap_surface, (0, 0))
    else:
        pygame.draw.circle(screen, BLUE, bubble_pos, inner_radius)

    # Event handling
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left button
                holding_left = True
            elif event.button == 3:  # Right button
                holding_right = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left button
                holding_left = False
            elif event.button == 3:  # Right button
                holding_right = False

    # Update inner circle size based on holding state and mouse position
    if holding_left and is_mouse_on_circle(mouse_pos, bubble_pos, inner_radius):
        inner_radius += growth_rate
    if holding_right and is_mouse_on_circle(mouse_pos, bubble_pos, inner_radius):
        inner_radius -= growth_rate
        if inner_radius < 10:  # Prevent the inner bubble from disappearing
            inner_radius = 10

    # Update the screen
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

# Quit Pygame
pygame.quit()
sys.exit()
