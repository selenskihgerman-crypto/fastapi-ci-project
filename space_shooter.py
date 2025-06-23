"""Космический скролл-шутер"""

import pygame
import random
import os

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Космический шутер")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Загрузка изображений
def load_image(name, scale=1):
    try:
        image = pygame.image.load(f"img/{name}")
        if scale != 1:
            size = image.get_size()
            image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
        return image
    except:
        # Если изображение не найдено, создаем заглушку
        surf = pygame.Surface((50, 50))
        surf.fill(RED if "enemy" in name else GREEN if "player" in name else BLUE)
        return surf


# Создаем папку для изображений, если её нет
if not os.path.exists("img"):
    os.makedirs("img")

# Загрузка изображений
try:
    background_img = pygame.image.load("img/space_bg.png")
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
except:
    background_img = pygame.Surface((screen_width, screen_height))
    background_img.fill(BLACK)
    # Добавляем звёзды для фона
    for _ in range(100):
        x, y = random.randint(0, screen_width), random.randint(0, screen_height)
        pygame.draw.circle(background_img, WHITE, (x, y), 1)

player_img = load_image("ship.png", 0.5)
enemy_img = load_image("enemy_ship.png", 0.5)
bullet_img = load_image("laser_bullet.png")

# Если пуля - заглушка, создаем новую
if bullet_img.get_size() == (50, 50):
    bullet_img = pygame.Surface((5, 15), pygame.SRCALPHA)
    pygame.draw.rect(bullet_img, (0, 255, 255), (0, 0, 5, 15))

# Игрок
player_width, player_height = player_img.get_size()
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 20
player_speed = 5
player_x_change = 0

# Враги
enemies = []
enemy_speed = 2
enemy_spawn_rate = 30

# Пули
bullets = []
bullet_speed = 10

# Очки
score = 0
font = pygame.font.SysFont(None, 36)


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y):
    screen.blit(enemy_img, (x, y))


def bullet(x, y):
    screen.blit(bullet_img, (x, y))


def show_score():
    score_text = font.render(f"Очки: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def spawn_enemy():
    x = random.randint(0, screen_width - enemy_img.get_width())
    y = random.randint(-100, -40)  # Фиксированные безопасные значения
    enemies.append([x, y])


def fire_bullet():
    if len(bullets) < 3:  # Ограничение количества пуль
        bullets.append([
            player_x + player_width // 2 - bullet_img.get_width() // 2,
            player_y
        ])


running = True
clock = pygame.time.Clock()

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            if event.key == pygame.K_SPACE:
                fire_bullet()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Обновление позиции игрока
    player_x += player_x_change
    player_x = max(0, min(player_x, screen_width - player_width))

    # Спавн врагов
    if random.randint(1, enemy_spawn_rate) == 1:
        spawn_enemy()

    # Обновление позиции врагов
    for enemy_pos in enemies[:]:
        enemy_pos[1] += enemy_speed
        if enemy_pos[1] > screen_height:
            enemies.remove(enemy_pos)
            score = max(0, score - 1)

    # Обновление позиции пуль
    for bullet_pos in bullets[:]:
        bullet_pos[1] -= bullet_speed
        if bullet_pos[1] < 0:
            bullets.remove(bullet_pos)

    # Проверка столкновений
    for bullet_pos in bullets[:]:
        bullet_rect = pygame.Rect(
            bullet_pos[0],
            bullet_pos[1],
            bullet_img.get_width(),
            bullet_img.get_height()
        )

        for enemy_pos in enemies[:]:
            enemy_rect = pygame.Rect(
                enemy_pos[0],
                enemy_pos[1],
                enemy_img.get_width(),
                enemy_img.get_height()
            )

            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet_pos)
                enemies.remove(enemy_pos)
                score += 10
                break

    # Проверка столкновения с игроком
    player_rect = pygame.Rect(
        player_x,
        player_y,
        player_width,
        player_height
    )

    for enemy_pos in enemies[:]:
        enemy_rect = pygame.Rect(
            enemy_pos[0],
            enemy_pos[1],
            enemy_img.get_width(),
            enemy_img.get_height()
        )

        if player_rect.colliderect(enemy_rect):
            running = False

    # Отрисовка
    screen.blit(background_img, (0, 0))

    for bullet_pos in bullets:
        bullet(bullet_pos[0], bullet_pos[1])

    for enemy_pos in enemies:
        enemy(enemy_pos[0], enemy_pos[1])

    player(player_x, player_y)
    show_score()

    pygame.display.update()
    clock.tick(60)

pygame.quit()