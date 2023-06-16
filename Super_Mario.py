import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 1500
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mario Level 1")

# Set up the background
background = pygame.image.load("background.png").convert_alpha()
background_x = 0

# Set up the ground
ground = pygame.image.load("ground.png").convert_alpha()
ground_x = 0

# Set up Mario
mario = pygame.image.load("mario.png").convert_alpha()
mario = pygame.transform.scale(mario, (40, 60))
mario_x = 100
mario_y = screen_height - ground.get_height() - mario.get_height()
mario_speed = 5  # Set Mario's speed

# Set up the obstacle
obstacle = pygame.image.load("obstacle.png").convert_alpha()
obstacle_x = 800
obstacle_y = screen_height - ground.get_height() - obstacle.get_height()

# Set up the clock
clock = pygame.time.Clock()

# Set up the running variable
running = True
paused = False  # Add a paused variable

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # Check for key presses
            if event.key == pygame.K_SPACE:  # Pause the game if the player presses the space bar
                paused = not paused

    # Update game state
    if not paused:  # Only update if the game is not paused
        ground_x -= mario_speed
        if ground_x < -ground.get_width():
            ground_x = 0
        background_x -= mario_speed / 2
        if background_x < -background.get_width():
            background_x = 0

        obstacle_x -= mario_speed
        if obstacle_x < -obstacle.get_width():
            obstacle_x = screen_width

        # Check for collisions with obstacles
        if mario_x + mario.get_width() > obstacle_x and mario_x < obstacle_x + obstacle.get_width() and mario_y + mario.get_height() > obstacle_y:
            mario_x -= mario_speed

        # Handle user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and mario_y == screen_height - ground.get_height() - mario.get_height():
            mario_y -= 20
        if keys[pygame.K_LEFT] and mario_x > 0:
            mario_x -= mario_speed
        if keys[pygame.K_RIGHT] and mario_x < screen_width - mario.get_width():
            mario_x += mario_speed

    # Draw the screen
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + background.get_width(), 0))
    screen.blit(ground, (ground_x, screen_height - ground.get_height()))
    screen.blit(ground, (ground_x + ground.get_width(), screen_height - ground.get_height()))
    screen.blit(obstacle, (obstacle_x, obstacle_y))
    screen.blit(mario, (mario_x, mario_y))
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()