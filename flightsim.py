try:
    import pygame
except ImportError as e:
    print("Oh no! Pygame is missing!")
    print("Use `pip install pygame` to install it.")
    exit()
 
import math
import random

# Variables before functions
speed = 0
pitch = 0
clouds = []
weather_phase = "clear"  # Initial weather phase
speedlock = False

# Colors
gray = (128, 128, 128)
white = (255, 255, 255)

# Cloud spawn probabilities for each weather phase
cloud_spawn_probabilities = {
    "clear": 0.01,
    "cloudy": 0.02,
    "rainy": 0.03,
    "stormy": 0.04
}


# Function to rotate an image
def rotate_image(image, angle):
    """Rotate an image."""
    rotated_image = pygame.transform.rotate(image, angle)
    return rotated_image


# Function to calculate altitude
def calculate_altitude(plane_y, ground_level):
    """Calculate the altitude of the plane relative to ground level."""
    return ground_level - plane_y


# Function to toggle speed lock
def toggle_speed_lock():
    global speedlock
    speedlock = not speedlock


# Rain particle class
class Rain:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length

    def draw(self, surface):
        pygame.draw.line(surface, white, (self.x, self.y), (self.x, self.y + self.length), 1)


# Initialize Pygame
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((800, 600))  # (width, height)
pygame.display.set_caption("Flight Sim")

# Set up fonts
font = pygame.font.Font("courierprime.ttf", 15)  # None uses the default system font, 36 is the font size

# Load the image of the plane
plane_image = pygame.image.load("plane.png")  # Provide the path to your plane image file

# Get the rectangle of the plane image
plane_rect = plane_image.get_rect()

# Calculate the position of the plane to make it appear in the center of the screen
plane_x = (screen.get_width() - plane_rect.width) / 2
plane_y = (screen.get_height() - plane_rect.height) / 2

# Set the position of the plane
plane_rect.topleft = (plane_x, plane_y)

# Load the cloud image
cloud_image = pygame.image.load("cloud.png")  # Provide the path to your cloud image file

# Load the icon image
icon_image = pygame.image.load("jetengine.png")  # Provide the path to your icon image file

# Set the window icon
pygame.display.set_icon(icon_image)

# Set up text
title = font.render("[Flight Sim]", True, gray)
speedtxt = font.render(f"[Speed: {speed:.2f}]", True, gray)
weather_label = font.render(f"[Weather: {weather_phase.capitalize()}]", True, gray)

# Define ground color
ground_color = (34, 139, 34)  # Green color for the ground

# Game Loop
running = True
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60) / 1000.0  # Get the time elapsed since the last frame (in seconds)

    # Define ground level
    ground_level = screen.get_height()  # Set ground level at the bottom of the plane

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check if the key 'W' is pressed to change the weather phase
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                # Cycle through the weather phases
                if weather_phase == "clear":
                    weather_phase = "cloudy"
                elif weather_phase == "cloudy":
                    weather_phase = "rainy"
                elif weather_phase == "rainy":
                    weather_phase = "stormy"
                elif weather_phase == "stormy":
                    weather_phase = "clear"

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Adjust speed and pitch based on pressed keys
    if keys[pygame.K_UP]:
        speed += 1000 * dt
    elif keys[pygame.K_DOWN]:
        speed -= 1000 * dt

    # Adjust pitch based on left/right arrow keys
    if keys[pygame.K_LEFT]:
        pitch += 100 * dt
    elif keys[pygame.K_RIGHT]:
        pitch -= 100 * dt
    elif keys[pygame.K_l]:
        pitch = 0

    if keys[pygame.K_k]:
        toggle_speed_lock()

    # Apply drag to simulate air resistance
    if not speedlock:
        speed -= 0.5 * dt

    # Clamp speed within reasonable limits
    speed = max(0, min(speed, 5000))

    # Update plane position
    plane_x += math.cos(math.radians(pitch)) * speed * dt
    plane_y -= math.sin(math.radians(pitch)) * speed * dt

    # Update plane rotation based on pitch
    rotated_plane_image = rotate_image(plane_image, pitch)
    rotated_plane_rect = rotated_plane_image.get_rect(center=plane_rect.center)

    # Draw the rotated plane image
    # Change sky color based on weather_phase
    if weather_phase == "clear":
        screen.fill((135, 206, 235))  # Light blue
    elif weather_phase == "cloudy":
        screen.fill((185, 185, 185))  # Gray
    elif weather_phase == "rainy":
        screen.fill((201, 201, 201))  # Slate gray
    elif weather_phase == "stormy":
        screen.fill((107, 107, 107))  # Black

    # Add new rain particles if weather is rainy or stormy
    if weather_phase in ["rainy", "stormy"]:
        for _ in range(10):
            x = random.randint(0, screen.get_width())
            y = random.randint(0, screen.get_height())
            length = random.randint(10, 20)
            rain_particle = Rain(x, y, length)
            rain_particle.draw(screen)

    screen.blit(rotated_plane_image, rotated_plane_rect)

    # Move clouds
    for cloud in clouds:
        cloud[0] -= (100 + speed * 0.25) * dt  # Adjust cloud x-coordinate based on speed
        cloud[1] += (100 + speed * 0.25) * dt * math.sin(
            math.radians(pitch))  # Adjust cloud y-coordinate based on speed and pitch

    # Add new clouds if needed
    if len(clouds) < 10 and random.random() < cloud_spawn_probabilities[weather_phase]:
        min_height = max(ground_level - 20000, 0)  # Minimum cloud height above ground
        max_height = max(ground_level - 8000, 0)  # Maximum cloud height above ground
        if min_height < max_height:
            clouds.append([screen.get_width(), random.randint(min_height, max_height)])

    # Remove off-screen clouds
    clouds = [cloud for cloud in clouds if cloud[0] > -cloud_image.get_width()]

    # Draw clouds
    for cloud in clouds:
        screen.blit(cloud_image, (cloud[0], cloud[1]))

    # Calculate altitude
    altitude = calculate_altitude(plane_y, ground_level)

    # Update text
    if weather_phase == "stormy":
        title = font.render("[Flight Sim]", True, white)
        speedtxt = font.render(f"[Speed: {speed:.2f}]", True, white)
        weather_label = font.render(f"[Weather: {weather_phase.capitalize()}]", True, white)
        speedlock_label = font.render(f"[Speed Lock: {speedlock}]", True, white)
        altitude_text = font.render(f"[Altitude: {altitude:.2f}]", True, white)
    else:
        title = font.render("[Flight Sim]", True, gray)
        speedtxt = font.render(f"[Speed: {speed:.2f}]", True, gray)
        weather_label = font.render(f"[Weather: {weather_phase.capitalize()}]", True, gray)
        speedlock_label = font.render(f"[Speed Lock: {speedlock}]", True, gray)
        altitude_text = font.render(f"[Altitude: {altitude:.2f}]", True, gray)

    # Define ground level
    ground_level = plane_y + plane_rect.height  # Set ground level at the bottom of the plane

    # Draw ground plane
    pygame.draw.rect(screen, ground_color,(0, screen.get_height() - ground_level + 150, screen.get_width(), ground_level))

    # Draw text
    screen.blit(title, (1, 1))
    screen.blit(speedtxt, (1, 20))
    screen.blit(weather_label, (1, 40))
    screen.blit(speedlock_label, (1, 60))
    screen.blit(altitude_text, (1, 80))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

