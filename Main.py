import sys
import pygame
import time
import sqlite3

# Initialize Pygame
pygame.init()
pygame.font.init()

# Import game mechanics and variables
from game_mechanics import (
    handle_black_obstacle_collision,
    handle_red_obstacle_collision,
    handle_coin_collision,
    handle_finish_flag_collision,
    handle_game_borders,
)
from game_variables import *


start_time = 0  # To be initialized after username input
elapsed_time = 0  # To store the final time on reaching the finish flag

# Database connection
conn = sqlite3.connect('times.db')
cursor = conn.cursor()

# Username input function
def get_username():
    """Prompt the user to enter their username."""
    username = ""
    active = True
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)

    while active:
        screen.fill(WHITE)
        prompt = font.render("Enter your username:", True, BLACK)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        user_text = font.render(username, True, BLACK)

        # Display the prompt and input box
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(user_text, (input_box.x + 10, input_box.y + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

    return username.strip()

def show_leaderboard():
    """Fetch and display leaderboard data."""
    cursor.execute("SELECT username, time, date FROM leaderboard ORDER BY time ASC LIMIT 10")
    records = cursor.fetchall()

    active = True
    header_color = (50, 50, 255)  # Blue for headers
    row_colors = [(200, 200, 200), (255, 255, 255)]  # Alternating row colors (light gray, white)
    column_width = 150  # Fixed width for each column

    while active:
        screen.fill(RED)

        # Title
        title = font.render("Leaderboard", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        # Render table headers
        headers = ["Rank", "Username", "Time", "Date"]
        for i, header in enumerate(headers):
            header_surface = font.render(header[:10], True, WHITE)
            pygame.draw.rect(
                screen, header_color,
                (50 + i * column_width, 80, column_width, 40)
            )
            screen.blit(header_surface, (50 + i * column_width + 10, 85))

        # Render leaderboard records
        for i, record in enumerate(records):
            rank = str(i + 1)
            username, time_taken, date = record
            time_display = f"{int(time_taken % 60):02}:{int((time_taken * 1000) % 1000):03}"

            # Prepare row content, truncating long text
            row_data = [
                rank[:10],
                username[:10],
                time_display[:10],
                date[:10],
            ]

            # Alternate row colors
            row_color = row_colors[i % 2]
            pygame.draw.rect(
                screen, row_color,
                (50, 120 + i * 40, column_width * len(headers), 40)
            )

            for j, col in enumerate(row_data):
                row_surface = font.render(col, True, BLACK)
                screen.blit(row_surface, (50 + j * column_width + 10, 125 + i * 40))

        # Render instructions to exit
        instructions = font.render("Press ENTER to go back", True, BLACK)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 50))

        pygame.display.flip()

        # Event handling for leaderboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Exit leaderboard on Enter
                    active = False


# Initialize game
username = get_username()
start_time = time.time()

# Game loop
running = True
winner_screen = False

def reset_game():
    """Reset all game settings to their default state."""
    global player_x, player_y, player_velocity_y, jumping, coin_counter, jump_power, coins, winner_screen, finish_flag_reached, start_time
    player_x, player_y = 100, SCREEN_HEIGHT - player_height - 20
    player_velocity_y = 0
    jumping = False
    coin_counter = 0
    jump_power = default_jump_power
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
    finish_flag_reached = False
    winner_screen = False
    start_time = time.time()

def draw_winner_screen():
    """Draw the winner screen with the time taken, restart button, and leaderboard button."""
    screen.fill(GOLD)
    message = font.render("You Win!", True, BLACK)
    time_message = font.render(f"Time: {int(elapsed_time % 60):02}:{int((elapsed_time * 1000) % 1000):03}", True, BLACK)
    user_message = font.render(f"Player: {username}", True, BLACK)

    # Restart button
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2, 150, 50)
    pygame.draw.rect(screen, BLUE, restart_button)
    restart_text = font.render("Restart", True, WHITE)
    restart_text_x = restart_button.x + (restart_button.width - restart_text.get_width()) // 2
    restart_text_y = restart_button.y + (restart_button.height - restart_text.get_height()) // 2

    # Leaderboard button
    leaderboard_text = font.render("Leaderboard", True, WHITE)
    leaderboard_button_width = leaderboard_text.get_width() + 20  # Add padding
    leaderboard_button = pygame.Rect(
        SCREEN_WIDTH // 2 - leaderboard_button_width // 2,
        SCREEN_HEIGHT // 2 + 70,
        leaderboard_button_width,
        50
    )
    pygame.draw.rect(screen, BLUE, leaderboard_button)
    leaderboard_text_x = leaderboard_button.x + (leaderboard_button.width - leaderboard_text.get_width()) // 2
    leaderboard_text_y = leaderboard_button.y + (leaderboard_button.height - leaderboard_text.get_height()) // 2

    # Draw elements on screen
    screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - 200))
    screen.blit(user_message, (SCREEN_WIDTH // 2 - user_message.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
    screen.blit(time_message, (SCREEN_WIDTH // 2 - time_message.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(restart_text, (restart_text_x, restart_text_y))
    screen.blit(leaderboard_text, (leaderboard_text_x, leaderboard_text_y))

    pygame.display.flip()
    return restart_button, leaderboard_button



while running:
    screen.fill(GREEN)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if winner_screen and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                reset_game()
            elif leaderboard_button.collidepoint(event.pos):
                show_leaderboard()

    if winner_screen:
        restart_button, leaderboard_button = draw_winner_screen()
        continue

    # Key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and not jumping:
        player_velocity_y = -jump_power
        jumping = True
        on_red_obstacle = False
        current_red_obstacle = None

    # Gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Enforce game borders
    player_x, player_y = handle_game_borders(player_x, player_y, player_width, player_height, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Timer logic
    elapsed_time = time.time() - start_time
    timer_text = f"{int(elapsed_time % 60):02}:{int((elapsed_time * 1000) % 1000):03}"

    # Player rectangle
    player_rect = pygame.Rect(player_x, player_y - camera_y, player_width, player_height)

    # Black obstacle collision
    player_velocity_y, jumping, player_y, player_x = handle_black_obstacle_collision(
        player_rect, obstacles, player_velocity_y, jumping, player_y, camera_y, player_x, player_width
    )

    # Red obstacle collision
    player_velocity_y, jumping, player_y, current_red_obstacle, player_x = handle_red_obstacle_collision(
        player_rect, red_obstacles, player_velocity_y, jumping, player_y, camera_y, current_red_obstacle, player_x,
        player_width
    )

    # Coin collision
    coins, coin_counter, jump_power = handle_coin_collision(
        player_rect, coins, coin_counter, jump_power, camera_y
    )

    # Finish flag collision
    if coin_counter == total_coins:
        finish_flag_reached = handle_finish_flag_collision(
            player_rect, finish_flag_x, finish_flag_y, camera_y
        )
        if finish_flag_reached:
            winner_screen = True
            cursor.execute("INSERT INTO leaderboard (username, time, date) VALUES (?, ?, ?)",
                           (username, elapsed_time, time.strftime("%Y-%m-%d")))
            conn.commit()

    # Camera logic
    camera_y = player_y - SCREEN_HEIGHT // 2

    # Draw elements
    pygame.draw.rect(screen, BLUE, (player_x, player_y - camera_y, player_width, player_height))
    for obstacle_x, obstacle_y in obstacles:
        pygame.draw.rect(screen, BLACK, (obstacle_x, obstacle_y - camera_y, 100, 50))
    for red_obstacle in red_obstacles:
        pygame.draw.rect(screen, RED, (red_obstacle[0], red_obstacle[1] - camera_y, 50, 50))
    for coin_x, coin_y in coins:
        pygame.draw.circle(screen, YELLOW, (coin_x, coin_y - camera_y), 10)
    if coin_counter == total_coins:
        pygame.draw.rect(screen, GOLD, (finish_flag_x - 15, finish_flag_y - camera_y, 30, 80))
    counter_text = font.render(f"Coins: {coin_counter}", True, BLACK)
    timer_surface = font.render(f"Time: {timer_text}", True, BLACK)
    screen.blit(counter_text, (10, 10))
    screen.blit(timer_surface, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

conn.close()
