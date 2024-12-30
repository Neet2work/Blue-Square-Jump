import pygame
from game_variables import *

def handle_black_obstacle_collision(player_rect, obstacles, player_velocity_y, jumping, player_y, camera_y, player_x, player_width):
    """Handle collisions with black obstacles."""
    for obstacle_x, obstacle_y in obstacles:
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y - camera_y, obstacle_width, obstacle_height)
        if player_rect.colliderect(obstacle_rect):
            if player_y + player_height - player_velocity_y <= obstacle_rect.top + camera_y:  # Top collision
                player_y = obstacle_rect.top + camera_y - player_height
                player_velocity_y = 0
                jumping = False
            elif player_y - player_velocity_y >= obstacle_rect.bottom + camera_y:  # Bottom collision
                player_y = obstacle_rect.bottom + camera_y
                player_velocity_y = 0
            elif player_x + player_width > obstacle_rect.left and player_x < obstacle_rect.left:  # Left collision
                player_x = obstacle_rect.left - player_width
            elif player_x < obstacle_rect.right and player_x + player_width > obstacle_rect.right:  # Right collision
                player_x = obstacle_rect.right
    return player_velocity_y, jumping, player_y, player_x

def handle_red_obstacle_collision(player_rect, red_obstacles, player_velocity_y, jumping, player_y, camera_y, current_red_obstacle, player_x, player_width):
    """Handle collisions with red obstacles."""
    on_red_obstacle = False
    for i, red_obstacle in enumerate(red_obstacles):
        red_obstacle_x, red_obstacle_y, red_obstacle_speed = red_obstacle
        red_obstacle_rect = pygame.Rect(red_obstacle_x, red_obstacle_y - camera_y, red_obstacle_size, red_obstacle_size)
        if player_rect.colliderect(red_obstacle_rect):
            if player_y + player_height - player_velocity_y <= red_obstacle_rect.top + camera_y:  # Top collision
                player_y = red_obstacle_rect.top + camera_y - player_height
                player_velocity_y = 0
                jumping = False
                on_red_obstacle = True
                current_red_obstacle = i
            elif player_y - player_velocity_y >= red_obstacle_rect.bottom + camera_y:  # Bottom collision
                player_y = red_obstacle_rect.bottom + camera_y
                player_velocity_y = 0
            elif player_x + player_width > red_obstacle_rect.left and player_x < red_obstacle_rect.left:  # Left collision
                player_x = red_obstacle_rect.left - player_width
            elif player_x < red_obstacle_rect.right and player_x + player_width > red_obstacle_rect.right:  # Right collision
                player_x = red_obstacle_rect.right
        red_obstacle[0] += red_obstacle_speed
        if red_obstacle[0] < 0 or red_obstacle[0] + red_obstacle_size > SCREEN_WIDTH:  # Boundary bounce
            red_obstacle[2] = -red_obstacle_speed
    if on_red_obstacle and current_red_obstacle is not None:
        player_x += red_obstacles[current_red_obstacle][2]
    return player_velocity_y, jumping, player_y, current_red_obstacle, player_x

def handle_coin_collision(player_rect, coins, coin_counter, jump_power, camera_y):
    """Handle collisions with coins."""
    for coin in coins[:]:
        coin_rect = pygame.Rect(coin[0], coin[1] - camera_y, 20, 20)
        if player_rect.colliderect(coin_rect):
            coins.remove(coin)
            coin_counter += 1
            if coin_counter == 4:
                jump_power += 3
            elif coin_counter == len(coins) + 1:
                jump_power += 2
    return coins, coin_counter, jump_power

def handle_finish_flag_collision(player_rect, finish_flag_x, finish_flag_y, camera_y):
    """Handle collisions with the finish flag."""
    finish_flag_rect = pygame.Rect(finish_flag_x - 15, finish_flag_y - camera_y, 30, 80)
    if player_rect.colliderect(finish_flag_rect):
        return True  # Finish flag reached
    return False

def handle_game_borders(player_x, player_y, player_width, player_height, screen_width, screen_height):
    """Restrict player within the game boundaries."""
    if player_x < 0:  # Left border
        player_x = 0
    elif player_x + player_width > screen_width:  # Right border
        player_x = screen_width - player_width
    if player_y + player_height > screen_height:  # Bottom border
        player_y = screen_height - player_height
    return player_x, player_y
