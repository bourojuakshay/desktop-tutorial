import pygame
import random
import os

# Initialize pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game - Gold")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# High score file
high_score_file = "highscore.txt"
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as f:
        content = f.read()
        if content:
            high_score = int(content)
        else:
            high_score = 0
else:
    high_score = 0

# Player
player_width = 50
player_height = 30
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Bullet
bullets = []
bullet_speed = 7

# Enemy
enemy_width = 40
enemy_height = 30
enemies = []
enemy_speed = 2

# Game variables
score = 0
lives = 3
game_over = False
paused = False
game_state = "start"  # Can be: start, playing, game_over

def draw_text(text, x, y, font_size=36, center=False):
    font_used = pygame.font.SysFont(None, font_size)
    img = font_used.render(text, True, WHITE)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

def reset_game():
    global bullets, enemies, player_x, score, lives, game_over
    bullets = []
    enemies = []
    player_x = WIDTH // 2 - player_width // 2
    score = 0
    lives = 3
    game_over = False

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_state == "start":
        draw_text("Au", WIDTH // 2, HEIGHT // 3, font_size=80, center=True)
        draw_text("Press SPACE to Start", WIDTH // 2, HEIGHT // 2 + 30, center=True)
        if keys[pygame.K_SPACE]:
            game_state = "playing"
            reset_game()

    elif game_state == "playing":
        # Pause
        if keys[pygame.K_p]:
            paused = not paused

        if not paused:
            # Player movement
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
                player_x += player_speed
            if keys[pygame.K_SPACE]:
                if len(bullets) < 5:
                    bullets.append([player_x + player_width // 2, player_y])

            # Update bullets
            for bullet in bullets[:]:
                bullet[1] -= bullet_speed
                if bullet[1] < 0:
                    bullets.remove(bullet)

            # Spawn enemies (less frequent = fewer enemies)
            if random.randint(1, 100) == 1:
                enemy_x = random.randint(0, WIDTH - enemy_width)
                enemies.append([enemy_x, 0])

            # Update enemies
            for enemy in enemies[:]:
                enemy[1] += enemy_speed
                if enemy[1] > HEIGHT:
                    enemies.remove(enemy)
                    lives -= 1
                    if lives == 0:
                        game_state = "game_over"

            # Collisions
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if (
                        enemy[0] < bullet[0] < enemy[0] + enemy_width
                        and enemy[1] < bullet[1] < enemy[1] + enemy_height
                    ):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 1
                        break

        # Draw player
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
        for bullet in bullets:
            pygame.draw.circle(screen, WHITE, (bullet[0], bullet[1]), 5)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))

        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Lives: {lives}", 10, 40)
        draw_text(f"High Score: {high_score}", 10, 70)

    elif game_state == "game_over":
        if score > high_score:
            high_score = score
            with open(high_score_file, "w") as f:
                f.write(str(high_score))

        draw_text("Game Over", WIDTH // 2, HEIGHT // 3, font_size=72, center=True)
        draw_text(f"Your Score: {score}", WIDTH // 2, HEIGHT // 2, center=True)
        draw_text(f"High Score: {high_score}", WIDTH // 2, HEIGHT // 2 + 40, center=True)
        draw_text("Press R to Restart or Q to Quit", WIDTH // 2, HEIGHT // 2 + 80, center=True)

        if keys[pygame.K_r]:
            game_state = "playing"
            reset_game()
        if keys[pygame.K_q]:
            running = False

    pygame.display.flip()

pygame.quit()
