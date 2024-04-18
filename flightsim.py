# Check python version
import sys
pyver = sys.version_info.major
if pyver < 3:
    print(f"Oh no! You currently have Python {pyver}. Please upgrade to Python 3 or above.")
elif pyver >= 3:
    print(f"Python {pyver} found, continuing...")

try:
    import pygame, requests
except ImportError as e:
    print("Missing dependencies! Install pygame and requests first: `pip install pygame requests`")
    exit()

import math
import random
import time

# Check for updates
import utils.updater

version = "v1.1.5"
response = requests.get("https://github.com/HyperSourceGithub/hyperair/releases/latest")
latest_version = response.url.split("/").pop()
print(f"Using version {version}")
if latest_version != version:
    update = input(f"Latest version is {latest_version}, would you like to update? [Y/n] ")
    if update.lower() == "y":
        utils.updater.update()
    elif update.lower() == "n":
        print("Update canceled, continuing with current version")

# Variables before functions
speed = 500
pitch = 0
clouds = []
stars = []
birds = []
weather_phase = "clear"  # Initial weather phase
speedlock = False

# Colors
gray = (128, 128, 128)
white = (255, 255, 255)

# Cloud spawn probabilities for each weather phase
cloud_spawn_probabilities = {
    "clear": 0.05,
    "cloudy": 0.06,
    "rainy": 0.07,
    "stormy": 0.08
}

# plane images for cycle
planes = ["assets/plane.png", "assets/plane2.png", "assets/plane3.png", "assets/plane4.png"]
plane_index = 0

# ==========================================================================

# Rain particle class
class Rain:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length

    def draw(self, surface):
        pygame.draw.line(surface, white, (self.x, self.y), (self.x, self.y + self.length), 1)

# ==========================================================================


# Initialize Pygame
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((1000, 750), pygame.RESIZABLE)  # (width, height)
pygame.display.set_caption(f"HyperAir {version}")

# Set up fonts
font = pygame.font.Font("fonts/courierprime.ttf", 15)  # (font, size)
logofont = pygame.font.Font("fonts/RobotoMono-Regular.ttf", 70)

# ==========================================================================

# Loading Screen
logo = pygame.image.load("assets/logo.png")
loadingtitle = logofont.render("Hyper Studios", True, white)

screen.fill((0, 0, 0))

