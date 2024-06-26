# Check python version
import os
import sys

try:
    import pygame
    from pygame import freetype
    import pygame.draw
    import requests
    import asyncio
    from pathlib import Path
except ImportError as e:
    autoimport = input("Missing dependencies! Would you like to import them super-automagically? [Y/n]")
    if autoimport.lower() == "y":
        os.system("python3 -m pip install -r requirements.txt")
    elif autoimport.lower() == "n":
        print("Please run [python3 -m pip install -r requirements.txt] please.")
        exit()

import math
import random
import time

# Check for updates
import utils.updater

# =================== #
version = "v1.2.1"
# =================== #
'''
hasWifi = input("Are you currently connected to WiFi? (Y/n): ")
if hasWifi.lower() == "y":
    response = requests.get("https://github.com/HyperSourceGithub/hyperair/releases/latest")
    latest_version = response.url.split("/").pop()
    print(f"Using version {version}")
    if latest_version != version:
        update = input(f"Latest version is {latest_version}, would you like to update? [Y/n] ")
        if update.lower() == "y":
            utils.updater.update()
        elif update.lower() == "n":
            print("Update canceled, continuing with current version")
else:
    print("Okay, continuing without WiFi")
'''

# Variables before functions
speed = 500
pitch = 0
clouds = []
stars = []
birds = []
buildings = []
weather_phase = "clear"  # Initial weather phase
speedlock = False
global exitcode

# Colors
gray = (128, 128, 128)
white = (255, 255, 255)
red = (255, 0, 0)

# Cloud spawn probabilities for each weather phase
cloud_spawn_probabilities = {
    "clear": 0.05,
    "cloudy": 0.06,
    "rainy": 0.07,
    "stormy": 0.08
}

# plane images for cycle
planes = ["assets/planes/plane.png", "assets/planes/plane2.png", "assets/planes/plane3.png", "assets/planes/plane4.png"]
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

def wasted():
    wasted = pygame.Surface((1000, 750))  # the size of your rect
    wasted.set_alpha(150)  # alpha level
    wasted.fill((180, 0, 0))  # this fills the entire surface
    screen.blit(wasted, (0, 0))

    bar_x = 5000
    bar_y = 200
    bar = pygame.Surface((bar_x, bar_y), pygame.SRCALPHA)
    bar.set_alpha(190)
    bar.fill((128, 128, 128))

    rotatedbar = pygame.transform.rotate(bar, 8)
    screen.blit(rotatedbar, (-40, -321))

def draw_rectangle(x, y, width, height, color, rotation=0):
    """Draw a rectangle, centered at x, y.

    Arguments:
      x (int/float):
        The x coordinate of the center of the shape.
      y (int/float):
        The y coordinate of the center of the shape.
      width (int/float):
        The width of the rectangle.
      height (int/float):
        The height of the rectangle.
      color (str):
        Name of the fill color, in HTML format.
    """
    points = []

    # The distance from the center of the rectangle to
    # one of the corners is the same for each corner.
    radius = math.sqrt((height / 2)**2 + (width / 2)**2)

    # Get the angle to one of the corners with respect
    # to the x-axis.
    angle = math.atan2(height / 2, width / 2)

    # Transform that angle to reach each corner of the rectangle.
    angles = [angle, -angle + math.pi, angle + math.pi, -angle]

    # Convert rotation from degrees to radians.
    rot_radians = (math.pi / 180) * rotation

    # Calculate the coordinates of each point.
    for angle in angles:
        y_offset = -1 * radius * math.sin(angle + rot_radians)
        x_offset = radius * math.cos(angle + rot_radians)
        points.append((x + x_offset, y + y_offset))

    pygame.draw.polygon(screen, color, points)

# ==========================================================================


# Initialize Pygame
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((1000, 750), pygame.RESIZABLE)  # (width, height)
pygame.display.set_caption(f"HyperAir {version}")

# Set up fonts
font = pygame.font.Font("fonts/courierprime.ttf", 15)  # (font, size)
logofont = pygame.font.Font("fonts/RobotoMono-Regular.ttf", 70)
crashfont = pygame.font.Font("fonts/RobotoMono-Bold.ttf", 90)
emojis = pygame.freetype.Font("fonts/NotoColorEmoji-Regular.ttf", 90)

