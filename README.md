# Mario Game

This is a simple game built using Pygame library in Python. In this game, the player controls Mario, a character from the popular video game franchise, and tries to collect coins while avoiding obstacles and enemies.

## How to play

- Use the arrow keys to move Mario left or right.
- Press the space bar to make Mario jump.
- Collect coins to increase your score.
- Avoid obstacles and enemies.
- If you collide with an enemy, you will lose a life. You start with three lives, and the game ends when you lose all of them.

## Code structure

The code is divided into three parts:

1. Constants: This section defines constants used throughout the game, such as the width and height of the enemies.
2. Classes: This section defines the classes used in the game, such as `Enemy` and `Coin`. Each class has an `__init__` method that initializes the object's properties and an `update` method that updates the object's position on the screen.
3. Main game loop: This section contains the main game loop, which handles user input, updates the game state, and draws the game on the screen.

## How to run

To run the game, you need to have Pygame installed. You can install it using the following command:

```
pip install pygame
```

After installing Pygame, you can run the game by running the following command:

```
python mario_game.py
```

## Acknowledgements

This game was inspired by the classic Super Mario Bros game. The images used in the game were created by Nintendo.