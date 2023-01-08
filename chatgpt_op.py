import pygame

# Initialize Pygame
pygame.init()

# Set the window size
screen_size = (800, 600)

# Create the window
screen = pygame.display.set_mode(screen_size)

# Load the background image
background_image = pygame.image.load("image.png").convert()

# Create a variable to store the y coordinate of the background
background_y = 0

# Set the speed at which the background should scroll
scroll_speed = 0.1

# Run the game loop
running = True
while running:
  # Check for events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Update the y coordinate of the background
  background_y -= scroll_speed

  # If the background has moved off the screen, reset its y coordinate
  if background_y < -background_image.get_height():
    background_y = 0

  # Draw the background
  screen.blit(background_image, (0, background_y))
  screen.blit(background_image, (0, background_y + background_image.get_height()))

  # Update the display
  pygame.display.flip()

# Quit Pygame
pygame.quit()