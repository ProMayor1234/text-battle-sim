import pygame
import sys

# Initialize PyGame
pygame.init()

# Set up window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First PyGame Window")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

# Clean exit
pygame.quit()
sys.exit()
