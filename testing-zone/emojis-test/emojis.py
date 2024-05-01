import pygame
from pygame import freetype

# Initialize Pygame
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((500, 500))  # Set the window size
pygame.display.set_caption("Emoji Display")  # Set the window title

# Load the NotoColorEmoji font
font = pygame.font.Font("NotoColorEmoji-Regular.ttf", 36)  # Adjust the path to your font file
emojis = pygame.freetype.Font("NotoColorEmoji-Regular.ttf", 50)

# Render the skull emoji 💀
emojis.render_to(screen, (0, 0), '💀', (255, 255, 255))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a background color


    # Display the skull emoji at the center of the screen
    # screen.blit(skull_text, (100,100))

    emojis.render_to(screen, (100, 100), '💀', (255, 255, 255))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
