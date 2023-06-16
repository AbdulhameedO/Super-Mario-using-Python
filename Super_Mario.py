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
mario_speed = 5
jump_height = 250
jump_speed = 18
jumping = False
vertical_velocity = 0

# Set up the obstacle
obstacle = pygame.image.load("obstacle.png").convert_alpha()
obstacle_x = 800
obstacle_y = screen_height - ground.get_height() - obstacle.get_height()

# Set up the clock
clock = pygame.time.Clock()

# Set up the running variable
running = True
paused = False

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not jumping and mario_y + mario.get_height() >= screen_height - ground.get_height() - jump_height:
                    jumping = True
                    vertical_velocity = -jump_speed

    # Update game state
    if not paused:
        if mario_x > screen_width / 2:  # Move the screen when Mario moves past the center of the screen
            mario_x -= mario_speed
            obstacle_x -= mario_speed
            background_x -= mario_speed / 2
            ground_x -= mario_speed
            if ground_x < -ground.get_width():
                ground_x = 0
            if background_x < -background.get_width():
                background_x = 0
            if obstacle_x < -obstacle.get_width():
                obstacle_x = screen_width

        # Check for collisions with obstacles
        if mario_x + mario.get_width() > obstacle_x and mario_x < obstacle_x + obstacle.get_width() and mario_y + mario.get_height() > obstacle_y and mario_y < obstacle_y + obstacle.get_height():
            # Determine which side of the obstacle Mario is colliding with
            if mario_x < obstacle_x + obstacle.get_width() / 2:
                mario_x = obstacle_x - mario.get_width()
            else:
                mario_x = obstacle_x + obstacle.get_width()

        # Handle user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and mario_x > 0:
            mario_x -= mario_speed
        if keys[pygame.K_RIGHT] and mario_x < screen_width - mario.get_width():
            mario_x += mario_speed

        # Handle jumping
        if jumping:
            mario_y += vertical_velocity
            vertical_velocity += 1.2
            if mario_y + mario.get_height() >= screen_height - ground.get_height():
                jumping = False
                mario_y = screen_height - ground.get_height() - mario.get_height()
                vertical_velocity = 0

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