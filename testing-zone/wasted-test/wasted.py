import pygame

# Initialize Pygame
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((500, 500))  # Set the window size
pygame.display.set_caption("Overlays")  # Set the window title

def wasted():
    wasted = pygame.Surface((1000, 750))  # the size of your rect
    wasted.set_alpha(130)  # alpha level
    wasted.fill((255, 0, 0))  # this fills the entire surface
    screen.blit(wasted, (0, 0))

    bar_x = 1000
    bar_y = 100
    bar = pygame.Surface((bar_x, bar_y), pygame.SRCALPHA)
    bar.set_alpha(160)
    bar.fill((128, 128,128))

    rotatedbar = pygame.transform.rotate(bar, 10)
    screen.blit(rotatedbar, (-10, 100))


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((135, 206, 235))
    screen.blit(pygame.image.load("cloud.png"), (0, 80))

    wasted()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
