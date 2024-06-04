import pygame

# Initialize Pygame
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("Interpolation Example")

# Define colors
sky_color = (135, 206, 235)  # Light blue
ground_color = (34, 139, 34)  # Green color for the ground
black = (0, 0, 0)

# Game loop
running = True
clock = pygame.time.Clock()
altitude = 30000  # Start altitude

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Simulate altitude changes for testing purposes
    altitude += 10  # Increase altitude
    if altitude > 50000:
        altitude = 30000  # Reset altitude after it exceeds 50000

    # Calculate the interpolation factor based on altitude
    interpolation_factor = min(1, max(0, (altitude - 30000) / 20000))  # Ensure the interpolation factor is between 0 and 1

    # Diagnostic print
    print(f"Altitude: {altitude}, Interpolation Factor: {interpolation_factor}")

    # Interpolate between sky color and black
    interpolated_color = (
        int(sky_color[0] * (1 - interpolation_factor) + black[0] * interpolation_factor),
        int(sky_color[1] * (1 - interpolation_factor) + black[1] * interpolation_factor),
        int(sky_color[2] * (1 - interpolation_factor) + black[2] * interpolation_factor)
    )

    # Diagnostic print
    print(f"Interpolated Color: {interpolated_color}")

    # Fill the screen with the interpolated color
    screen.fill(interpolated_color)

    pygame.display.flip()
    clock.tick(60)  # Cap the frame rate to 60 FPS

# Quit Pygame
pygame.quit()
