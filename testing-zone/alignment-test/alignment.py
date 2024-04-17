import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Vertical Alignment Example")

# Define colors
WHITE = (255, 255, 255)

# Example item to align (text)
font = pygame.font.Font(None, 36)  # You can choose your own font
text_surface = font.render("Aligned Text", True, WHITE)
text_rect = text_surface.get_rect()

# Calculate vertical position to align to the middle of the screen
vertical_position = (screen_height - text_rect.height) // 2

# Set the vertical position of the item
text_rect.y = vertical_position

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a background color (optional)
    screen.fill((0, 0, 0))  # Black background

    # Draw the aligned item (text in this case)
    screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
