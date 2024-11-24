import pygame
import sys
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("You Are Your Own Enemy")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # You can replace None with the path to a custom font

# Game variables
player_size = 30
player_speed = 4
goal_size = 20
ghost_size = player_size
max_score = 20
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
goal_x, goal_y = random.randint(0, SCREEN_WIDTH - goal_size), random.randint(0, SCREEN_HEIGHT - goal_size)
score = 0
ghosts = []
history = deque(maxlen=300)

# Functions for resetting the game state
def reset_game():
    """Reset all game variables to start a new game."""
    global player_x, player_y, goal_x, goal_y, score, ghosts, history
    player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    goal_x, goal_y = random.randint(0, SCREEN_WIDTH - goal_size), random.randint(0, SCREEN_HEIGHT - goal_size)
    score = 0
    ghosts = []
    history = deque(maxlen=300)

# Load images
player_img = pygame.image.load("player.png")  # Replace with your image path
goal_img = pygame.image.load("goal.png")
ghost_img = pygame.image.load("ghost.png")
background_img = pygame.image.load("background.jpg")  # Background image

# Resize if necessary
player_img = pygame.transform.scale(player_img, (player_size, player_size))
goal_img = pygame.transform.scale(goal_img, (goal_size, goal_size))
ghost_img = pygame.transform.scale(ghost_img, (ghost_size, ghost_size))

# Functions
def draw_background():
    """Draw the background image to fill the screen."""
    screen.blit(background_img, (0, 0))

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_goal(x, y):
    screen.blit(goal_img, (x, y))

def draw_ghost(x, y):
    screen.blit(ghost_img, (x, y))

def check_collision(x1, y1, size1, x2, y2, size2):
    """Check if two rectangles overlap."""
    return (x1 < x2 + size2 and x1 + size1 > x2 and y1 < y2 + size2 and y1 + size1 > y2)

def reset_goal():
    """Place a new goal at a random position."""
    return random.randint(0, SCREEN_WIDTH - goal_size), random.randint(0, SCREEN_HEIGHT - goal_size)

def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_health_bar(health):
    pygame.draw.rect(screen, RED, (10, 50, 100, 10))  # Background
    pygame.draw.rect(screen, GREEN, (10, 50, health, 10))  # Foreground (health)

def show_menu():
    screen.fill(BLACK)
    title_text = font.render("You Are Your Own Enemy", True, WHITE)
    start_text = font.render("Press Enter to start", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 4))
    screen.blit(start_text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def show_game_over():
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    restart_text = font.render("Press Enter to Restart", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
    screen.blit(restart_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()  # Reset the game state when Enter is pressed
                waiting = False

def fade_out():
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(20)

# Main game loop
def game_loop():
    global player_x, player_y, goal_x, goal_y, score, ghosts, history, running
    running = True
    while running:
        draw_background()  # Draw the background image

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_y += player_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Ensure player stays within bounds
        player_x = max(0, min(SCREEN_WIDTH - player_size, player_x))
        player_y = max(0, min(SCREEN_HEIGHT - player_size, player_y))

        # Update player history
        history.append((player_x, player_y))

        # Check for goal collision
        if check_collision(player_x, player_y, player_size, goal_x, goal_y, goal_size):
            score += 1
            goal_x, goal_y = reset_goal()
            ghosts.append(list(history))  # Spawn a new ghost with current history

        # Draw goal and player
        draw_goal(goal_x, goal_y)
        draw_player(player_x, player_y)

        # Draw ghosts
        for ghost_history in ghosts:
            if ghost_history:
                ghost_x, ghost_y = ghost_history.pop(0)  # Replay ghost's movements
                draw_ghost(ghost_x, ghost_y)
                ghost_history.append((ghost_x, ghost_y))  # Loop movements
                if check_collision(player_x, player_y, player_size, ghost_x, ghost_y, ghost_size):
                    # Game over
                    fade_out()
                    show_game_over()
                    running = False

        # Display score and health bar
        display_score()
        draw_health_bar(100)  # You can replace the value with actual health mechanics

        # Check win condition
        if score >= max_score:
            win_text = font.render("You Win!", True, WHITE)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            running = False

        # Update the screen
        pygame.display.update()
        clock.tick(30)  # Limit FPS to 30

# Start menu
show_menu()

# Start the game loop
game_loop()