# ==========================================================================

# Loading Screen
logo = pygame.image.load("assets/logo.png")
loadingtitle = logofont.render("Hyper Studios", True, white)

screen.fill((0, 0, 0))

screen.blit(logo, (90, (screen.get_height() - logo.get_height()) // 2))
screen.blit(loadingtitle, (360, (screen.get_height() - loadingtitle.get_height()) // 2))

pygame.display.flip()

# pygame.time.delay(3000)

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

ground_level = plane_y + plane_rect.height  # Set ground level at the bottom of the plane

# Define the actual ground level: where the rectangle's top is.
absolute_ground_y = screen.get_height() - ground_level + 351

groundRect = pygame.Rect(0, screen.get_height() - ground_level + 300, screen.get_width(), ground_level)

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
            exitcode = "quit"

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

    # Update plane rotation based on pitch
    rotated_plane_image = pygame.transform.rotate(plane_image, pitch)
    rotated_plane_rect = rotated_plane_image.get_rect(center=plane_rect.center)

    # Calculate altitude
    altitude = ground_level - plane_y

    global sky_color

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
        else:
            sky_color = (135, 206, 235)
        screen.fill(sky_color)
    else:
        # Calculate the interpolation factor based on altitude
        interpolation_factor = min(1, (altitude - 30000) / 20000)  # Make the interpol factor is between 0 and 1

        # Interpolate between sky color and black
        black = (0, 0, 0)
        interpolated_color = (
            float(sky_color[0] * (1 - interpolation_factor) + black[0] * interpolation_factor),
            float(sky_color[1] * (1 - interpolation_factor) + black[1] * interpolation_factor),
            float(sky_color[2] * (1 - interpolation_factor) + black[2] * interpolation_factor)
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

    # buildings = [] at start

    building_images = ["assets/buildings/house1.png"]
    # define building image
    buildImage = random.choice(building_images)

    # Generate buildings
    if len(buildings) < 5 and random.random() < 1:
        buildings.append([screen.get_width(), absolute_ground_y - pygame.image.load(buildImage).get_height() + 5, buildImage]) # only x value, y for ground

    # Move buildings
    for b in buildings:
        b[0] -= (100 + speed / 4) * dt
        b[1] = absolute_ground_y - pygame.image.load(buildImage).get_height() + 5

    # Remove off-screens
    buildings = [b for b in buildings if b[0] > -pygame.image.load(buildImage).get_width()]

    # Draw buildings
    for b in buildings:
        screen.blit(b[2], (b[0], b[1]))


    # Crashes
    if plane_rect.colliderect(groundRect):
        exitcode = "crash"
        running = False
    else:
        pass


    '''
    if altitude < 240 :
        if pitch < -3:
            exitcode = "crash"
            running = False
        else:
            pass
    '''

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

    # Define the actual ground level: where the rectangle's top is.
    absolute_ground_y = screen.get_height() - ground_level + 351

    # Ground rectangle
    groundRect = pygame.Rect(0, screen.get_height() - ground_level + 300, screen.get_width(), ground_level)

    # Draw ground plane
    pygame.draw.rect(screen, ground_color, groundRect)

    # Draw text [w,h :(1000, 800)]
    screen.blit(title, (1, 1))
    screen.blit(speedtxt, (1, 20))
    screen.blit(weather_label, (1, 40))
    screen.blit(speedlock_label, (1, 60))
    screen.blit(altitude_text, (1, 80))
    screen.blit(pitch_text, (1, 100))

    # Buildings!
    # screen.blit(house_image, (((screen.get_width() - house_image.get_width()) //2 ), (absolute_ground_y - house_image.get_height())))

    # Update the display
    pygame.display.flip()

# ==========================================================================

# Handle exit codes
if exitcode == "crash":
    wasted_img = pygame.image.load("assets/wasted.png")

    wasted_y = ((screen.get_height() - wasted_img.get_height()) // 2)
    wasted_x = ((screen.get_width() - wasted_img.get_width()) // 2)

    wasted()

    screen.blit(wasted_img, (wasted_x, wasted_y))

    pygame.display.flip()

    pygame.time.delay(5000)

elif exitcode == "quit":
    pass

# Quit Pygame
pygame.quit()