screen.blit(logo, (90, (screen.get_height() - logo.get_height()) // 2))
screen.blit(loadingtitle, (360, (screen.get_height() - loadingtitle.get_height()) // 2))

pygame.display.flip()

time.sleep(3)

# ==========================================================================

# Load the image of the plane
plane_image = pygame.image.load(planes[plane_index])

# Get the rectangle of the plane image
plane_rect = plane_image.get_rect()

# Calculate the position of the plane to make it appear in the center of the screen
plane_x = (screen.get_width() - plane_rect.width) / 2
plane_y = (screen.get_height() - plane_rect.height) / 2

# Set the position of the plane
plane_rect.topleft = (plane_x, plane_y)

# Load the cloud image
cloud_image = pygame.image.load("assets/cloud.png")

# Load the star image
star_image = pygame.image.load("assets/star.png")

# Load the birb
bird_image = pygame.image.load("assets/bird.png")

# ==========================================================================

# Load the icon image
icon_image = pygame.image.load("assets/jetengine.png")

# Set the window icon
pygame.display.set_icon(icon_image)

# ==========================================================================

# Set up text
title = font.render(f"[HyperAir {version}]", True, gray)
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

            # Plane Switcher
            elif event.key == pygame.K_p:
                if plane_index == 3:
                    plane_index = 0
                else:
                    plane_index += 1
                plane_image = pygame.image.load(planes[plane_index])

        # Resize Checker
        elif event.type == pygame.VIDEORESIZE:
            # Get the rectangle of the plane image
            plane_rect = plane_image.get_rect()

            # Calculate the position of the plane to make it appear in the center of the screen
            plane_x = (screen.get_width() - plane_rect.width) / 2
            plane_y = (screen.get_height() - plane_rect.height) / 2

            # Set the position of the plane
            plane_rect.topleft = (plane_x, plane_y)
    # ==========================================================================

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

    # Toggle speedlock
    if keys[pygame.K_k]:
        speedlock = not speedlock

    # Apply drag to simulate air resistance
    if not speedlock:
        speed -= 0.2 * dt

    # Clamp speed within reasonable limits
    speed = max(0, min(speed, 8000))

    # Update plane position
    plane_x += math.cos(math.radians(pitch)) * speed * dt
    plane_y -= math.sin(math.radians(pitch)) * speed * dt

    # Lift simulation
    # Data sources: 
    #   https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/lifteq.html
    #   https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/area.html
    #   https://aerospaceweb.org/question/aerodynamics/q0252.shtml
    # lift = 0.5 * d * v^2 * A * Cl
    # Not a 100% accurate since it breaks things
    lift = 0.5 * 0.302 * speed * 0.08 * 0.02 * math.cos(math.radians(pitch)) * dt

    # Gravity
    plane_y += 98 * dt - lift


    # Update plane rotation based on pitch
    rotated_plane_image = pygame.transform.rotate(plane_image, pitch)
    rotated_plane_rect = rotated_plane_image.get_rect(center=plane_rect.center)

    # Calculate altitude
    altitude = ground_level - plane_y


    # Change sky color based on weather_phase
    if altitude < 30000:
        if weather_phase == "clear":
            sky_color = (135, 206, 235)  # light blue
        elif weather_phase == "cloudy":
            sky_color = (185, 185, 185)  # a bit gray
        elif weather_phase == "rainy":
            sky_color = (201, 201, 201)  # darkish gray
        elif weather_phase == "stormy":
            sky_color = (107, 107, 107)  # really dark gray
        screen.fill(sky_color)
    else:
        # Calculate the interpolation factor based on altitude
        interpolation_factor = min(1, (
                altitude - 30000) / 20000)  # Ensure that the interpolation factor is between 0 and 1

        # Interpolate between sky color and black
        black = (0, 0, 0)
        interpolated_color = (
            int(sky_color[0] * (1 - interpolation_factor) + black[0] * interpolation_factor),
            int(sky_color[1] * (1 - interpolation_factor) + black[1] * interpolation_factor),
            int(sky_color[2] * (1 - interpolation_factor) + black[2] * interpolation_factor)
        )

        # Fill the screen with the interpolated color
        screen.fill(interpolated_color)

    # Add new rain particles if weather is rainy or stormy
    if weather_phase in ["rainy", "stormy"] and altitude < 12000:
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
    if len(clouds) < 20 and random.random() < cloud_spawn_probabilities[weather_phase] and 3000 < altitude < 12000:
        clouds.append([screen.get_width(), random.randint(0, screen.get_height() - 100)])

    # Remove off-screen clouds
    clouds = [cloud for cloud in clouds if cloud[0] > -cloud_image.get_width()]

    # Draw clouds
    for cloud in clouds:
        screen.blit(cloud_image, (cloud[0], cloud[1]))

    # ==========================================================================

    # Move stars
    for star in stars:
        star[0] -= (100 + speed * 0.25) * dt  # Adjust star x-coordinate based on speed
        star[1] += (100 + speed * 0.25) * dt * math.sin(
            math.radians(pitch))  # Adjust star y-coordinate based on speed and pitch

    # Add new stars if needed
    if len(stars) < 20 and random.random() < 0.4 and altitude > 35000:
        stars.append([screen.get_width(), random.randint(0, screen.get_height() - 100)])

    # Remove off-screen stars
    stars = [star for star in stars if star[0] > -star_image.get_width()]

    # Draw stars
    for star in stars:
        screen.blit(star_image, (star[0], star[1]))

    # Move birds
    for bird in birds:
        bird[0] -= (100 + speed / 4) * dt  # Adjust bird x-coordinate based on speed
        bird[1] += (100 + speed / 4) * dt * math.sin(
            math.radians(pitch))  # Adjust bird y-coordinate based on speed and pitch

    # Add new birds if needed
    if len(birds) < 20 and random.random() < 0.005 and altitude < 12000:
        birds.append([screen.get_width(), random.randint(0, screen.get_height() - 100)])

    # Remove off-screen birds
    birds = [bird for bird in birds if bird[0] > -bird_image.get_width()]

    # Draw birds
    for bird in birds:
        screen.blit(bird_image, (bird[0], bird[1]))

    # Update text
    if weather_phase == "stormy":
        title = font.render(f"[HyperAir {version}]", True, white)
        speedtxt = font.render(f"[Speed: {speed:.2f}]", True, white)
        weather_label = font.render(f"[Weather: {weather_phase.capitalize()}]", True, white)
        speedlock_label = font.render(f"[Speed Lock: {speedlock}]", True, white)
        altitude_text = font.render(f"[Altitude: {altitude:.2f}]", True, white)
        pitch_text = font.render(f"[Pitch: {pitch:.2f}]", True, white)
    else:
        title = font.render(f"[HyperAir {version}]", True, gray)
        speedtxt = font.render(f"[Speed: {speed:.2f}]", True, gray)
        weather_label = font.render(f"[Weather: {weather_phase.capitalize()}]", True, gray)
        speedlock_label = font.render(f"[Speed Lock: {speedlock}]", True, gray)
        altitude_text = font.render(f"[Altitude: {altitude:.2f}]", True, gray)
        pitch_text = font.render(f"[Pitch: {pitch:.2f}]", True, gray)

    # Define ground level
    ground_level = plane_y + plane_rect.height  # Set ground level at the bottom of the plane

    # Draw ground plane
    pygame.draw.rect(screen, ground_color, (0, screen.get_height() - ground_level + 300, screen.get_width(), ground_level))

    # Draw text [w,h :(1000, 800)]
    screen.blit(title, (1, 1))
    screen.blit(speedtxt, (1, 20))
    screen.blit(weather_label, (1, 40))
    screen.blit(speedlock_label, (1, 60))
    screen.blit(altitude_text, (1, 80))
    screen.blit(pitch_text, (1, 100))

    # Update the display
    pygame.display.flip()

# Quit Pygame
# pygame.quit()
