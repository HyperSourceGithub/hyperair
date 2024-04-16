import pygame

# Initialize Pygame
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((1000, 800))  # (width, height)
pygame.display.set_caption("Cityscape")

# Load building image
building_image = pygame.image.load("testbuilding.png")  # Replace "testbuilding.png" with your building image file

# Define the percentage reduction (e.g., 50%)
percentage_reduction = 50

# Calculate new dimensions based on the percentage reduction
new_width = int(building_image.get_width() * (percentage_reduction / 100))
new_height = int(building_image.get_height() * (percentage_reduction / 100))

# Resize building image
building_image = pygame.transform.scale(building_image, (new_width, new_height))

# Define building class
class Building:
    def __init__(self, x, y):
        self.image = building_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Create a list to hold building objects
buildings = []

# Create buildings and add them to the list
building1 = Building(100, 400)  # Replace these coordinates with your desired positions
building2 = Building(550, 400)
buildings.extend([building1, building2])

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((135, 206, 235))  # Fill the screen with black (change color if needed)

    # Draw buildings
    for building in buildings:
        building.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
