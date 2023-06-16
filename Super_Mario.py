import pygame
import random

# Define constants
ENEMY_WIDTH = 30
ENEMY_HEIGHT = 40


class Coin:
    def __init__(self, x, y, speed):
        self.image = pygame.image.load("coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed


class Enemy:
    def __init__(self, x, y, speed):
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.rect.height
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed


class GroundEnemy(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.rect.y = y - self.rect.height + 10  # Adjust the y-coordinate to make the enemy appear on the ground


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

# Set up the enemies
enemies = []
enemy_speed = 8
enemy_delay = 100
enemy_timer = 0

coins = []
coin_speed = 6
coin_delay = 200
coin_timer = 0

# Set up the font
font = pygame.font.SysFont(None, 48)

# Set up the clock
clock = pygame.time.Clock()

# Set up the running variable
running = True
paused = False
lives = 3
score = 0

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

        # Update enemies
        enemy_timer += 1
        if enemy_timer >= enemy_delay:
            enemy_timer = 0
            enemy_y = screen_height - ground.get_height() - mario.get_height()
            # Create a mixture of normal enemies and ground enemies
            if len(enemies) % 2 == 0:
                enemy = Enemy(screen_width, enemy_y, enemy_speed)
            else:
                enemy = GroundEnemy(screen_width, enemy_y, enemy_speed)
            enemies.append(enemy)

        for enemy in enemies:
            enemy.update()
            if enemy.rect.colliderect(mario.get_rect()):
                lives -= 1
                if lives == 0:
                    running = False
                else:
                    enemies.remove(enemy)
            if enemy.rect.x < -enemy.rect.width:
                enemies.remove(enemy)

        coin_timer += 1
        if coin_timer >= coin_delay:
            coin_timer = 0
            coin_y = screen_height - ground.get_height() - mario.get_height()
            # Create a mixture of normal enemies and ground enemies
            if len(coins) % 2 == 0:
                coin = Coin(screen_width, enemy_y, enemy_speed)
            else:
                coin = GroundEnemy(screen_width, enemy_y, enemy_speed)
            coins.append(coin)

        for coin in coins:
            coin.update()
            if coin.rect.colliderect(mario.get_rect()):
                score += 50
                coins.remove(coin)
            if coin.rect.x < -coin.rect.width:
                coins.remove(coin)

        # Check for collisions with obstacles
        if mario_x + mario.get_width() > obstacle_x and mario_x < obstacle_x + obstacle.get_width() and mario_y + mario.get_height() > obstacle_y and mario_y < obstacle_y + obstacle.get_height():
            # Determine which side of the obstacle Mario is colliding with
            if mario_x < obstacle_x + obstacle.get_width() / 2:
                mario_x = obstacle_x - mario.get_width()
            else:
                mario_x = obstacle_x + obstacle.get_width()

        # Check for collisions with enemies
        for enemy in enemies:
            if mario_x + mario.get_width() > enemy.rect.x and mario_x < enemy.rect.x + enemy.rect.width and mario_y + mario.get_height() > enemy.rect.y and mario_y < enemy.rect.y + enemy.rect.height:
                lives -= 1
                if lives == 0:
                    running = False
                else:
                    enemies.remove(enemy)

        # Check for collisions with coins
        for coin in coins:
            if mario_x + mario.get_width() > coin.rect.x and mario_x < coin.rect.x + coin.rect.width and mario_y + mario.get_height() > coin.rect.y and mario_y < coin.rect.y + coin.rect.height:
                score += 50
                coins.remove(coin)

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

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)

    screen.blit(obstacle, (obstacle_x, obstacle_y))
    screen.blit(mario, (mario_x, mario_y))

    # Update coins
    coin_timer += 1
    if coin_timer >= coin_delay:
        coin_timer = 0
        coin_y = random.randint(0, screen_height - ground.get_height() - 100)
        coin = Coin(screen_width, coin_y, coin_speed)
        coins.append(coin)

    for coin in coins:
        coin.update()
        if coin.rect.colliderect(mario.get_rect()):
            coins.remove(coin)
            # Increase the score or add coins to the player's inventory

        if coin.rect.x < -coin.rect.width:
            coins.remove(coin)

    # Draw coins
    for coin in coins:
        screen.blit(coin.image, coin.rect)
    # Draw lives
    if score > 99:
        score = 0
        lives += 1
    lives_text = font.render("Lives: " + str(lives), True, (255, 255, 255))
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (10, 50))
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()