import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 736, 414
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Blocks!")

background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

character_images = []
for i in range(179):
    img_path = os.path.join("character_images", f"{i:03}.png")
    character_images.append(pygame.image.load(img_path))

player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
current_image_index = 0
image_change_event = pygame.USEREVENT + 2
pygame.time.set_timer(image_change_event, 100)

enemy_list = []
enemy_images = [pygame.image.load(os.path.join("enemy_images", f"enemy_{i}.png")) for i in range(1, 3)]
new_enemy_event = pygame.USEREVENT + 1
pygame.time.set_timer(new_enemy_event, 500)

score = 0
high_score = 0
font = pygame.font.Font(None, 35)

def create_enemy():
    enemy_size = random.randint(40, 70)
    enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
    enemy_speed = random.randint(5, 15)
    enemy_image = random.choice(enemy_images)
    return {"pos": enemy_pos, "size": enemy_size, "speed": enemy_speed, "image": pygame.transform.scale(enemy_image, (enemy_size, enemy_size))}

def game_over():
    global running, score, high_score
    high_score = max(high_score, score)
    screen.blit(background_image, (0, 0))

    game_over_surface = pygame.Surface((400, 300))
    game_over_surface.set_alpha(200)
    game_over_surface.fill((100, 100, 200))
    screen.blit(game_over_surface, (WIDTH // 2 - 200, HEIGHT // 2 - 150))

    pygame.draw.rect(screen, (200, 200, 255), (WIDTH // 2 - 200, HEIGHT // 2 - 150, 400, 300), 5, border_radius=20)

    draw_text("Game Over", 80, WHITE, WIDTH // 2, HEIGHT // 2 - 80)
    score_text = f"Score: {score}"
    high_score_text = f"High Score: {high_score}"
    restart_text = "Press R to Restart"

    draw_text(score_text, 50, WHITE, WIDTH // 2, HEIGHT // 2 + 20)
    draw_text(high_score_text, 50, WHITE, WIDTH // 2, HEIGHT // 2 + 60)
    draw_text(restart_text, 40, WHITE, WIDTH // 2, HEIGHT // 2 + 100)

    pygame.display.flip()
    wait_for_restart()

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def wait_for_restart():
    global score, enemy_list, player_pos
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                score = 0
                enemy_list.clear()
                player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
                return

running = True
clock = pygame.time.Clock()
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == new_enemy_event:
            enemy_list.append(create_enemy())
        if event.type == image_change_event:
            current_image_index = (current_image_index + 1) % len(character_images)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 10
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += 10

    for enemy in enemy_list[:]:
        enemy["pos"][1] += enemy["speed"]
        if enemy["pos"][1] > HEIGHT:
            enemy_list.remove(enemy)
            score += 1

        if (enemy["pos"][0] < player_pos[0] < enemy["pos"][0] + enemy["size"] or
            enemy["pos"][0] < player_pos[0] + player_size < enemy["pos"][0] + enemy["size"]):
            if enemy["pos"][1] + enemy["size"] >= player_pos[1] and enemy["pos"][1] <= player_pos[1] + player_size:
                game_over()

    screen.blit(pygame.transform.scale(character_images[current_image_index], (player_size, player_size)), player_pos)
    for enemy in enemy_list:
        screen.blit(enemy["image"], enemy["pos"])

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
