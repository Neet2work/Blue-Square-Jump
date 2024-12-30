import pygame


# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_width = 50
player_height = 50
player_x = 100
player_y = SCREEN_HEIGHT - player_height - 20
player_speed = 5
default_jump_power = 15
jump_power = default_jump_power
gravity = 1
player_velocity_y = 0
jumping = False
on_red_obstacle = False
current_red_obstacle = None

# Camera settings
camera_y = 0

# Obstacle settings
obstacle_width = 100
obstacle_height = 50

# Black obstacles
obstacles = [
    (300, SCREEN_HEIGHT - obstacle_height - 20),
    (600, SCREEN_HEIGHT - 310 - obstacle_height - 20),
    (400, SCREEN_HEIGHT - 100 - obstacle_height),
    (580, SCREEN_HEIGHT - 175 - obstacle_height),
    (420, SCREEN_HEIGHT - 250 - obstacle_height),
    (600, SCREEN_HEIGHT - obstacle_height - 20),
    (300, SCREEN_HEIGHT - 300 - obstacle_height - 20),
    (150, SCREEN_HEIGHT - 175 - obstacle_height)
]

# Red obstacle settings
red_obstacle_size = 50
highest_black_y = min(obstacle[1] for obstacle in obstacles)
red_obstacles = [
    [350, highest_black_y - 75, 3],
    [700, highest_black_y - 200, 2],
    [450, highest_black_y - 400, 3],
    [250, highest_black_y - 125, 2]
]
red_obstacles.sort(key=lambda x: x[1])
for i in range(1, len(red_obstacles)):
    if red_obstacles[i][1] - red_obstacles[i - 1][1] < 100:
        red_obstacles[i][1] = red_obstacles[i - 1][1] - 100

# Coins
coins = [
    (200, SCREEN_HEIGHT - 250),
    (775, SCREEN_HEIGHT - 550),
    (450, SCREEN_HEIGHT - 50),
    (500, SCREEN_HEIGHT - 310),
    (200, SCREEN_HEIGHT - 375),
    (175, SCREEN_HEIGHT - 400),
    (600, SCREEN_HEIGHT - 500),
    (500, SCREEN_HEIGHT - 450),
]
total_coins = len(coins)
coin_counter = 0

# Finish flag
highest_red_obstacle = max(red_obstacles, key=lambda x: x[1])
finish_flag_x = highest_red_obstacle[0] + red_obstacle_size // 2
finish_flag_y = highest_red_obstacle[1] - 550
finish_flag_reached = False

# Font settings
font = pygame.font.Font(None, 36)
